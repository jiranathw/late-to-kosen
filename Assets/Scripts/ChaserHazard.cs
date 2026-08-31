using UnityEngine;

// The soi dog.
//
// Rethemed from Krin's DeathBeam, which was a Kamehameha that grew out of a
// wall. The mechanic was good - a thing behind you that turns a careful stretch
// into a sprint - but a Dragon Ball beam is someone else's copyrighted art in a
// graded submission and it fights Bun's 8-bit style. A dog that comes out of a
// soi when you walk past does the same job and is the single most universal
// experience of walking anywhere in Thailand.
//
// Behaviour: sits asleep off-screen left. A HazardTrigger wakes it. It then
// runs right at `chaseSpeed` and kills on contact. It gives up after
// `giveUpDistance`, because a hazard that follows you for the rest of the
// stage stops being funny about four seconds in.
[RequireComponent(typeof(Collider2D))]
public class ChaserHazard : MonoBehaviour, ITriggerable
{
    [Header("Chase")]
    [SerializeField] private float chaseSpeed = 7.6f;   // faster than walk (6), slower than sprint (8.5)
    [SerializeField] private float giveUpDistance = 34f;
    [SerializeField] private string playerTag = "Player";

    [Header("Wake-up")]
    [Tooltip("Wakes when the player is this far AHEAD of it. 0 disables the " +
             "proximity check and leaves a HazardTrigger as the only way in.")]
    [SerializeField] private float triggerDistance = 8f;

    [Header("Wind-up")]
    [Tooltip("Seconds between the trigger and the dog actually moving. This is " +
             "the player's warning; without it the chase is unfair.")]
    [SerializeField] private float windUpSeconds = 0.45f;

    [Header("Feedback")]
    [SerializeField] private HazardTrigger rearmOnDeath;

    private Vector3 restPosition;
    private SpriteRenderer sprite;
    private Transform player;
    private bool running;
    private float windUpLeft;
    private float travelled;

    private void Awake()
    {
        restPosition = transform.position;
        sprite = GetComponent<SpriteRenderer>();
        Sleep();
    }

    private void Start()
    {
        // Counts toward "traps survived" at the position where it stops being a
        // threat, not where it starts - otherwise the player scores it just by
        // standing still in front of it.
        GameManager.Instance?.RegisterTrap(restPosition.x + giveUpDistance);

        // Subscribed in Start, not Awake: GameManager.Instance is assigned in
        // GameManager.Awake and the order of two Awakes is not guaranteed.
        if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerRespawned += OnPlayerRespawned;
        }
    }

    private void OnDestroy()
    {
        if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerRespawned -= OnPlayerRespawned;
        }
    }

    // Without this, the ajarn only ever happens once per run.
    //
    // He is mid-chase when you die - `running` is true and he is somewhere out
    // to the right of his post. Nothing resets him, so he keeps going until he
    // has covered giveUpDistance and only then sleeps, by which time you have
    // respawned at the checkpoint and walked back through his wake-up window.
    // CheckProximity only fires while the player is within triggerDistance
    // AHEAD of his rest position, so once you are past that band he is asleep
    // for good and the rest of the run has no chase in it at all.
    //
    // Putting him back on his post the moment the player respawns re-arms the
    // proximity check, and the second run through the soi plays like the first.
    private void OnPlayerRespawned()
    {
        Sleep();
        if (rearmOnDeath != null) rearmOnDeath.Rearm();
    }

    public void Trigger()
    {
        if (running) return;
        running = true;
        windUpLeft = windUpSeconds;
        travelled = 0f;
        gameObject.SetActive(true);
        if (sprite != null) sprite.enabled = true;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null || gm.IsPaused || gm.IsGameOver) return;

        if (!running)
        {
            CheckProximity();
            return;
        }

        if (windUpLeft > 0f)
        {
            windUpLeft -= Time.deltaTime;

            // Crouch-and-bark tell: a small bob so the player can see something
            // is about to happen even before Bun's animation exists.
            if (sprite != null)
            {
                float bob = Mathf.Sin(Time.time * 26f) * 0.09f;
                transform.position = restPosition + new Vector3(0f, bob, 0f);
            }
            return;
        }

        float step = chaseSpeed * Time.deltaTime;
        transform.position += Vector3.right * step;
        travelled += step;

        if (travelled >= giveUpDistance) Sleep();
    }

    private void OnTriggerEnter2D(Collider2D other) { TryKill(other); }
    private void OnCollisionEnter2D(Collision2D c)  { TryKill(c.collider); }

    private void TryKill(Collider2D other)
    {
        if (!running || windUpLeft > 0f) return;
        if (!other.CompareTag(playerTag)) return;

        PlayerController player = other.GetComponent<PlayerController>();

        // Reset BEFORE the kill. PlayerController.Die may end the run, and a
        // dog left mid-street on the game-over screen looks broken.
        Sleep();
        if (rearmOnDeath != null) rearmOnDeath.Rearm();

        if (player != null) player.Die();
        else GameManager.Instance?.PlayerDied();
    }

    // Self-arming, so the dog needs no trigger object wired to it in the scene
    // and re-arms by itself after it kills you. Only fires while the player is
    // AHEAD of the dog: walking backwards past a sleeping dog should not set it
    // off, because then it would be chasing you in the direction you already
    // came from.
    private void CheckProximity()
    {
        if (triggerDistance <= 0f) return;

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag(playerTag);
            if (p == null) return;
            player = p.transform;
        }

        float ahead = player.position.x - restPosition.x;
        if (ahead > 0f && ahead <= triggerDistance) Trigger();
    }

    private void Sleep()
    {
        running = false;
        windUpLeft = 0f;
        travelled = 0f;
        transform.position = restPosition;
        if (sprite != null) sprite.enabled = false;
    }
}
