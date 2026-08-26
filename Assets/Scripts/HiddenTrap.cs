using UnityEngine;

// TROLL TRAP TYPE 1 - the invisible one.
//
// Sits on a stretch of ground that looks completely safe. Kills on contact.
// The instant it kills you it turns visible and STAYS visible for the rest of
// the run, so the retry is fair: you get trolled exactly once per trap.
// That is what separates a troll game from a cheap game.
[RequireComponent(typeof(Collider2D))]
public class HiddenTrap : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private Color revealedColor = new Color(1f, 0.25f, 0.3f, 1f);

    private SpriteRenderer sprite;
    private bool revealed;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();
        if (sprite != null) sprite.enabled = false; // invisible until it gets you
    }

    private void Start()
    {
        GameManager.Instance?.RegisterTrap(transform.position.x);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        Reveal();

        PlayerController player = other.GetComponent<PlayerController>();
        if (player != null) player.Die();
        else GameManager.Instance?.PlayerDied();
    }

    private void Reveal()
    {
        if (revealed) return;
        revealed = true;
        if (sprite != null)
        {
            sprite.enabled = true;
            sprite.color = revealedColor;
        }
    }
}
