using UnityEngine;

// Movement, jumping and respawn for the KOSEN student.
//
// Tuned values live here rather than in the scene so they survive a scene
// revert. If you change them in the Inspector, change them here too or the
// next person to reset the prefab loses your tuning.
[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 6f;      // 8 read as a sprint even when walking
    [SerializeField] private float sprintSpeed = 8.5f;  // Shift now roughly the old walk speed

    [Header("Sprint (Shift) - a short boost, not a permanent one")]
    [SerializeField] private float maxStamina = 2.5f;   // seconds of sprint
    [SerializeField] private float staminaRegen = 0.6f; // seconds regained per second
    private float stamina;
    private bool sprintLocked;                          // must release Shift after draining
    public float Stamina01 => maxStamina <= 0f ? 0f : Mathf.Clamp01(stamina / maxStamina);
    public bool IsSprinting { get; private set; }

    [Header("Bicycle power-up (Optional feature from the design form)")]
    [SerializeField] private float bikeMultiplier = 1.45f; // applied on top of walk/sprint
    private float bikeTimer;
    public bool HasBike => bikeTimer > 0f;
    public float BikeSecondsLeft => Mathf.Max(0f, bikeTimer);

    [Header("Jump")]
    [SerializeField] private float jumpForce = 13f;

    [Header("Jump Feel")]
    [SerializeField] private float coyoteTime = 0.12f;
    [SerializeField] private float jumpBufferTime = 0.12f;
    [SerializeField] private float fallMultiplier = 1.5f;
    [SerializeField] private float lowJumpMultiplier = 2.5f;

    [Header("Ground Check")]
    [SerializeField] private Transform groundCheck;
    [SerializeField] private float groundCheckRadius = 0.13f;
    [SerializeField] private LayerMask groundLayer;

    [Header("Fall Safety")]
    [SerializeField] private float killY = -12f;

    private Rigidbody2D rb;
    private float baseGravityScale;
    private float moveInput;
    private float coyoteCounter;
    private float jumpBufferCounter;
    private bool isGrounded;
    private bool jumpHeld;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        baseGravityScale = rb.gravityScale;
        stamina = maxStamina;

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
            IsSprinting = false;
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

        UpdateSprint();

        if (bikeTimer > 0f) bikeTimer -= Time.deltaTime;

        isGrounded = groundCheck != null &&
                     Physics2D.OverlapCircle(groundCheck.position, groundCheckRadius, groundLayer);

        coyoteCounter = isGrounded ? coyoteTime : coyoteCounter - Time.deltaTime;
        jumpBufferCounter = Input.GetButtonDown("Jump") ? jumpBufferTime
                                                        : jumpBufferCounter - Time.deltaTime;

        if (jumpBufferCounter > 0f && coyoteCounter > 0f)
        {
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, jumpForce);
            jumpBufferCounter = 0f; // consume both or a single press double-jumps
            coyoteCounter = 0f;
        }

        if (moveInput != 0f)
        {
            transform.localScale = new Vector3(Mathf.Sign(moveInput), 1f, 1f);
        }
    }

    private void UpdateSprint()
    {
        bool wantsSprint = Input.GetKey(KeyCode.LeftShift) || Input.GetKey(KeyCode.RightShift);

        if (!wantsSprint) sprintLocked = false; // releasing Shift clears the lockout

        IsSprinting = wantsSprint && !sprintLocked && stamina > 0f && moveInput != 0f;

        if (IsSprinting)
        {
            stamina -= Time.deltaTime;
            if (stamina <= 0f)
            {
                stamina = 0f;
                sprintLocked = true; // no stutter-tapping for infinite sprint
                IsSprinting = false;
            }
        }
        else if (stamina < maxStamina)
        {
            stamina = Mathf.Min(maxStamina, stamina + staminaRegen * Time.deltaTime);
        }
    }

    private void FixedUpdate()
    {
        float speed = IsSprinting ? sprintSpeed : moveSpeed;
        if (bikeTimer > 0f) speed *= bikeMultiplier;
        rb.linearVelocity = new Vector2(moveInput * speed, rb.linearVelocity.y);
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

    // Called by BicyclePickup. A second bike refreshes the timer rather than
    // stacking it, so the speed can never run away from the player.
    public void GrantBike(float seconds)
    {
        bikeTimer = Mathf.Max(bikeTimer, seconds);
        stamina = maxStamina;   // hopping on a bike is a breather
        sprintLocked = false;
    }

    // Single entry point for dying, so traps and the fall-out-of-the-world
    // check can never disagree about what happens next.
    public void Die()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null) return;
        if (gm.PlayerDied()) Respawn();
    }

    public void Respawn()
    {
        if (GameManager.Instance == null) return;

        rb.position = GameManager.Instance.GetCheckpoint();
        rb.linearVelocity = Vector2.zero;
        rb.gravityScale = baseGravityScale;
        coyoteCounter = 0f;
        jumpBufferCounter = 0f;
        stamina = maxStamina; // don't punish a respawn with an empty sprint bar
        sprintLocked = false;
        bikeTimer = 0f;       // dying costs you the bike
    }

    private void OnDrawGizmosSelected()
    {
        if (groundCheck == null) return;
        Gizmos.color = Color.green;
        Gizmos.DrawWireSphere(groundCheck.position, groundCheckRadius);
    }
}
