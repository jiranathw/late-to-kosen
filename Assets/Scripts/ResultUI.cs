using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Win / lose screen.
//
// This builds its own Canvas at runtime and finds the GameManager by itself, so
// there is NOTHING to wire up in the scene and nothing for anyone to accidentally
// unassign in the Inspector. Every scene in the build gets it automatically.
//
// Text is English on purpose: the default TextMeshPro font (LiberationSans) has no
// Thai glyphs, so Thai text would render as empty boxes. If you want Thai later,
// import a Thai TTF as a TMP Font Asset first, then swap the strings below.
public class ResultUI : MonoBehaviour
{
    private const string RestartHint = "Press R to try again    |    Press Q to quit";

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
        panel.color = new Color(0f, 0f, 0f, 0.72f);
        Stretch(panel.rectTransform);

        headline = MakeText(canvasGo.transform, "Headline", 130f, new Vector2(0f, 90f), new Vector2(1600f, 240f));
        detail = MakeText(canvasGo.transform, "Detail", 52f, new Vector2(0f, -110f), new Vector2(1600f, 260f));
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
        if (gm == null)
        {
            Hide();
            return;
        }

        if (!gm.IsGameOver)
        {
            Hide();
            return;
        }

        Show(gm);

        if (Input.GetKeyDown(KeyCode.R))
        {
            gm.RestartLevel();
        }
        else if (Input.GetKeyDown(KeyCode.Q))
        {
            gm.QuitGame();
        }
    }

    private void Show(GameManager gm)
    {
        if (gm.DidWin)
        {
            headline.text = "YOU MADE IT!";
            headline.color = new Color(0.55f, 1f, 0.6f);
            detail.text =
                $"Made it with {FormatTime(gm.TimeRemaining)} to spare, {gm.Lives} lives left\n" +
                $"Traps survived: {gm.TrapsSurvived}/{gm.TrapTotal}    Deaths: {gm.DeathCount}\n" +
                $"SCORE  {gm.Score}\n\n{RestartHint}";
        }
        else if (gm.LoseReason == "lives")
        {
            headline.text = "OUT OF LIVES";
            headline.color = new Color(1f, 0.45f, 0.45f);
            detail.text =
                $"The traps got you {gm.DeathCount} times. You're not going anywhere.\n" +
                $"Traps survived: {gm.TrapsSurvived}/{gm.TrapTotal}\n" +
                $"SCORE  {gm.Score}\n\n{RestartHint}";
        }
        else
        {
            headline.text = "THE BELL RANG";
            headline.color = new Color(1f, 0.45f, 0.45f);
            detail.text =
                $"You were late. Lives left: {gm.Lives}\n" +
                $"Traps survived: {gm.TrapsSurvived}/{gm.TrapTotal}    Deaths: {gm.DeathCount}\n" +
                $"SCORE  {gm.Score}\n\n{RestartHint}";
        }

        group.alpha = 1f;
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
