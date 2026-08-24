using UnityEngine;
using TMPro;

// Attach to a TextMeshPro UI text object under a Canvas.
public class DeathCounterUI : MonoBehaviour
{
    [SerializeField] private TMP_Text deathText; // drag this same object's TMP_Text component here

    private void Update()
    {
        if (GameManager.Instance == null || deathText == null) return;
        deathText.text = $"Deaths: {GameManager.Instance.DeathCount}";
    }
}
