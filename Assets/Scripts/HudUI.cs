using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Lives (pixel hearts), score, and bike readout.
// Hides during stage intro card so the opening scene and player character remain completely clean.
// Features big retro heart icons (Full red heart -> Empty black frame upon death) and thick stroked text.
public class HudUI : MonoBehaviour
{
    private const int MaxLifeIcons = 10;

    private static HudUI instance;

    private CanvasGroup hudGroup;
    private TMP_Text scoreText;
    private TMP_Text bikeText;
    private readonly Image[] lifeIcons = new Image[MaxLifeIcons];
    private PlayerController player;

    private Sprite heartFullSprite;
    private Sprite heartEmptySprite;

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
        LoadHeartSprites();
        Build();
    }

    private void LoadHeartSprites()
    {
        heartFullSprite = Resources.Load<Sprite>("Sprites/heart_full");
        heartEmptySprite = Resources.Load<Sprite>("Sprites/heart_empty");

        if (heartFullSprite == null || heartEmptySprite == null)
        {
            Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
            foreach (var s in all)
            {
                if (s == null) continue;
                if (s.name == "heart_full" && heartFullSprite == null) heartFullSprite = s;
                else if (s.name == "heart_empty" && heartEmptySprite == null) heartEmptySprite = s;
            }
        }
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

        // Big Pixel Hearts for Lives: top-left (size 66x66, close together)
        for (int i = 0; i < MaxLifeIcons; i++)
        {
            GameObject go = new GameObject($"Life{i}");
            go.transform.SetParent(canvasGo.transform, false);

            Image img = go.AddComponent<Image>();
            if (heartFullSprite != null) img.sprite = heartFullSprite;
            img.color = Color.white;

            RectTransform rt = img.rectTransform;
            rt.anchorMin = new Vector2(0f, 1f);
            rt.anchorMax = new Vector2(0f, 1f);
            rt.pivot = new Vector2(0f, 1f);
            rt.anchoredPosition = new Vector2(28f + i * 48f, -94f);
            rt.sizeDelta = new Vector2(66f, 66f);

            lifeIcons[i] = img;
            go.SetActive(false);
        }

        // Bike status
        bikeText = MakeText(canvasGo.transform, "Bike", 30f,
                            new Vector2(0f, 1f), new Vector2(30f, -160f),
                            TextAlignmentOptions.TopLeft, new Vector2(560f, 44f),
                            new Color(0.55f, 0.95f, 0.20f, 1f), 0.35f, new Color32(0, 0, 0, 255));
        bikeText.gameObject.SetActive(false);

        // Score: top-right with bold dark stroke outline
        scoreText = MakeText(canvasGo.transform, "Score", 40f,
                             new Vector2(1f, 1f), new Vector2(-30f, -88f),
                             TextAlignmentOptions.TopRight, new Vector2(600f, 100f),
                             new Color(1f, 0.95f, 0.40f, 1f), 0.35f, new Color32(0, 0, 0, 255));
    }

    private static TMP_Text MakeText(Transform parent, string name, float size,
                                     Vector2 anchor, Vector2 pos,
                                     TextAlignmentOptions align, Vector2 dimensions,
                                     Color textColor, float outlineWidth = 0.35f, Color32? outlineColor = null)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(parent, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        text.fontSize = size;
        text.alignment = align;
        text.color = textColor;
        text.fontStyle = FontStyles.Bold;
        text.outlineWidth = outlineWidth;
        text.outlineColor = outlineColor ?? new Color32(0, 0, 0, 255);

        if (text.fontMaterial != null)
        {
            text.fontMaterial.EnableKeyword(ShaderUtilities.Keyword_Outline);
            text.fontMaterial.SetColor(ShaderUtilities.ID_OutlineColor, outlineColor ?? new Color32(0, 0, 0, 255));
            text.fontMaterial.SetFloat(ShaderUtilities.ID_OutlineWidth, outlineWidth);
        }

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

        if (heartFullSprite == null || heartEmptySprite == null)
        {
            LoadHeartSprites();
        }

        int total = Mathf.Clamp(gm.StartingLives, 0, MaxLifeIcons);
        int left = Mathf.Clamp(gm.Lives, 0, total);
        for (int i = 0; i < MaxLifeIcons; i++)
        {
            bool used = i < total;
            if (lifeIcons[i].gameObject.activeSelf != used) lifeIcons[i].gameObject.SetActive(used);
            if (used)
            {
                bool hasLife = i < left;
                if (hasLife)
                {
                    if (heartFullSprite != null) lifeIcons[i].sprite = heartFullSprite;
                    lifeIcons[i].color = Color.white;
                }
                else
                {
                    // Empty heart: hollow frame with red removed
                    if (heartEmptySprite != null) lifeIcons[i].sprite = heartEmptySprite;
                    lifeIcons[i].color = Color.white;
                }
            }
        }

        scoreText.text = $"Score: {gm.Score}\nTraps: {gm.TrapsSurvived}/{gm.TrapTotal}";

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag("Player");
            if (p != null) player = p.GetComponent<PlayerController>();
        }

        bool riding = player != null && player.IsRiding;
        if (bikeText.gameObject.activeSelf != riding) bikeText.gameObject.SetActive(riding);
        if (riding) bikeText.text = "ON ANYWHEEL BIKE - park at a rack to finish";
    }
}
