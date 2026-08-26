using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Lives, score and the sprint bar.
//
// Built at runtime for the same reason as ResultUI and PauseMenu: no scene
// wiring means nothing to accidentally unassign, and it shows up in every
// scene in the build automatically. The timer and death counter still live on
// the scene's own Canvas - this sits underneath them.
//
// Lives are drawn as plain UI Images, not heart characters, because the
// default TextMeshPro font (LiberationSans) has no heart glyph and would
// render empty boxes. Same reason the rest of the UI is ASCII.
public class HudUI : MonoBehaviour
{
    private const int MaxLifeIcons = 10;

    private static HudUI instance;

    private TMP_Text scoreText;
    private Image staminaFill;
    private TMP_Text bikeText;
    private RectTransform staminaRoot;
    private readonly Image[] lifeIcons = new Image[MaxLifeIcons];
    private PlayerController player;

    private static readonly Color LifeFull  = new Color(1f, 0.30f, 0.38f, 1f);
    private static readonly Color LifeEmpty = new Color(1f, 1f, 1f, 0.18f);

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (instance != null) return;

        GameObject host = new GameObject("~HudUI");
        DontDestroyOnLoad(host);
        instance = host.AddComponent<HudUI>();
    }

    private void Awake()
    {
        instance = this;
        Build();
    }

    private void Build()
    {
        GameObject canvasGo = new GameObject("HudCanvas");
        canvasGo.transform.SetParent(transform, false);

        Canvas canvas = canvasGo.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 50;

        CanvasScaler scaler = canvasGo.AddComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920f, 1080f);
        scaler.matchWidthOrHeight = 0.5f;

        CanvasGroup group = canvasGo.AddComponent<CanvasGroup>();
        group.interactable = false;
        group.blocksRaycasts = false;

        // Lives: a row of blocks, top-left, pushed clear of the scene
        // Canvas's TimerText which sits at (30, -30) and is 50 tall.
        // Score likewise clears DeathCountText at (-30, -30).
        for (int i = 0; i < MaxLifeIcons; i++)
        {
            GameObject go = new GameObject($"Life{i}");
            go.transform.SetParent(canvasGo.transform, false);

            Image img = go.AddComponent<Image>();
            img.color = LifeFull;

            RectTransform rt = img.rectTransform;
            rt.anchorMin = new Vector2(0f, 1f);
            rt.anchorMax = new Vector2(0f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.anchoredPosition = new Vector2(32f + i * 46f, -94f);
            rt.sizeDelta = new Vector2(36f, 36f);

            lifeIcons[i] = img;
            go.SetActive(false);
        }

        // Sprint bar, just under the lives
        GameObject barBg = new GameObject("SprintBar");
        barBg.transform.SetParent(canvasGo.transform, false);
        Image bg = barBg.AddComponent<Image>();
        bg.color = new Color(0f, 0f, 0f, 0.45f);
        staminaRoot = bg.rectTransform;
        staminaRoot.anchorMin = new Vector2(0f, 1f);
        staminaRoot.anchorMax = new Vector2(0f, 1f);
        staminaRoot.pivot = new Vector2(0f, 1f);
        staminaRoot.anchoredPosition = new Vector2(32f, -142f);
        staminaRoot.sizeDelta = new Vector2(220f, 16f);

        GameObject fillGo = new GameObject("Fill");
        fillGo.transform.SetParent(barBg.transform, false);
        staminaFill = fillGo.AddComponent<Image>();
        staminaFill.color = new Color(0.4f, 0.85f, 1f, 0.95f);
        staminaFill.type = Image.Type.Filled;
        staminaFill.fillMethod = Image.FillMethod.Horizontal;
        staminaFill.fillOrigin = (int)Image.OriginHorizontal.Left;
        RectTransform frt = staminaFill.rectTransform;
        frt.anchorMin = Vector2.zero;
        frt.anchorMax = Vector2.one;
        frt.pivot = new Vector2(0.5f, 0.5f);
        frt.offsetMin = new Vector2(2f, 2f);
        frt.offsetMax = new Vector2(-2f, -2f);

        MakeText(canvasGo.transform, "SprintLabel", 22f,
                 new Vector2(0f, 1f), new Vector2(258f, -140f),
                 TextAlignmentOptions.TopLeft, new Vector2(300f, 30f))
            .text = "SHIFT";

        // Bicycle power-up timer, sits under the sprint bar and hides itself
        // when the player isn't riding.
        bikeText = MakeText(canvasGo.transform, "Bike", 26f,
                            new Vector2(0f, 1f), new Vector2(32f, -166f),
                            TextAlignmentOptions.TopLeft, new Vector2(400f, 40f));
        bikeText.color = new Color(0.35f, 0.85f, 1f);
        bikeText.gameObject.SetActive(false);

        // Score, top-right under the scene's death counter
        scoreText = MakeText(canvasGo.transform, "Score", 38f,
                             new Vector2(1f, 1f), new Vector2(-30f, -92f),
                             TextAlignmentOptions.TopRight, new Vector2(600f, 100f));
    }

    private static TMP_Text MakeText(Transform parent, string name, float size,
                                     Vector2 anchor, Vector2 pos,
                                     TextAlignmentOptions align, Vector2 dimensions)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(parent, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        text.fontSize = size;
        text.alignment = align;
        text.color = Color.white;

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
        if (gm == null) return;

        int total = Mathf.Clamp(gm.StartingLives, 0, MaxLifeIcons);
        int left = Mathf.Clamp(gm.Lives, 0, total);
        for (int i = 0; i < MaxLifeIcons; i++)
        {
            bool used = i < total;
            if (lifeIcons[i].gameObject.activeSelf != used) lifeIcons[i].gameObject.SetActive(used);
            if (used) lifeIcons[i].color = i < left ? LifeFull : LifeEmpty;
        }

        scoreText.text = $"Score: {gm.Score}\nTraps: {gm.TrapsSurvived}/{gm.TrapTotal}";

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag("Player");
            if (p != null) player = p.GetComponent<PlayerController>();
        }

        if (player != null)
        {
            if (!staminaRoot.gameObject.activeSelf) staminaRoot.gameObject.SetActive(true);
            staminaFill.fillAmount = player.Stamina01;
            staminaFill.color = player.IsSprinting
                ? new Color(1f, 0.85f, 0.3f, 0.95f)
                : new Color(0.4f, 0.85f, 1f, 0.95f);

            bool riding = player.HasBike;
            if (bikeText.gameObject.activeSelf != riding) bikeText.gameObject.SetActive(riding);
            if (riding) bikeText.text = $"BIKE  {player.BikeSecondsLeft:0.0}s";
        }
        else if (staminaRoot.gameObject.activeSelf)
        {
            staminaRoot.gameObject.SetActive(false);
            bikeText.gameObject.SetActive(false);
        }
    }
}
