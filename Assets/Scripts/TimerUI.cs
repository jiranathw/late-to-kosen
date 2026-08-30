using UnityEngine;
using TMPro;

// Attach to a TextMeshPro UI text object under a Canvas.
// Hides during stage intro title card so the screen stays clean.
// Features bold white text with thick black outline for maximum readability.
public class TimerUI : MonoBehaviour
{
    [SerializeField] private TMP_Text timerText;
    private bool styleApplied;

    private void Awake()
    {
        if (timerText == null) timerText = GetComponent<TMP_Text>();
        ApplySharpStyle();
    }

    private void ApplySharpStyle()
    {
        if (timerText == null || styleApplied) return;
        timerText.color = Color.white;
        timerText.fontStyle = FontStyles.Bold;
        timerText.outlineWidth = 0.35f;
        timerText.outlineColor = new Color32(0, 0, 0, 255);
        if (timerText.fontMaterial != null)
        {
            timerText.fontMaterial.EnableKeyword(ShaderUtilities.Keyword_Outline);
            timerText.fontMaterial.SetColor(ShaderUtilities.ID_OutlineColor, new Color32(0, 0, 0, 255));
            timerText.fontMaterial.SetFloat(ShaderUtilities.ID_OutlineWidth, 0.35f);
        }
        styleApplied = true;
    }

    private void Update()
    {
        if (GameManager.Instance == null) return;
        if (timerText == null) timerText = GetComponent<TMP_Text>();
        if (timerText == null) return;

        if (!styleApplied) ApplySharpStyle();

        if (GameManager.Instance.IsIntroActive || GameManager.Instance.IsGameOver)
        {
            if (timerText.enabled) timerText.enabled = false;
            return;
        }

        if (!timerText.enabled) timerText.enabled = true;

        float t = GameManager.Instance.TimeRemaining;
        int minutes = Mathf.FloorToInt(t / 60f);
        int seconds = Mathf.FloorToInt(t % 60f);
        timerText.text = $"{minutes:00}:{seconds:00}";
    }
}
