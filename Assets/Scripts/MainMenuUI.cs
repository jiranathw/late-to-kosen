using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using UnityEngine.EventSystems;
using TMPro;

// Main Menu Title Screen & Character Selection for "Late to KOSEN"
// Supports:
// 1. PLAY (Loads Level1)
// 2. CHANGE CHARACTER (3 selectable uniforms: Formal White Tie, PE Sport Orange, Workshop Dark Navy)
// 3. QUIT (Exits game)
public class MainMenuUI : MonoBehaviour
{
    private static MainMenuUI instance;

    private CanvasGroup mainCanvasGroup;
    private GameObject mainMenuPanel;
    private GameObject charSelectPanel;

    // Main Menu Buttons
    private Button[] mainButtons;
    private TMP_Text[] mainButtonTexts;
    private readonly string[] mainButtonLabels = { "PLAY", "CHANGE CHARACTER", "QUIT" };
    private int mainSelectedIndex = 0;

    // Character Select Cards
    private GameObject[] charCards = new GameObject[3];
    private Image[] charPreviews = new Image[3];
    private TMP_Text[] charStatusTexts = new TMP_Text[3];
    private Image[] cardBorders = new Image[3];
    private int selectedCharIndex = 0;
    private int currentEquippedChar = 0;

    private readonly string[] charTitles = { "FORMAL UNIFORM", "PE SPORT", "SHOP WORK" };
    private readonly string[] charDescriptions = {
        "White shirt with Orange/Blue striped necktie and navy slacks.",
        "Bright Orange polo with blue collar and black sweatpants.",
        "Dark Navy workshop shirt with purple chest stripe."
    };

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
        currentEquippedChar = PlayerPrefs.GetInt("SelectedCharacter", 0);
        selectedCharIndex = currentEquippedChar;

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
        mainCanvasGroup = canvasGo.AddComponent<CanvasGroup>();

        // Build Panels
        BuildMainMenuPanel(canvasGo.transform);
        BuildCharSelectPanel(canvasGo.transform);

        ShowMainMenu();
    }

    // ========================================================================
    // 1. MAIN MENU PANEL
    // ========================================================================
    private void BuildMainMenuPanel(Transform parent)
    {
        mainMenuPanel = new GameObject("MainMenuPanel", typeof(RectTransform));
        mainMenuPanel.transform.SetParent(parent, false);
        RectTransform rt = (RectTransform)mainMenuPanel.transform;
        rt.anchorMin = Vector2.zero;
        rt.anchorMax = Vector2.one;
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;

        // Title: LATE TO KOSEN
        TMP_Text titleText = MakeText(mainMenuPanel.transform, "TitleText", 96f,
                                      new Vector2(0.5f, 0.5f), new Vector2(0f, 260f),
                                      TextAlignmentOptions.Center, new Vector2(1600f, 130f),
                                      new Color(1f, 0.90f, 0.20f, 1f), 0.38f, new Color32(0, 0, 0, 255));
        titleText.text = "LATE TO KOSEN";

        // Subtitle
        TMP_Text subtitleText = MakeText(mainMenuPanel.transform, "SubtitleText", 36f,
                                         new Vector2(0.5f, 0.5f), new Vector2(0f, 190f),
                                         TextAlignmentOptions.Center, new Vector2(1600f, 60f),
                                         Color.white, 0.30f, new Color32(0, 0, 0, 255));
        subtitleText.text = "AN 8-BIT MORNING SPRINT TO CLASS";

        // 3 Buttons (PLAY, CHANGE CHARACTER, QUIT)
        mainButtons = new Button[3];
        mainButtonTexts = new TMP_Text[3];

        float startY = 60f;
        float spacingY = 100f;

        for (int i = 0; i < 3; i++)
        {
            int index = i;
            GameObject btnGo = new GameObject($"Btn_{mainButtonLabels[i]}", typeof(RectTransform));
            btnGo.transform.SetParent(mainMenuPanel.transform, false);

            Image btnImg = btnGo.AddComponent<Image>();
            btnImg.color = new Color(0.08f, 0.12f, 0.22f, 0.92f);

            Button btn = btnGo.AddComponent<Button>();
            RectTransform brt = btn.GetComponent<RectTransform>();
            brt.anchorMin = new Vector2(0.5f, 0.5f);
            brt.anchorMax = new Vector2(0.5f, 0.5f);
            brt.pivot = new Vector2(0.5f, 0.5f);
            brt.anchoredPosition = new Vector2(0f, startY - i * spacingY);
            brt.sizeDelta = new Vector2(520f, 76f);

            // Border
            GameObject borderGo = new GameObject("Border", typeof(RectTransform));
            borderGo.transform.SetParent(btnGo.transform, false);
            Image borderImg = borderGo.AddComponent<Image>();
            borderImg.color = new Color(1f, 0.85f, 0.25f, 0.85f);
            borderImg.raycastTarget = false;
            RectTransform borderRt = (RectTransform)borderGo.transform;
            borderRt.anchorMin = Vector2.zero;
            borderRt.anchorMax = Vector2.one;
            borderRt.offsetMin = new Vector2(-3f, -3f);
            borderRt.offsetMax = new Vector2(3f, 3f);
            borderGo.transform.SetAsFirstSibling();

            // Label
            TMP_Text btnText = MakeText(btnGo.transform, "Label", 36f,
                                        new Vector2(0.5f, 0.5f), Vector2.zero,
                                        TextAlignmentOptions.Center, new Vector2(500f, 60f),
                                        Color.white, 0.35f, new Color32(0, 0, 0, 255));
            btnText.text = mainButtonLabels[i];

            mainButtons[i] = btn;
            mainButtonTexts[i] = btnText;

            btn.onClick.AddListener(() => OnMainButtonClicked(index));

            EventTrigger trigger = btnGo.AddComponent<EventTrigger>();
            EventTrigger.Entry entry = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
            entry.callback.AddListener((data) => { SetMainSelected(index); });
            trigger.triggers.Add(entry);
        }

        // Footer
        TMP_Text footerText = MakeText(mainMenuPanel.transform, "FooterText", 24f,
                                       new Vector2(0.5f, 0f), new Vector2(0f, 36f),
                                       TextAlignmentOptions.Center, new Vector2(1200f, 40f),
                                       new Color(1f, 1f, 1f, 0.65f), 0.25f, new Color32(0, 0, 0, 255));
        footerText.text = "PROGRAMMING 7  |  TEAM SIXSEVEN  |  KOSEN-KMITL";

        UpdateMainHighlight();
    }

    // ========================================================================
    // 2. CHARACTER SELECTION PANEL
    // ========================================================================
    private void BuildCharSelectPanel(Transform parent)
    {
        charSelectPanel = new GameObject("CharSelectPanel", typeof(RectTransform));
        charSelectPanel.transform.SetParent(parent, false);
        RectTransform rt = (RectTransform)charSelectPanel.transform;
        rt.anchorMin = Vector2.zero;
        rt.anchorMax = Vector2.one;
        rt.offsetMin = Vector2.zero;
        rt.offsetMax = Vector2.zero;

        // Title
        TMP_Text title = MakeText(charSelectPanel.transform, "SelectTitle", 76f,
                                  new Vector2(0.5f, 0.5f), new Vector2(0f, 340f),
                                  TextAlignmentOptions.Center, new Vector2(1600f, 100f),
                                  new Color(1f, 0.90f, 0.20f, 1f), 0.38f, new Color32(0, 0, 0, 255));
        title.text = "CHOOSE YOUR UNIFORM";

        TMP_Text subtitle = MakeText(charSelectPanel.transform, "SelectSubtitle", 30f,
                                     new Vector2(0.5f, 0.5f), new Vector2(0f, 280f),
                                     TextAlignmentOptions.Center, new Vector2(1600f, 50f),
                                     Color.white, 0.28f, new Color32(0, 0, 0, 255));
        subtitle.text = "SELECT YOUR OUTFIT FOR TODAY'S SPRINT TO CLASS";

        // 3 Character Cards (Width 400px each, Spacing 460px)
        float[] cardX = { -460f, 0f, 460f };

        for (int i = 0; i < 3; i++)
        {
            int index = i;
            GameObject card = new GameObject($"Card_{i}", typeof(RectTransform));
            card.transform.SetParent(charSelectPanel.transform, false);

            Image cardBg = card.AddComponent<Image>();
            cardBg.color = new Color(0.06f, 0.09f, 0.18f, 0.94f);

            Button cardBtn = card.AddComponent<Button>();
            RectTransform crt = card.GetComponent<RectTransform>();
            crt.anchorMin = new Vector2(0.5f, 0.5f);
            crt.anchorMax = new Vector2(0.5f, 0.5f);
            crt.pivot = new Vector2(0.5f, 0.5f);
            crt.anchoredPosition = new Vector2(cardX[i], 20f);
            crt.sizeDelta = new Vector2(400f, 440f);

            // Border
            GameObject border = new GameObject("CardBorder", typeof(RectTransform));
            border.transform.SetParent(card.transform, false);
            Image borderImg = border.AddComponent<Image>();
            borderImg.color = new Color(0.4f, 0.5f, 0.7f, 0.6f);
            borderImg.raycastTarget = false;
            RectTransform brt = (RectTransform)border.transform;
            brt.anchorMin = Vector2.zero;
            brt.anchorMax = Vector2.one;
            brt.offsetMin = new Vector2(-4f, -4f);
            brt.offsetMax = new Vector2(4f, 4f);
            border.transform.SetAsFirstSibling();
            cardBorders[i] = borderImg;

            // Character Title
            TMP_Text cTitle = MakeText(card.transform, "CardTitle", 34f,
                                       new Vector2(0.5f, 1f), new Vector2(0f, -34f),
                                       TextAlignmentOptions.Center, new Vector2(380f, 48f),
                                       new Color(1f, 0.95f, 0.40f, 1f), 0.35f, new Color32(0, 0, 0, 255));
            cTitle.text = charTitles[i];

            // Character Pixel Art Preview (Large 140x140)
            GameObject previewGo = new GameObject("Preview", typeof(RectTransform));
            previewGo.transform.SetParent(card.transform, false);
            Image prevImg = previewGo.AddComponent<Image>();
            Sprite charSprite = Resources.Load<Sprite>($"Sprites/char_{i}_idle") ?? Resources.Load<Sprite>("Sprites/player_idle");
            if (charSprite != null) prevImg.sprite = charSprite;
            prevImg.preserveAspect = true;
            RectTransform prt = (RectTransform)previewGo.transform;
            prt.anchorMin = new Vector2(0.5f, 0.5f);
            prt.anchorMax = new Vector2(0.5f, 0.5f);
            prt.pivot = new Vector2(0.5f, 0.5f);
            prt.anchoredPosition = new Vector2(0f, 30f);
            prt.sizeDelta = new Vector2(150f, 150f);
            charPreviews[i] = prevImg;

            // Character Description
            TMP_Text cDesc = MakeText(card.transform, "CardDesc", 20f,
                                      new Vector2(0.5f, 0f), new Vector2(0f, 96f),
                                      TextAlignmentOptions.Center, new Vector2(360f, 60f),
                                      new Color(0.9f, 0.92f, 0.96f, 0.9f), 0.25f, new Color32(0, 0, 0, 255));
            cDesc.text = charDescriptions[i];

            // Status Badge (EQUIPPED / SELECT)
            TMP_Text cStatus = MakeText(card.transform, "StatusBadge", 26f,
                                        new Vector2(0.5f, 0f), new Vector2(0f, 40f),
                                        TextAlignmentOptions.Center, new Vector2(340f, 40f),
                                        Color.white, 0.35f, new Color32(0, 0, 0, 255));
            charStatusTexts[i] = cStatus;

            charCards[i] = card;

            cardBtn.onClick.AddListener(() => SelectAndEquipCharacter(index));

            EventTrigger trigger = card.AddComponent<EventTrigger>();
            EventTrigger.Entry entry = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
            entry.callback.AddListener((data) => { SetCharSelected(index); });
            trigger.triggers.Add(entry);
        }

        // Back / Confirm Button
        GameObject backBtnGo = new GameObject("Btn_Back", typeof(RectTransform));
        backBtnGo.transform.SetParent(charSelectPanel.transform, false);
        Image backImg = backBtnGo.AddComponent<Image>();
        backImg.color = new Color(0.12f, 0.18f, 0.32f, 0.95f);
        Button backBtn = backBtnGo.AddComponent<Button>();
        RectTransform backRt = backBtnGo.GetComponent<RectTransform>();
        backRt.anchorMin = new Vector2(0.5f, 0.5f);
        backRt.anchorMax = new Vector2(0.5f, 0.5f);
        backRt.pivot = new Vector2(0.5f, 0.5f);
        backRt.anchoredPosition = new Vector2(0f, -280f);
        backRt.sizeDelta = new Vector2(380f, 68f);

        GameObject backBorder = new GameObject("Border", typeof(RectTransform));
        backBorder.transform.SetParent(backBtnGo.transform, false);
        Image bbImg = backBorder.AddComponent<Image>();
        bbImg.color = new Color(1f, 0.85f, 0.25f, 0.85f);
        bbImg.raycastTarget = false;
        RectTransform bbrt = (RectTransform)backBorder.transform;
        bbrt.anchorMin = Vector2.zero;
        bbrt.anchorMax = Vector2.one;
        bbrt.offsetMin = new Vector2(-3f, -3f);
        bbrt.offsetMax = new Vector2(3f, 3f);
        backBorder.transform.SetAsFirstSibling();

        TMP_Text backText = MakeText(backBtnGo.transform, "Label", 32f,
                                     new Vector2(0.5f, 0.5f), Vector2.zero,
                                     TextAlignmentOptions.Center, new Vector2(360f, 50f),
                                     Color.white, 0.35f, new Color32(0, 0, 0, 255));
        backText.text = "CONFIRM & BACK";

        backBtn.onClick.AddListener(ShowMainMenu);
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
        if (mainMenuPanel.activeSelf)
        {
            // Main Menu Navigation
            if (Input.GetKeyDown(KeyCode.UpArrow) || Input.GetKeyDown(KeyCode.W))
            {
                mainSelectedIndex = (mainSelectedIndex - 1 + mainButtons.Length) % mainButtons.Length;
                AudioManager.Instance?.PlayJumpSFX();
                UpdateMainHighlight();
            }
            else if (Input.GetKeyDown(KeyCode.DownArrow) || Input.GetKeyDown(KeyCode.S))
            {
                mainSelectedIndex = (mainSelectedIndex + 1) % mainButtons.Length;
                AudioManager.Instance?.PlayJumpSFX();
                UpdateMainHighlight();
            }
            else if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.Space))
            {
                OnMainButtonClicked(mainSelectedIndex);
            }
        }
        else if (charSelectPanel.activeSelf)
        {
            // Character Select Navigation
            if (Input.GetKeyDown(KeyCode.LeftArrow) || Input.GetKeyDown(KeyCode.A))
            {
                selectedCharIndex = (selectedCharIndex - 1 + 3) % 3;
                AudioManager.Instance?.PlayJumpSFX();
                UpdateCharSelectHighlight();
            }
            else if (Input.GetKeyDown(KeyCode.RightArrow) || Input.GetKeyDown(KeyCode.D))
            {
                selectedCharIndex = (selectedCharIndex + 1) % 3;
                AudioManager.Instance?.PlayJumpSFX();
                UpdateCharSelectHighlight();
            }
            else if (Input.GetKeyDown(KeyCode.Return) || Input.GetKeyDown(KeyCode.Space))
            {
                SelectAndEquipCharacter(selectedCharIndex);
            }
            else if (Input.GetKeyDown(KeyCode.Escape))
            {
                ShowMainMenu();
            }
        }
    }

    private void ShowMainMenu()
    {
        AudioManager.Instance?.PlayJumpSFX();
        mainMenuPanel.SetActive(true);
        charSelectPanel.SetActive(false);
        UpdateMainHighlight();
    }

    private void ShowCharSelect()
    {
        AudioManager.Instance?.PlayJumpSFX();
        mainMenuPanel.SetActive(false);
        charSelectPanel.SetActive(true);
        selectedCharIndex = currentEquippedChar;
        UpdateCharSelectHighlight();
    }

    private void SetMainSelected(int index)
    {
        if (mainSelectedIndex != index)
        {
            mainSelectedIndex = index;
            AudioManager.Instance?.PlayJumpSFX();
            UpdateMainHighlight();
        }
    }

    private void UpdateMainHighlight()
    {
        for (int i = 0; i < mainButtons.Length; i++)
        {
            if (i == mainSelectedIndex)
            {
                mainButtonTexts[i].color = new Color(1f, 0.95f, 0.35f, 1f);
                mainButtonTexts[i].text = $">  {mainButtonLabels[i]}  <";
                mainButtons[i].Select();
            }
            else
            {
                mainButtonTexts[i].color = Color.white;
                mainButtonTexts[i].text = mainButtonLabels[i];
            }
        }
    }

    private void OnMainButtonClicked(int index)
    {
        switch (index)
        {
            case 0: // PLAY
                AudioManager.Instance?.PlayJumpSFX();
                SceneManager.LoadScene("Level1");
                break;

            case 1: // CHANGE CHARACTER
                ShowCharSelect();
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

    private void SetCharSelected(int index)
    {
        if (selectedCharIndex != index)
        {
            selectedCharIndex = index;
            AudioManager.Instance?.PlayJumpSFX();
            UpdateCharSelectHighlight();
        }
    }

    private void SelectAndEquipCharacter(int index)
    {
        currentEquippedChar = index;
        selectedCharIndex = index;
        PlayerPrefs.SetInt("SelectedCharacter", index);
        PlayerPrefs.Save();
        AudioManager.Instance?.PlayStageClearSFX();
        UpdateCharSelectHighlight();
    }

    private void UpdateCharSelectHighlight()
    {
        for (int i = 0; i < 3; i++)
        {
            bool isFocus = (i == selectedCharIndex);
            bool isEquipped = (i == currentEquippedChar);

            if (cardBorders[i] != null)
            {
                cardBorders[i].color = isFocus
                    ? new Color(1f, 0.88f, 0.25f, 1f) // Bright Gold border
                    : (isEquipped ? new Color(0.2f, 0.8f, 0.4f, 0.9f) : new Color(0.3f, 0.4f, 0.6f, 0.5f));
            }

            if (charStatusTexts[i] != null)
            {
                if (isEquipped)
                {
                    charStatusTexts[i].text = "[ EQUIPPED ]";
                    charStatusTexts[i].color = new Color(0.35f, 0.95f, 0.4f, 1f); // Vibrant Green
                }
                else
                {
                    charStatusTexts[i].text = isFocus ? "> CLICK TO SELECT <" : "SELECT";
                    charStatusTexts[i].color = isFocus ? new Color(1f, 0.92f, 0.35f, 1f) : new Color(0.7f, 0.75f, 0.85f, 0.8f);
                }
            }
        }
    }
}
