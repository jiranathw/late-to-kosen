using UnityEngine;

// An Anywheel bike, lying where the last renter dumped it.
//
// This replaces BicyclePickup, which was a 4.5-second speed boost. A boost is a
// reward: you grab it, you go fast, it ends, nothing was asked of you. That is
// not what a rented bike is. You unlock one of these and you are ON it - faster,
// heavier, worse at jumping - until you find somewhere the app will let you end
// the ride. See PlayerController.MountBike / ParkBike and BikeRack.cs.
//
// One-shot and permanent. The old pickup respawned after six seconds so a player
// who died past it would not be left worse off; that reasoning does not apply
// any more, because you keep the bike when you die. Taking a bike is a decision
// the level should only offer once.
[RequireComponent(typeof(Collider2D))]
public class BikeRental : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    [Header("Idle")]
    [SerializeField] private float bobHeight = 0.14f;
    [SerializeField] private float bobSpeed = 2.6f;

    [Header("Sign")]
    [Tooltip("Shown from a distance, before the player commits.")]
    [SerializeField, TextArea] private string offerMessage = "ANYWHEEL - scan to unlock";

    [Tooltip("Latched on after mounting, so the player is still reading the " +
             "terms while they ride away from them.")]
    [SerializeField, TextArea] private string mountMessage =
        "RIDE STARTED - park at a rack to end it";

    private SpriteRenderer sprite;
    private Collider2D col;
    private Signpost sign;
    private Vector3 restPosition;
    private bool taken;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();
        col = GetComponent<Collider2D>();
        restPosition = transform.position;

        // The sign is part of the object rather than a separate prop, so a bike
        // placed by build_levels.py explains itself with no extra scene wiring.
        sign = GetComponent<Signpost>();
        if (sign == null) sign = gameObject.AddComponent<Signpost>();
        sign.Say(offerMessage, false);
    }

    private void Update()
    {
        if (taken) return;

        // Gentle bob so it reads as a pickup and not as scenery.
        float y = restPosition.y + Mathf.Sin(Time.time * bobSpeed) * bobHeight;
        transform.position = new Vector3(restPosition.x, y, restPosition.z);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (taken) return;
        if (!other.CompareTag(playerTag)) return;

        PlayerController player = other.GetComponent<PlayerController>();
        if (player == null) return;
        if (player.IsRiding) return;   // already on one; walking past is not a crime

        player.MountBike();
        taken = true;

        if (sign != null) sign.Say(mountMessage, true);
        if (sprite != null) sprite.enabled = false;
        if (col != null) col.enabled = false;
    }
}
