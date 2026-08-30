using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using TMPro;

// Clean, cinematic stage intro title card:
// Displays "STAGE 1: LATE TO KOSEN" or "STAGE 2: INSIDE THE KOSEN" boldly in the center.
// Uses a dark retro plaque with crisp outline to ensure high contrast against any background.
// While displaying, hides all other HUD/corner UI for a clean camera view, and locks player/timer.
// Once the intro fades out, gameplay and the stage timer begin!
public class StageBannerUI : MonoBehaviour
{
    private const float FadeSeconds = 0.5f;

    private static StageBannerUI instance;

    private TMP_Text corner;
    private TMP_Text cardTitle;
    private TMP_Text cardSubtitle;
    private CanvasGroup cardGroup;

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
    }

    private void Build()
    {
        GameObject canvasGo = new GameObject("StageBannerCanvas", typeof(RectTransform));
        canvasGo.transform.SetParent(transform, false);

        Canvas canvas = canvasGo.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 60; // above the HUD, below the pause and result screens

        UnityEngine.UI.CanvasScaler scaler = canvasGo.AddComponent<UnityEngine.UI.CanvasScaler>();
        scaler.uiScaleMode = UnityEngine.UI.CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920f, 1080f);
        scaler.matchWidthOrHeight = 0.5f;

        CanvasGroup rootGroup = canvasGo.AddComponent<CanvasGroup>();
        rootGroup.interactable = false;
        rootGroup.blocksRaycasts = false;

        // Subtle corner label that only appears AFTER the intro finishes
        corner = MakeText(canvasGo.transform, "StageLabel", 28f,
                          new Vector2(0.5f, 1f), new Vector2(0f, -28f),
                          TextAlignmentOptions.Top, new Vector2(900f, 44f),
                          Color.white, 0.2f, new Color32(0, 0, 0, 220));

        // Center Stage Title Card
        GameObject cardGo = new GameObject("TitleCard", typeof(RectTransform));
        cardGo.transform.SetParent(canvasGo.transform, false);
        cardGroup = cardGo.AddComponent<CanvasGroup>();
        RectTransform crt = (RectTransform)cardGo.transform;
        crt.anchorMin = Vector2.zero;
        crt.anchorMax = Vector2.one;
        crt.offsetMin = Vector2.zero;
        crt.offsetMax = Vector2.zero;

        // Retro Dark Plaque Background with Golden Pixel Border
        GameObject plaqueBorder = new GameObject("PlaqueBorder", typeof(RectTransform));
        plaqueBorder.transform.SetParent(cardGo.transform, false);
        Image borderImg = plaqueBorder.AddComponent<Image>();
        borderImg.color = new Color(1f, 0.86f, 0.20f, 0.95f); // Golden yellow pixel border
        RectTransform brt = (RectTransform)plaqueBorder.transform;
        brt.anchorMin = new Vector2(0.5f, 0.5f);
        brt.anchorMax = new Vector2(0.5f, 0.5f);
        brt.pivot = new Vector2(0.5f, 0.5f);
        brt.anchoredPosition = Vector2.zero;
        brt.sizeDelta = new Vector2(1300f, 220f);

        GameObject plaqueInner = new GameObject("PlaqueInner", typeof(RectTransform));
        plaqueInner.transform.SetParent(plaqueBorder.transform, false);
        Image innerImg = plaqueInner.AddComponent<Image>();
        innerImg.color = new Color(0.04f, 0.07f, 0.14f, 0.92f); // Deep dark slate background
        RectTransform irt = (RectTransform)plaqueInner.transform;
        irt.anchorMin = Vector2.zero;
        irt.anchorMax = Vector2.one;
        irt.offsetMin = new Vector2(5f, 5f);
        irt.offsetMax = new Vector2(-5f, -5f);

        // Bold Retro Title with Dark Pixel Outline
        cardTitle = MakeText(cardGo.transform, "CardTitle", 76f,
                             new Vector2(0.5f, 0.5f), new Vector2(0f, 32f),
                             TextAlignmentOptions.Center, new Vector2(1250f, 110f),
                             new Color(1f, 0.93f, 0.25f, 1f), 0.35f, new Color32(10, 15, 30, 255));

        // Crisp Subtitle with Dark Pixel Outline
        cardSubtitle = MakeText(cardGo.transform, "CardSubtitle", 34f,
                                new Vector2(0.5f, 0.5f), new Vector2(0f, -40f),
                                TextAlignmentOptions.Center, new Vector2(1250f, 70f),
                                new Color(0.92f, 0.96f, 1f, 1f), 0.30f, new Color32(10, 15, 30, 255));
    }

    private static TMP_Text MakeText(Transform parent, string name, float size,
                                     Vector2 anchor, Vector2 pos,
                                     TextAlignmentOptions align, Vector2 dimensions,
                                     Color textColor, float outlineWidth = 0.25f, Color32? outlineColor = null)
    {
        GameObject go = new GameObject(name, typeof(RectTransform));
        go.transform.SetParent(parent, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        text.fontSize = size;
        text.alignment = align;
        text.color = textColor;
        text.fontStyle = FontStyles.Bold;
        text.outlineWidth = outlineWidth;
        text.outlineColor = outlineColor ?? new Color32(0, 0, 0, 255);

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

        // Hide banner during Game Over
        if (gm.IsGameOver)
        {
            corner.text = string.Empty;
            cardGroup.alpha = 0f;
            return;
        }

        // During Stage Intro
        if (gm.IsIntroActive)
        {
            corner.text = string.Empty; // Keep screen clean without corner text
            cardTitle.text = $"STAGE {stage}: {gm.LevelTitle}";
            cardSubtitle.text = gm.LevelSubtitle;

            // Fade out in the final 0.5s of the intro
            if (gm.IntroRemaining <= FadeSeconds)
            {
                cardGroup.alpha = Mathf.Clamp01(gm.IntroRemaining / FadeSeconds);
            }
            else
            {
                cardGroup.alpha = 1f;
            }
            return;
        }

        // After Stage Intro completes:
        cardGroup.alpha = 0f;
        corner.text = $"STAGE {stage}/{GameSession.LevelCount}   {gm.LevelTitle}";
    }
}
