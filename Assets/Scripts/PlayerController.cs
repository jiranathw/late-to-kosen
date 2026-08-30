using UnityEngine;

// Movement, jumping and respawn for the KOSEN student.
//
// Tuned values live here rather than in the scene so they survive a scene
// revert. If you change them in the Inspector, change them here too or the
// next person to reset the prefab loses your tuning.
[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    // SPEED. One gear, no Shift.
    //
    // Sprint is gone as of 28 Aug (evening). It was a 2.5-second burst on a lockout, and
    // in practice it was only ever used to cross the one gap that needed it,
    // which made it a hidden requirement rather than a choice. The team asked
    // to "take sprint out but keep it as fast as it was", so 7.5 IS the old
    // sprint speed and it is now the only speed. One less key to teach, one
    // less system to balance, and every gap in the game can be measured
    // against a single number.
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 7.5f;

    // JUMP. Retuned 28 Aug (evening) so Krin's stage is actually completable.
    //
    // Krin built his level against jumpForce 7 at gravityScale 1 - a 2.50u apex
    // and a very floaty 1.43s in the air, giving an 8.56u flat reach. Our
    // previous tuning (12 against 3.4) reached 3.45u, which could not cross his
    // widest gap - 5.04u, between Ground_Start and GroundCheckpoint1 - even at
    // a sprint, and could not climb his +2.1u steps at all. His stage was
    // literally impossible on our physics, which is why this moved.
    //
    // 13.5 against 2.6 with fallMultiplier 1.8:
    //     apex     3.57u      rise 0.529s    fall 0.395s
    //     airtime  0.92s      flat reach     6.93u
    // Krin's 5.04u gap is 73% of that reach, just inside the 75% design rule,
    // and the apex clears his +2.1u steps with 1.4u to spare.
    //
    // gravityScale 2.6 is a Rigidbody2D property and lives in
    // Tools/scene_skeleton.unity, not here - gravity belongs to the body.
    // These numbers also exist as constants at the top of Tools/build_levels.py,
    // which is what the design-rule checker measures every gap against. Change
    // one, change all three.
    [Header("Jump")]
    [SerializeField] private float jumpForce = 13.5f;

    [Header("Jump Feel")]
    [SerializeField] private float coyoteTime = 0.12f;
    [SerializeField] private float jumpBufferTime = 0.12f;
    [SerializeField] private float fallMultiplier = 1.8f;   // land fast, never float
    [SerializeField] private float lowJumpMultiplier = 3f;  // a tap is a small hop

    // THE ANYWHEEL BIKE.
    //
    // Not a speed power-up any more. You pick a bike up and you are ON it until
    // you find somewhere to park it, exactly like the real thing: the app will
    // not end your ride outside a docking zone, so you go looking for a rack
    // while the meter runs. Some of the racks in this game are painted on.
    // See BikeRental.cs and BikeRack.cs.
    //
    // Riding is faster but heavier: input is smoothed instead of instant, so
    // you carry momentum and overshoot, and the jump is cut because you are on
    // a bicycle. That combination is what makes the bike a decision instead of
    // a free upgrade.
    [Header("Bicycle (Anywheel)")]
    [SerializeField] private float bikeSpeedMultiplier = 1.5f;
    [SerializeField] private float bikeJumpMultiplier = 0.78f;
    [Tooltip("Seconds to reach full speed, and to stop, while riding. On foot " +
             "the response stays instant.")]
    [SerializeField] private float bikeAccelTime = 0.35f;
    public bool IsRiding { get; private set; }

    [Header("Ground Check")]
    [SerializeField] private Transform groundCheck;
    [SerializeField] private float groundCheckRadius = 0.13f;
    [SerializeField] private LayerMask groundLayer;

    [Header("Fall Safety")]
    [SerializeField] private float killY = -12f;

    private Rigidbody2D rb;
    private float baseGravityScale;
    private float moveInput;
    private float rideVelocity;     // smoothed horizontal speed while riding
    private float coyoteCounter;
    private float jumpBufferCounter;
    private bool isGrounded;
    private bool jumpHeld;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        baseGravityScale = rb.gravityScale;

        if (GetComponent<PlayerAnimator>() == null)
        {
            gameObject.AddComponent<PlayerAnimator>();
        }

        // Zero friction, or the player catches on the vertical face of a
        // platform when falling into a gap and hangs there instead of dropping.
        // Costs nothing: horizontal velocity is assigned outright every
        // FixedUpdate, so there is no ice-skating when you let go of the key.
        Collider2D body = GetComponent<Collider2D>();
        if (body != null && body.sharedMaterial == null)
        {
            body.sharedMaterial = new PhysicsMaterial2D("PlayerNoFriction")
            {
                friction = 0f,
                bounciness = 0f
            };
        }
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;

        if (gm != null && (gm.IsGameOver || gm.IsPaused))
        {
            // Zero the input so the player doesn't drift or bank a jump while
            // the pause menu is up. Time.timeScale already froze the physics.
            moveInput = 0f;
            jumpBufferCounter = 0f;
            return;
        }

        // rb.position, not transform: autoSyncTransforms is off, transform lags a step
        if (rb.position.y < killY)
        {
            Die();
            return;
        }

        moveInput = Input.GetAxisRaw("Horizontal");
        jumpHeld = Input.GetButton("Jump");

        isGrounded = groundCheck != null &&
                     Physics2D.OverlapCircle(groundCheck.position, groundCheckRadius, groundLayer);

        coyoteCounter = isGrounded ? coyoteTime : coyoteCounter - Time.deltaTime;
        jumpBufferCounter = Input.GetButtonDown("Jump") ? jumpBufferTime
                                                        : jumpBufferCounter - Time.deltaTime;

        if (jumpBufferCounter > 0f && coyoteCounter > 0f)
        {
            float force = IsRiding ? jumpForce * bikeJumpMultiplier : jumpForce;
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, force);
            jumpBufferCounter = 0f; // consume both or a single press double-jumps
            coyoteCounter = 0f;
            AudioManager.Instance?.PlayJumpSFX();
        }

        if (moveInput != 0f)
        {
            transform.localScale = new Vector3(Mathf.Sign(moveInput), 1f, 1f);
        }
    }

    private void FixedUpdate()
    {
        float target = moveInput * moveSpeed * (IsRiding ? bikeSpeedMultiplier : 1f);

        if (IsRiding && bikeAccelTime > 0f)
        {
            // A bike does not start and stop on a key press. Ramping toward the
            // target instead of assigning it outright is the whole feel of the
            // thing: you commit to a direction and then you live with it for a
            // third of a second.
            float maxStep = (moveSpeed * bikeSpeedMultiplier / bikeAccelTime) * Time.fixedDeltaTime;
            rideVelocity = Mathf.MoveTowards(rideVelocity, target, maxStep);
        }
        else
        {
            rideVelocity = target;
        }

        rb.linearVelocity = new Vector2(rideVelocity, rb.linearVelocity.y);
        ApplyJumpGravity();
    }

    // Rising slowly and falling fast is what makes a 2D jump feel good rather
    // than floaty. Releasing the jump button early cuts the arc short.
    private void ApplyJumpGravity()
    {
        if (rb.linearVelocity.y < -0.01f)
        {
            rb.gravityScale = baseGravityScale * fallMultiplier;
        }
        else if (rb.linearVelocity.y > 0.01f && !jumpHeld)
        {
            rb.gravityScale = baseGravityScale * lowJumpMultiplier;
        }
        else
        {
            rb.gravityScale = baseGravityScale;
        }
    }

    // THE BIKE. Mounting is free. Getting off is not.
    //
    // There is deliberately no timer and no "drop bike" key. BikeRack is the
    // only thing in the game that clears IsRiding, and one of the racks on
    // stage 1 is painted on. That is the joke, and it is why build_levels.py
    // rule 9 checks that everything after a rack is still crossable on a bike.
    public void MountBike()
    {
        if (IsRiding) return;
        IsRiding = true;

        // Inherit whatever speed you were already carrying, so the ramp in
        // FixedUpdate starts from where you are instead of snapping you to a
        // standstill the instant you touch the bike.
        rideVelocity = rb.linearVelocity.x;
    }

    public void ParkBike()
    {
        if (!IsRiding) return;
        IsRiding = false;
        rideVelocity = 0f;
    }

    // Single entry point for dying, so traps and the fall-out-of-the-world
    // check can never disagree about what happens next.
    public void Die()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null) return;
        AudioManager.Instance?.PlayDeathSFX();
        if (gm.PlayerDied()) Respawn();
    }

    public void Respawn()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null) return;

        rb.position = gm.GetCheckpoint();
        rb.linearVelocity = Vector2.zero;
        rb.gravityScale = baseGravityScale;
        coyoteCounter = 0f;
        jumpBufferCounter = 0f;
        rideVelocity = 0f;

        // Reset all level traps, falling rocks, and beams for the fresh attempt
        FallingRock.ResetAllRocks();
        DeathBeam.ResetAllBeams();

        AudioManager.Instance?.PlayRespawnSFX();
        gm.NotifyRespawned();
    }

    private void OnDrawGizmosSelected()
    {
        if (groundCheck == null) return;
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(groundCheck.position, groundCheckRadius);
    }
}