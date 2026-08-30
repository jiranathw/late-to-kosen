using UnityEngine;
using TMPro;

// Attach to a TextMeshPro UI text object under a Canvas.
// Hides during stage intro title card so the screen stays clean.
public class TimerUI : MonoBehaviour
{
    [SerializeField] private TMP_Text timerText;

    private void Awake()
    {
        if (timerText == null) timerText = GetComponent<TMP_Text>();
    }

    private void Update()
    {
        if (GameManager.Instance == null) return;
        if (timerText == null) timerText = GetComponent<TMP_Text>();
        if (timerText == null) return;

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
