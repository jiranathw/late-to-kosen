using UnityEngine;
using TMPro;

// Attach to a TextMeshPro UI text object under a Canvas.
// Hides during stage intro title card so the screen stays clean.
// Features bold white text with thick black outline for maximum readability.
public class DeathCounterUI : MonoBehaviour
{
    [SerializeField] private TMP_Text deathText;
    private bool styleApplied;

    private void Awake()
    {
        if (deathText == null) deathText = GetComponent<TMP_Text>();
        ApplySharpStyle();
    }

    private void ApplySharpStyle()
    {
        if (deathText == null || styleApplied) return;
        deathText.color = Color.white;
        deathText.fontStyle = FontStyles.Bold;
        deathText.outlineWidth = 0.35f;
        deathText.outlineColor = new Color32(0, 0, 0, 255);
        if (deathText.fontMaterial != null)
        {
            deathText.fontMaterial.EnableKeyword(ShaderUtilities.Keyword_Outline);
            deathText.fontMaterial.SetColor(ShaderUtilities.ID_OutlineColor, new Color32(0, 0, 0, 255));
            deathText.fontMaterial.SetFloat(ShaderUtilities.ID_OutlineWidth, 0.35f);
        }
        styleApplied = true;
    }

    private void Update()
    {
        if (GameManager.Instance == null) return;
        if (deathText == null) deathText = GetComponent<TMP_Text>();
        if (deathText == null) return;

        if (!styleApplied) ApplySharpStyle();

        if (GameManager.Instance.IsIntroActive || GameManager.Instance.IsGameOver)
        {
            if (deathText.enabled) deathText.enabled = false;
            return;
        }

        if (!deathText.enabled) deathText.enabled = true;

        deathText.text = $"Deaths: {GameManager.Instance.DeathCount}";
    }
}
