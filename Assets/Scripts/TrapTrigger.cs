using UnityEngine;

// Attach to any trap/hazard GameObject. Its Collider2D must have "Is Trigger" checked.
// Reusable: same script works for every trap prefab in the game.
//
// Registers itself with the GameManager so the score can count how many traps
// the player got past without dying.
public class TrapTrigger : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private bool countsTowardScore = true;

    private void Start()
    {
        if (countsTowardScore)
        {
            GameManager.Instance?.RegisterTrap(transform.position.x);
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        PlayerController player = other.GetComponent<PlayerController>();
        if (player != null) player.Die();
        else GameManager.Instance?.PlayerDied();
    }
}
