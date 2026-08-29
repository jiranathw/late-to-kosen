using UnityEngine;

public class RockTrigger : MonoBehaviour
{
    public FallingRock fallingRock;

    private bool triggered = false;

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag("Player")) return;
        if (triggered) return;

        triggered = true;

        if (fallingRock != null)
        {
            fallingRock.Activate();
        }
    }

    public void ResetTrigger()
    {
        triggered = false;
    }
}