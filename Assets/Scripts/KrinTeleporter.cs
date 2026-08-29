using UnityEngine;

public class KrinTeleporter : MonoBehaviour
{
    [Header("Teleport Destination")]
    public Transform destination;

    [Header("Starting Point")]
    public Transform startPoint;

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag("Player")) return;

        // Reset checkpoint to the beginning
        if (GameManager.Instance != null && startPoint != null)
        {
            GameManager.Instance.SetCheckpoint(startPoint.position);
        }

        // Teleport player
        if (destination != null)
        {
            other.transform.position = destination.position;
        }
        else
        {
            Debug.LogWarning("KrinTeleporter: Destination is not assigned!");
        }
    }
}