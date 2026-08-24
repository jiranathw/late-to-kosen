using UnityEngine;

// Attach to a trigger zone the player walks through to save progress.
// Place a few of these along each level so death doesn't send the player back to the very start.
public class Checkpoint : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;
        GameManager.Instance?.SetCheckpoint(transform.position);
    }
}
