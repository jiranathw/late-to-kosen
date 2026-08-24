using UnityEngine;

// Attach to the Player GameObject. Requires Rigidbody2D + a Collider2D on the same object.
[RequireComponent(typeof(Rigidbody2D))]
public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 6f;
    [SerializeField] private float jumpForce = 12f;

    [Header("Ground Check")]
    [SerializeField] private Transform groundCheck;   // empty child object at the player's feet
    [SerializeField] private float groundCheckRadius = 0.15f;
    [SerializeField] private LayerMask groundLayer;   // set to the "Ground" layer

    [Header("Fall Safety")]
    // Falling off the level counts as a death instead of dropping forever.
    // Keep this comfortably below the lowest platform in the level.
    [SerializeField] private float killY = -20f;

    private Rigidbody2D rb;
    private bool isGrounded;
    private float moveInput;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
    }

    private void Update()
    {
        if (GameManager.Instance != null && GameManager.Instance.IsGameOver)
        {
            moveInput = 0f; // stop sliding once the run is over
            return;
        }

        // Fell off the map: treat it exactly like walking into a trap.
        if (transform.position.y < killY)
        {
            GameManager.Instance?.PlayerDied();
            Respawn();
            return;
        }

        // Default Input Manager: Horizontal = A/D and Left/Right arrows
        moveInput = Input.GetAxisRaw("Horizontal");

        isGrounded = groundCheck != null &&
                     Physics2D.OverlapCircle(groundCheck.position, groundCheckRadius, groundLayer);

        // Default Input Manager: Jump = Space
        if (isGrounded && Input.GetButtonDown("Jump"))
        {
            rb.linearVelocity = new Vector2(rb.linearVelocity.x, jumpForce);
        }

        if (moveInput != 0f)
        {
            transform.localScale = new Vector3(Mathf.Sign(moveInput), 1f, 1f);
        }
    }

    private void FixedUpdate()
    {
        rb.linearVelocity = new Vector2(moveInput * moveSpeed, rb.linearVelocity.y);
    }

    public void Respawn()
    {
        if (GameManager.Instance == null) return;
        transform.position = GameManager.Instance.GetCheckpoint();
        rb.linearVelocity = Vector2.zero;
    }

    private void OnDrawGizmosSelected()
    {
        if (groundCheck == null) return;
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(groundCheck.position, groundCheckRadius);
    }
}
