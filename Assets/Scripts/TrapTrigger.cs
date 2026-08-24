using UnityEngine;

// Attach to any trap/hazard GameObject. Its Collider2D must have "Is Trigger" checked.
// Reusable: same script works for every trap prefab in the game (spikes, falling signs, etc).
public class TrapTrigger : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerDied();
        }

        PlayerController player = other.GetComponent<PlayerController>();
        if (player != null)
        {
            player.Respawn();
        }
    }
}
