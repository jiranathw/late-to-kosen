using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Lives, score, and whether you are stuck on a rented bicycle.
// Hides during stage intro card so the opening scene and player character remain completely clean.
public class HudUI : MonoBehaviour
{
    private const int MaxLifeIcons = 10;

    private static HudUI instance;

    private CanvasGroup hudGroup;
    private TMP_Text scoreText;
    private TMP_Text bikeText;
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

        hudGroup = canvasGo.AddComponent<CanvasGroup>();
        hudGroup.interactable = false;
        hudGroup.blocksRaycasts = false;
        hudGroup.alpha = 0f;

        // Lives: top-left
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

        // Bike status
        bikeText = MakeText(canvasGo.transform, "Bike", 26f,
                            new Vector2(0f, 1f), new Vector2(32f, -140f),
                            TextAlignmentOptions.TopLeft, new Vector2(560f, 40f));
        bikeText.color = new Color(0.35f, 0.85f, 1f);
        bikeText.gameObject.SetActive(false);

        // Score: top-right
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
        if (gm == null || gm.IsGameOver || gm.IsIntroActive)
        {
            if (hudGroup != null) hudGroup.alpha = 0f;
            return;
        }

        if (hudGroup != null) hudGroup.alpha = 1f;

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

        bool riding = player != null && player.IsRiding;
        if (bikeText.gameObject.activeSelf != riding) bikeText.gameObject.SetActive(riding);
        if (riding) bikeText.text = "ON A BIKE - find a rack to park";
    }
}
