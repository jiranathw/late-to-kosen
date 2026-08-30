using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using TMPro;

// Main Menu Title Screen for "Late to KOSEN"
// Features:
// 1. PLAY (Loads Level1)
// 2. CHANGE CHARACTER (Placeholder for future character select)
// 3. QUIT (Exits game)
// Supports mouse clicking and Up/Down/Enter keyboard navigation.
public class MainMenuUI : MonoBehaviour
{
    private static MainMenuUI instance;

    private CanvasGroup menuGroup;
    private Button[] buttons;
    private TMP_Text[] buttonTexts;
    private string[] originalButtonLabels = { "PLAY", "CHANGE CHARACTER", "QUIT" };
    private int selectedIndex = 0;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (SceneManager.GetActiveScene().name != "MainMenu") return;

        if (instance != null) return;

        GameObject host = new GameObject("~MainMenuUI");
        instance = host.AddComponent<MainMenuUI>();
    }

    private void Awake()
    {
        if (SceneManager.GetActiveScene().name != "MainMenu")
        {
            Destroy(gameObject);
            return;
        }

        instance = this;
        EnsureEventSystem();
        BuildUI();
    }

    private void EnsureEventSystem()
    {
        if (FindFirstObjectByType<EventSystem>() == null)
        {
            GameObject esGo = new GameObject("EventSystem");
            esGo.AddComponent<EventSystem>();
            esGo.AddComponent<StandaloneInputModule>();
        }
    }

    private void BuildUI()
    {
        GameObject canvasGo = new GameObject("MainMenuCanvas", typeof(RectTransform));
        canvasGo.transform.SetParent(transform, false);

        Canvas canvas = canvasGo.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 100;

        CanvasScaler scaler = canvasGo.AddComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920f, 1080f);
        scaler.matchWidthOrHeight = 0.5f;

        canvasGo.AddComponent<GraphicRaycaster>();

        menuGroup = canvasGo.AddComponent<CanvasGroup>();

        // 1. Title: LATE TO KOSEN
        TMP_Text titleText = MakeText(canvasGo.transform, "TitleText", 96f,
                                      new Vector2(0.5f, 0.5f), new Vector2(0f, 260f),
                                      TextAlignmentOptions.Center, new Vector2(1600f, 130f),
                                      new Color(1f, 0.90f, 0.20f, 1f), 0.38f, new Color32(0, 0, 0, 255));
        titleText.text = "LATE TO KOSEN";

        // 2. Subtitle
        TMP_Text subtitleText = MakeText(canvasGo.transform, "SubtitleText", 36f,
                                         new Vector2(0.5f, 0.5f), new Vector2(0f, 190f),
                                         TextAlignmentOptions.Center, new Vector2(1600f, 60f),
                                         Color.white, 0.30f, new Color32(0, 0, 0, 255));
        subtitleText.text = "AN 8-BIT MORNING SPRINT TO CLASS";

        // 3. Buttons Container (PLAY, CHANGE CHARACTER, QUIT)
        buttons = new Button[3];
        buttonTexts = new TMP_Text[3];

        float startY = 60f;
        float spacingY = 100f;

        for (int i = 0; i < 3; i++)
        {
            int index = i;
            GameObject btnGo = new GameObject($"Btn_{originalButtonLabels[i]}", typeof(RectTransform));
            btnGo.transform.SetParent(canvasGo.transform, false);

            Image btnImg = btnGo.AddComponent<Image>();
            btnImg.color = new Color(0.08f, 0.12f, 0.22f, 0.92f); // Deep dark retro navy

            Button btn = btnGo.AddComponent<Button>();
            ColorBlock cb = btn.colors;
            cb.normalColor = new Color(0.08f, 0.12f, 0.22f, 0.92f);
            cb.highlightedColor = new Color(0.18f, 0.35f, 0.65f, 1f);
            cb.pressedColor = new Color(0.35f, 0.75f, 0.95f, 1f);
            cb.selectedColor = new Color(0.18f, 0.35f, 0.65f, 1f);
            btn.colors = cb;

            RectTransform rt = btn.GetComponent<RectTransform>();
            rt.anchorMin = new Vector2(0.5f, 0.5f);
            rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0.5f, 0.5f);
            rt.anchoredPosition = new Vector2(0f, startY - i * spacingY);
            rt.sizeDelta = new Vector2(500f, 76f);

            // Button Border
            GameObject borderGo = new GameObject("Border", typeof(RectTransform));
            borderGo.transform.SetParent(btnGo.transform, false);
            Image borderImg = borderGo.AddComponent<Image>();
            borderImg.color = new Color(1f, 0.85f, 0.25f, 0.85f);
            borderImg.raycastTarget = false;
            RectTransform brt = (RectTransform)borderGo.transform;
            brt.anchorMin = Vector2.zero;
            brt.anchorMax = Vector2.one;
            brt.offsetMin = new Vector2(-3f, -3f);
            brt.offsetMax = new Vector2(3f, 3f);
            borderGo.transform.SetAsFirstSibling();

            // Button Label Text
            TMP_Text btnText = MakeText(btnGo.transform, "Label", 36f,
                                        new Vector2(0.5f, 0.5f), Vector2.zero,
                                        TextAlignmentOptions.Center, new Vector2(480f, 60f),
                                        Color.white, 0.35f, new Color32(0, 0, 0, 255));
            btnText.text = originalButtonLabels[i];

            buttons[i] = btn;
            buttonTexts[i] = btnText;

            // Click Handlers
            btn.onClick.AddListener(() => OnButtonClicked(index));

            // Add Event Trigger for hover sound and selection
            EventTrigger trigger = btnGo.AddComponent<EventTrigger>();
            EventTrigger.Entry entry = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
            entry.callback.AddListener((data) => { SetSelected(index); });
            trigger.triggers.Add(entry);
        }

        // 4. Footer info
        TMP_Text footerText = MakeText(canvasGo.transform, "FooterText", 24f,
                                       new Vector2(0.5f, 0f), new Vector2(0f, 36f),
                                       TextAlignmentOptions.Center, new Vector2(1200f, 40f),
                                       new Color(1f, 1f, 1f, 0.65f), 0.25f, new Color32(0, 0, 0, 255));
        footerText.text = "PROGRAMMING 7  |  TEAM SIXSEVEN  |  KOSEN-KMITL";

        UpdateHighlight();
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
        // Keyboard Navigation (W/S or Up/Down, Space/Enter to confirm)
        if (Input.GetKeyDown(KeyCode.UpArrow) || Input.GetKeyDown(KeyCode.W))
        {
            selectedIndex = (selectedIndex - 1 + buttons.Length) % buttons.Length;
            AudioManager.Instance?.PlayJumpSFX();
            UpdateHighlight();
        }
        else if (Input.GetKeyDown(KeyCode.DownArrow) || Input.GetKeyDown(KeyCode.S))
        {
            selectedIndex = (selectedIndex + 1) % buttons.Length;
            AudioManager.Instance?.PlayJumpSFX();
            UpdateHighlight();
        }
        else if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.Space))
        {
            OnButtonClicked(selectedIndex);
        }
    }

    private void SetSelected(int index)
    {
        if (selectedIndex != index)
        {
            selectedIndex = index;
            AudioManager.Instance?.PlayJumpSFX();
            UpdateHighlight();
        }
    }

    private void UpdateHighlight()
    {
        for (int i = 0; i < buttons.Length; i++)
        {
            if (i == selectedIndex)
            {
                buttonTexts[i].color = new Color(1f, 0.95f, 0.35f, 1f); // Vibrant Yellow
                buttonTexts[i].text = $">  {originalButtonLabels[i]}  <";
                buttons[i].Select();
            }
            else
            {
                buttonTexts[i].color = Color.white;
                buttonTexts[i].text = originalButtonLabels[i];
            }
        }
    }

    private void OnButtonClicked(int index)
    {
        switch (index)
        {
            case 0: // PLAY
                AudioManager.Instance?.PlayJumpSFX();
                SceneManager.LoadScene("Level1");
                break;

            case 1: // CHANGE CHARACTER
                AudioManager.Instance?.PlayJumpSFX();
                Debug.Log("Change Character clicked (Placeholder)");
                break;

            case 2: // QUIT
                AudioManager.Instance?.PlayDeathSFX();
#if UNITY_EDITOR
                UnityEditor.EditorApplication.isPlaying = false;
#else
                Application.Quit();
#endif
                break;
        }
    }
}
