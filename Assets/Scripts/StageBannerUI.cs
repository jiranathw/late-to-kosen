using UnityEngine;
using UnityEngine.SceneManagement;
using TMPro;

// Clean, cinematic stage intro title card:
// Displays "STAGE 1: LATE TO KOSEN" or "STAGE 2: INSIDE THE KOSEN" boldly in the center.
// Features clean, punchy retro typography with thick black stroke outlines (no background box).
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
        corner = MakeText(canvasGo.transform, "StageLabel", 32f,
                          new Vector2(0.5f, 1f), new Vector2(0f, -28f),
                          TextAlignmentOptions.Top, new Vector2(1000f, 48f),
                          new Color(1f, 0.95f, 0.40f, 1f), 0.35f, new Color32(0, 0, 0, 255));

        // Center Stage Title Card (Pure Text with Thick Stroke Outline, No Background Box)
        GameObject cardGo = new GameObject("TitleCard", typeof(RectTransform));
        cardGo.transform.SetParent(canvasGo.transform, false);
        cardGroup = cardGo.AddComponent<CanvasGroup>();
        RectTransform crt = (RectTransform)cardGo.transform;
        crt.anchorMin = Vector2.zero;
        crt.anchorMax = Vector2.one;
        crt.offsetMin = Vector2.zero;
        crt.offsetMax = Vector2.zero;

        // Bold Retro Title: Bright Yellow with Heavy Black Stroke
        cardTitle = MakeText(cardGo.transform, "CardTitle", 88f,
                             new Vector2(0.5f, 0.5f), new Vector2(0f, 32f),
                             TextAlignmentOptions.Center, new Vector2(1800f, 130f),
                             new Color(1f, 0.90f, 0.20f, 1f), 0.38f, new Color32(0, 0, 0, 255));

        // Subtitle: Pure White with Crisp Black Stroke
        cardSubtitle = MakeText(cardGo.transform, "CardSubtitle", 40f,
                                new Vector2(0.5f, 0.5f), new Vector2(0f, -48f),
                                TextAlignmentOptions.Center, new Vector2(1800f, 90f),
                                Color.white, 0.32f, new Color32(0, 0, 0, 255));
    }

    private static TMP_Text MakeText(Transform parent, string name, float size,
                                     Vector2 anchor, Vector2 pos,
                                     TextAlignmentOptions align, Vector2 dimensions,
                                     Color textColor, float outlineWidth = 0.35f, Color32? outlineColor = null)
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

        // Ensure stroke outline shader keywords are applied
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
