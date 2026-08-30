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

    // CEILING MODE. Used by the black kill blocks that plug the stairwell gaps.
    //
    // Those blocks live in the slab band just under the floor above, and the
    // jump apex is taller than the gap between floors - so a player jumping on
    // the lower floor punches their head straight into the block and dies for
    // nothing. With this on, a body whose centre is BELOW the block passes
    // through harmlessly; only a fall from above kills. The block is also
    // taller than the arc can clear, so nobody can pop out the top and then
    // come back down "from above" by accident.
    [SerializeField] private bool onlyKillFromAbove;

    private SpriteRenderer sprite;
    private bool revealed;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();
        Hide();
    }

    private void OnEnable()
    {
        // LevelPropArt runs at -80 and can switch a renderer back on. Re-hide
        // here so an untriggered trap never flashes into view on scene load.
        if (!revealed) Hide();
    }

    private void Start()
    {
        GameManager.Instance?.RegisterTrap(transform.position.x);
    }

    private void Hide()
    {
        if (sprite == null) return;
        sprite.enabled = false;          // invisible until it gets you
        sprite.forceRenderingOff = true;
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        // Came up from underneath - this is a head-bump, not a landing.
        if (onlyKillFromAbove && other.bounds.center.y <= transform.position.y) return;

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
            sprite.forceRenderingOff = false;
            // Keep the wet-floor sprite colours. The pink tint was for the
            // placeholder square so a revealed trap was still readable.
            if (sprite.sprite == null || sprite.sprite.name == "Square")
                sprite.color = revealedColor;
            else
                sprite.color = Color.white;
        }
    }
}
