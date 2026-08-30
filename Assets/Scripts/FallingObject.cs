using UnityEngine;

// The flowerpot off the third-floor balcony.
//
// Rethemed from Krin's FallingRock. Two real fixes on the way across:
//
//   1. rb.velocity is gone in Unity 6. It is rb.linearVelocity now, and the old
//      name does not even compile.
//   2. The original called GameManager.PlayerDied() and then Respawn()
//      unconditionally, so on the last life the player respawned INTO a run
//      that had already ended. Everything goes through PlayerController.Die()
//      now, which is the one place that knows whether a life is left.
//
// It also puts itself back rather than disabling itself forever, so the retry
// is the same gag and not an empty balcony.
[RequireComponent(typeof(Rigidbody2D))]
public class FallingObject : MonoBehaviour, ITriggerable
{
    [Tooltip("Drops when the player is this far short of being underneath it. " +
             "Tuned so the pot arrives at head height as the player does.")]
    [SerializeField] private float triggerDistance = 3.4f;

    [SerializeField] private float fallGravity = 3.4f;
    [SerializeField] private float resetAfterSeconds = 3.5f;
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private HazardTrigger rearmOnReset;

    private Rigidbody2D rb;
    private Vector3 restPosition;
    private SpriteRenderer sprite;
    private Collider2D col;
    private Transform player;
    private float timer;
    private bool falling;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        col = GetComponent<Collider2D>();
        sprite = GetComponent<SpriteRenderer>();
        restPosition = transform.position;
        Rest();
    }

    private void Start()
    {
        GameManager.Instance?.RegisterTrap(restPosition.x);
    }

    public void Trigger()
    {
        if (falling) return;

        falling = true;
        timer = resetAfterSeconds;

        rb.bodyType = RigidbodyType2D.Dynamic;
        rb.gravityScale = fallGravity;
        rb.linearVelocity = Vector2.zero;
        rb.angularVelocity = 0f;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null || gm.IsPaused || gm.IsGameOver) return;

        if (!falling)
        {
            CheckProximity();
            return;
        }

        timer -= Time.deltaTime;
        if (timer <= 0f) Rest();
    }

    // Self-arming for the same reason as ChaserHazard: no wiring in the scene,
    // and it re-arms itself for the retry.
    //
    // The proximity test USED to be x-only and one-directional
    // (toGo > 0 && toGo <= triggerDistance), which broke twice over on a
    // stacked-floor stage:
    //
    //   1. No y test at all. Stage 1 is a stairwell - every x in the tower is
    //      spanned by four floors - so a player walking the floor ABOVE came
    //      within triggerDistance of the pot's x and dropped it while standing
    //      a whole storey away. By the time they came down it was long spent.
    //   2. toGo > 0 meant "only fire when the player is to the LEFT", i.e. only
    //      on a rightward approach. Floor 3 is walked RIGHT TO LEFT, so on the
    //      one floor the pot is actually meant to threaten, toGo was negative
    //      and it never fired at all.
    //
    // Now: the player has to be underneath the pot - which is what "on the
    // floor below the balcony" means - and may arrive from either side.
    private void CheckProximity()
    {
        if (triggerDistance <= 0f) return;

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag(playerTag);
            if (p == null) return;
            player = p.transform;
        }

        // Wrong storey. This single line is what stops the early drop.
        if (player.position.y >= restPosition.y) return;

        float toGo = Mathf.Abs(restPosition.x - player.position.x);
        if (toGo <= triggerDistance) Trigger();
    }

    private void OnCollisionEnter2D(Collision2D c) { TryKill(c.collider); }
    private void OnTriggerEnter2D(Collider2D other) { TryKill(other); }

    private void TryKill(Collider2D other)
    {
        if (!falling) return;

        if (!other.CompareTag(playerTag))
        {
            // Hit the pavement instead. Shatter, i.e. go back to the balcony.
            Rest();
            return;
        }

        PlayerController player = other.GetComponent<PlayerController>();
        Rest();
        if (player != null) player.Die();
        else GameManager.Instance?.PlayerDied();
    }

    private void Rest()
    {
        falling = false;

        rb.linearVelocity = Vector2.zero;
        rb.angularVelocity = 0f;
        rb.bodyType = RigidbodyType2D.Kinematic;

        transform.position = restPosition;
        transform.rotation = Quaternion.identity;

        if (col != null) col.enabled = true;
        if (sprite != null) sprite.enabled = true;
        if (rearmOnReset != null) rearmOnReset.Rearm();
    }
}
