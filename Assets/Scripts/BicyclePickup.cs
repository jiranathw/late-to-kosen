using UnityEngine;

// Bicycle power-up - "temporarily increases movement speed" (Optional Features
// on the design form).
//
// One-shot: touch it, it disappears and the player rides faster for a few
// seconds. It comes back if you die, because it belongs to the level rather
// than to the run - respawning at a checkpoint before a bike you already used
// would otherwise leave you permanently worse off.
[RequireComponent(typeof(Collider2D))]
public class BicyclePickup : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private float boostSeconds = 4.5f;
    [SerializeField] private float respawnSeconds = 6f;
    [SerializeField] private float bobHeight = 0.14f;
    [SerializeField] private float bobSpeed = 2.6f;

    private SpriteRenderer sprite;
    private Collider2D col;
    private Vector3 restPosition;
    private float cooldown;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();
        col = GetComponent<Collider2D>();
        restPosition = transform.position;
    }

    private void Update()
    {
        if (cooldown > 0f)
        {
            cooldown -= Time.deltaTime;
            if (cooldown <= 0f) SetAvailable(true);
            return;
        }

        // Gentle bob so it reads as a pickup and not as scenery.
        float y = restPosition.y + Mathf.Sin(Time.time * bobSpeed) * bobHeight;
        transform.position = new Vector3(restPosition.x, y, restPosition.z);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (cooldown > 0f) return;
        if (!other.CompareTag(playerTag)) return;

        PlayerController player = other.GetComponent<PlayerController>();
        if (player == null) return;

        player.GrantBike(boostSeconds);
        cooldown = respawnSeconds;
        SetAvailable(false);
    }

    private void SetAvailable(bool available)
    {
        if (sprite != null) sprite.enabled = available;
        if (col != null) col.enabled = available;
    }
}
