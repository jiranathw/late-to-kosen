using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

// "STAGE 2/2 - INSIDE", plus the title card that flashes up when a stage
// starts.
//
// Once the game is three scenes instead of one, the player needs to be told
// where they are, otherwise the stages read as one level that keeps reloading
// for no reason. The card is deliberately non-blocking: it does not pause, it
// does not eat input, it just fades out over the first couple of seconds while
// you are already walking.
//
// Self-bootstrapping like the rest of the UI, so there is nothing in any scene
// to wire up or accidentally delete.
public class StageBannerUI : MonoBehaviour
{
    private const float HoldSeconds = 1.6f;
    private const float FadeSeconds = 1.0f;

    private static StageBannerUI instance;

    private TMP_Text corner;
    private TMP_Text cardTitle;
    private TMP_Text cardSubtitle;
    private CanvasGroup cardGroup;

    private float cardTimer;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (instance != null) return;

        GameObject host = new GameObject("~StageBannerUI");
        DontDestroyOnLoad(host);
        instance = host.AddComponent<StageBannerUI>();
    }

    private void Awake()
    {
        instance = this;
        Build();
        cardTimer = HoldSeconds + FadeSeconds;
    }

    private void OnEnable()  { SceneManager.sceneLoaded += OnSceneLoaded; }
    private void OnDisable() { SceneManager.sceneLoaded -= OnSceneLoaded; }

    // Re-arm on every scene load. The object survives the load, so without this
    // the card would only ever be seen on stage 1.
    private void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        cardTimer = HoldSeconds + FadeSeconds;
    }

    private void Build()
    {
        // Created WITH a RectTransform. A GameObject made bare gets a plain
        // Transform, and swapping that for a RectTransform afterwards - which is
        // what AddComponent<RectTransform>() has to do - is the one UI
        // construction step Unity is not reliable about. Every Canvas child
        // below is built the same way for the same reason.
        GameObject canvasGo = new GameObject("StageBannerCanvas", typeof(RectTransform));
        canvasGo.transform.SetParent(transform, false);

        Canvas canvas = canvasGo.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 60; // above the HUD, below the pause and result screens

        UnityEngine.UI.CanvasScaler scaler = canvasGo.AddComponent<UnityEngine.UI.CanvasScaler>();
        scaler.uiScaleMode = UnityEngine.UI.CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920f, 1080f);
        scaler.matchWidthOrHeight = 0.5f;

        // CanvasGroup lives in UnityEngine, not UnityEngine.UI - qualifying it
        // with UI does not compile.
        CanvasGroup rootGroup = canvasGo.AddComponent<CanvasGroup>();
        rootGroup.interactable = false;
        rootGroup.blocksRaycasts = false;

        // Persistent corner label, top-centre so it clears the timer on the
        // left and the death counter on the right.
        corner = MakeText(canvasGo.transform, "StageLabel", 30f,
                          new Vector2(0.5f, 1f), new Vector2(0f, -28f),
                          TextAlignmentOptions.Top, new Vector2(900f, 44f));
        corner.color = new Color(1f, 1f, 1f, 0.75f);

        // Title card
        GameObject cardGo = new GameObject("TitleCard", typeof(RectTransform));
        cardGo.transform.SetParent(canvasGo.transform, false);
        cardGroup = cardGo.AddComponent<CanvasGroup>();
        RectTransform crt = (RectTransform)cardGo.transform;
        crt.anchorMin = Vector2.zero;
        crt.anchorMax = Vector2.one;
        crt.offsetMin = Vector2.zero;
        crt.offsetMax = Vector2.zero;

        cardTitle = MakeText(cardGo.transform, "CardTitle", 96f,
                             new Vector2(0.5f, 0.5f), new Vector2(0f, 40f),
                             TextAlignmentOptions.Center, new Vector2(1600f, 160f));
        cardSubtitle = MakeText(cardGo.transform, "CardSubtitle", 40f,
                                new Vector2(0.5f, 0.5f), new Vector2(0f, -60f),
                                TextAlignmentOptions.Center, new Vector2(1600f, 100f));
        cardSubtitle.color = new Color(0.8f, 0.88f, 1f);
    }

    private static TMP_Text MakeText(Transform parent, string name, float size,
                                     Vector2 anchor, Vector2 pos,
                                     TextAlignmentOptions align, Vector2 dimensions)
    {
        GameObject go = new GameObject(name, typeof(RectTransform));
        go.transform.SetParent(parent, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        text.fontSize = size;
        text.alignment = align;
        text.color = Color.white;

        // Outline so the card stays legible over Bun's art whatever colour it
        // turns out to be.
        text.fontStyle = FontStyles.Bold;

        RectTransform rt = text.rectTransform;
        rt.anchorMin = anchor;
        rt.anchorMax = anchor;
        rt.pivot = anchor;
        rt.anchoredPosition = pos;
        rt.sizeDelta = dimensions;

        return text;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null)
        {
            corner.text = string.Empty;
            cardGroup.alpha = 0f;
            return;
        }

        int stage = gm.LevelIndex;
        corner.text = $"STAGE {stage}/{GameSession.LevelCount}   {gm.LevelTitle}";

        // Hide the whole banner once the run ends so it never overlaps the
        // result screen's text block.
        if (gm.IsGameOver)
        {
            corner.text = string.Empty;
            cardGroup.alpha = 0f;
            return;
        }

        if (cardTimer <= 0f)
        {
            if (cardGroup.alpha != 0f) cardGroup.alpha = 0f;
            return;
        }

        cardTitle.text = $"STAGE {stage}   {gm.LevelTitle}";
        cardSubtitle.text = gm.LevelSubtitle;

        // unscaledDeltaTime, so pausing on the first second of a stage does not
        // freeze the card on screen.
        cardTimer -= Time.unscaledDeltaTime;
        cardGroup.alpha = Mathf.Clamp01(cardTimer / FadeSeconds);
    }
}
