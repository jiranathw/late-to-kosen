using UnityEngine;
using TMPro;

// Attach to a TextMeshPro UI text object under a Canvas.
// Hides during stage intro title card so the screen stays clean.
public class DeathCounterUI : MonoBehaviour
{
    [SerializeField] private TMP_Text deathText;

    private void Awake()
    {
        if (deathText == null) deathText = GetComponent<TMP_Text>();
    }

    private void Update()
    {
        if (GameManager.Instance == null) return;
        if (deathText == null) deathText = GetComponent<TMP_Text>();
        if (deathText == null) return;

        if (GameManager.Instance.IsIntroActive || GameManager.Instance.IsGameOver)
        {
            if (deathText.enabled) deathText.enabled = false;
            return;
        }

        if (!deathText.enabled) deathText.enabled = true;

        deathText.text = $"Deaths: {GameManager.Instance.DeathCount}";
    }
}
