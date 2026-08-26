using UnityEngine;

// Attach to a trigger zone the player walks through to save progress.
// Place a few of these along each level so death doesn't send the player back
// to the very start.
//
// The prefab carries a SpriteRenderer purely as feedback: the marker sits dim
// until you touch it, then turns bright green. Without that, a checkpoint is an
// invisible box and the player has no idea their progress was saved.
[RequireComponent(typeof(Collider2D))]
public class Checkpoint : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private Color armedColor = new Color(1f, 0.85f, 0.2f, 0.45f);
    [SerializeField] private Color reachedColor = new Color(0.35f, 1f, 0.45f, 0.95f);

    private SpriteRenderer sprite;
    private bool reached;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();
        if (sprite != null) sprite.color = armedColor;
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        // Latching on `reached` also stops backtracking from moving the respawn
        // point backwards through an earlier checkpoint.
        if (reached) return;
        if (!other.CompareTag(playerTag)) return;

        reached = true;
        GameManager.Instance?.SetCheckpoint(transform.position);
        if (sprite != null) sprite.color = reachedColor;
    }
}
