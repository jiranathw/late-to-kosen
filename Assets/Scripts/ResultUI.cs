using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Stage-clear / final-results / game-over screen.
//
// This builds its own Canvas at runtime and finds the GameManager by itself, so
// there is NOTHING to wire up in the scene and nothing for anyone to accidentally
// unassign in the Inspector. Every scene in the build gets it automatically.
//
// Four states, because "you finished stage 1 of 3" and "you finished the whole
// morning" are different news and deserve different screens:
//
//   STAGE CLEAR    won, and there is another stage  -> Space continues
//   YOU MADE IT    won the final stage              -> run totals, R replays the run
//   OUT OF LIVES   lost this stage to the traps     -> R retries THIS stage
//   THE BELL RANG  lost this stage to the clock     -> R retries THIS stage
//
// Text is English on purpose: the default TextMeshPro font (LiberationSans) has no
// Thai glyphs, so Thai text would render as empty boxes. If you want Thai later,
// import a Thai TTF as a TMP Font Asset first, then swap the strings below.
public class ResultUI : MonoBehaviour
{
    private static ResultUI instance;

    private TMP_Text headline;
    private TMP_Text detail;
    private CanvasGroup group;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (instance != null) return;

        GameObject host = new GameObject("~ResultUI");
        DontDestroyOnLoad(host);
        instance = host.AddComponent<ResultUI>();
    }

    private void Awake()
    {
        instance = this;
        Build();
        Hide();
    }

    private void Build()
    {
        // Canvas
        GameObject canvasGo = new GameObject("ResultCanvas");
        canvasGo.transform.SetParent(transform, false);

        Canvas canvas = canvasGo.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 100; // always on top of the timer / death counter

        CanvasScaler scaler = canvasGo.AddComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920f, 1080f);
        scaler.matchWidthOrHeight = 0.5f;

        group = canvasGo.AddComponent<CanvasGroup>();
        group.interactable = false;
        group.blocksRaycasts = false;

        // Dim panel behind the text so it stays readable over any tileset
        GameObject panelGo = new GameObject("Dim");
        panelGo.transform.SetParent(canvasGo.transform, false);
        Image panel = panelGo.AddComponent<Image>();
        panel.color = new Color(0f, 0f, 0f, 0.78f);
        Stretch(panel.rectTransform);

        headline = MakeText(canvasGo.transform, "Headline", 120f, new Vector2(0f, 200f), new Vector2(1700f, 240f));
        detail   = MakeText(canvasGo.transform, "Detail",    44f, new Vector2(0f, -110f), new Vector2(1700f, 540f));
    }

    private static void Stretch(RectTransform rt)
    {
        rt.anchorMin = Vector2.zero;
        rt.anchorMax = Vector2.one;
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;
    }

    private static TMP_Text MakeText(Transform parent, string name, float size, Vector2 pos, Vector2 dimensions)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(parent, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        text.fontSize = size;
        text.alignment = TextAlignmentOptions.Center;
        text.color = Color.white;

        RectTransform rt = text.rectTransform;
        rt.anchorMin = new Vector2(0.5f, 0.5f);
        rt.anchorMax = new Vector2(0.5f, 0.5f);
        rt.pivot = new Vector2(0.5f, 0.5f);
        rt.anchoredPosition = pos;
        rt.sizeDelta = dimensions;

        return text;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null || !gm.IsGameOver)
        {
            Hide();
            return;
        }

        Show(gm);
        ReadInput(gm);
    }

    // Space only does anything on a mid-run stage clear. Binding it on every
    // screen would let a player who is mashing Space at the instant of death
    // skip straight past the game-over screen without ever seeing it.
    private static void ReadInput(GameManager gm)
    {
        bool midRunClear = gm.DidWin && !gm.IsFinalLevel;

        if (midRunClear && (Input.GetKeyDown(KeyCode.Space) || Input.GetKeyDown(KeyCode.Return)))
        {
            gm.NextLevel();
            return;
        }

        if (Input.GetKeyDown(KeyCode.R))
        {
            // On the final screen R restarts the whole morning; everywhere else
            // it retries just the stage you are standing in.
            if (gm.DidWin && gm.IsFinalLevel) gm.RestartRun();
            else gm.RestartLevel();
            return;
        }

        if (Input.GetKeyDown(KeyCode.Q)) gm.QuitGame();
    }

    private void Show(GameManager gm)
    {
        GameSession session = GameSession.Instance;
        int stage = gm.LevelIndex;

        if (gm.DidWin && !gm.IsFinalLevel)
        {
            headline.text = $"STAGE {stage} CLEAR";
            headline.color = new Color(0.55f, 1f, 0.6f);

            detail.text =
                $"{GameSession.TitleFor(stage)}  -  done\n\n" +
                $"{FormatTime(gm.TimeRemaining)} to spare    {gm.Lives} lives left    " +
                $"traps survived {gm.TrapsSurvived}/{gm.TrapTotal}    deaths {gm.DeathCount}\n" +
                $"Stage score  {gm.Score}{RunTotalLine(session)}\n\n" +
                $"NEXT:  STAGE {stage + 1}  -  {GameSession.TitleFor(stage + 1)}\n" +
                $"{GameSession.SubtitleFor(stage + 1)}\n\n" +
                "Press SPACE to keep going    |    R replay this stage    |    Q quit";
        }
        else if (gm.DidWin)
        {
            headline.text = "YOU MADE IT!";
            headline.color = new Color(0.55f, 1f, 0.6f);

            detail.text =
                "You sat down before the lecturer shut the door.\n\n" +
                StageBreakdown(session) +
                $"\nTOTAL SCORE  {TotalScore(session, gm)}\n" +
                $"Total deaths {TotalDeaths(session, gm)}    " +
                $"morning spent {FormatTime(TotalTime(session, gm))}\n\n" +
                "Press R to run the whole morning again    |    Q quit";
        }
        else if (gm.LoseReason == "lives")
        {
            headline.text = "OUT OF LIVES";
            headline.color = new Color(1f, 0.45f, 0.45f);

            detail.text =
                $"STAGE {stage}  -  {GameSession.TitleFor(stage)}\n\n" +
                $"The road got you {gm.DeathCount} times. You are not past this one yet.\n" +
                $"Traps survived {gm.TrapsSurvived}/{gm.TrapTotal}\n\n" +
                $"Press R to retry STAGE {stage}    |    Q quit\n" +
                "Only this stage restarts. Everything you already cleared stays cleared.";
        }
        else
        {
            headline.text = "THE BELL RANG";
            headline.color = new Color(1f, 0.45f, 0.45f);

            detail.text =
                $"STAGE {stage}  -  {GameSession.TitleFor(stage)}\n\n" +
                $"Out of time with {gm.Lives} lives still in hand. Too careful, not fast enough.\n" +
                $"Traps survived {gm.TrapsSurvived}/{gm.TrapTotal}    deaths {gm.DeathCount}\n\n" +
                $"Press R to retry STAGE {stage}    |    Q quit\n" +
                "Only this stage restarts. Everything you already cleared stays cleared.";
        }

        group.alpha = 1f;
    }

    // The stage that just ended is already banked in the session by the time
    // this runs - GameManager.WinGame records before the screen appears - so the
    // session totals are complete on their own. The gm fallbacks below only
    // matter if someone deleted GameSession.cs.
    private static int TotalScore(GameSession s, GameManager gm) => s != null ? s.TotalScore : gm.Score;
    private static int TotalDeaths(GameSession s, GameManager gm) => s != null ? s.TotalDeaths : gm.DeathCount;
    private static float TotalTime(GameSession s, GameManager gm) => s != null ? s.TotalTimeUsed : gm.TimeUsed;

    private static string RunTotalLine(GameSession s) =>
        s != null ? $"        Run total  {s.TotalScore}" : string.Empty;

    private static string StageBreakdown(GameSession s)
    {
        if (s == null) return string.Empty;

        string rows = string.Empty;
        for (int lv = 1; lv <= GameSession.LevelCount; lv++)
        {
            string title = GameSession.TitleFor(lv);
            rows += $"Stage {lv}   {title.PadRight(12)}  {s.ScoreFor(lv),6} pts    " +
                    $"{s.DeathsFor(lv)} deaths    {FormatTime(s.TimeUsedFor(lv))}\n";
        }
        return rows;
    }

    private void Hide()
    {
        if (group != null) group.alpha = 0f;
    }

    private static string FormatTime(float seconds)
    {
        int m = Mathf.FloorToInt(seconds / 60f);
        int s = Mathf.FloorToInt(seconds % 60f);
        return $"{m:00}:{s:00}";
    }
}
