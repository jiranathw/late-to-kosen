using UnityEngine;

// Attach to the "school gate" object at the end of the level.
public class GoalTrigger : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;
        GameManager.Instance?.WinGame();
    }
}
