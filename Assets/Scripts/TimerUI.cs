using UnityEngine;
using TMPro; // requires TextMeshPro - Unity will prompt "Import TMP Essentials" the first time, accept it

// Attach to a TextMeshPro UI text object under a Canvas.
public class TimerUI : MonoBehaviour
{
    [SerializeField] private TMP_Text timerText; // drag this same object's TMP_Text component here

    private void Update()
    {
        if (GameManager.Instance == null || timerText == null) return;

        float t = GameManager.Instance.TimeRemaining;
        int minutes = Mathf.FloorToInt(t / 60f);
        int seconds = Mathf.FloorToInt(t % 60f);
        timerText.text = $"{minutes:00}:{seconds:00}";
    }
}
