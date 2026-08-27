using UnityEngine;

// Cycles through 8-bit sprite frames for the KOSEN student based on movement.
// Left/Right orientation is handled automatically via PlayerController's localScale flip.
[RequireComponent(typeof(SpriteRenderer))]
[RequireComponent(typeof(PlayerController))]
public class PlayerAnimator : MonoBehaviour
{
    [Header("Sprites")]
    [SerializeField] private Sprite idleSprite;
    [SerializeField] private Sprite[] runSprites;
    [SerializeField] private Sprite jumpSprite;

    [Header("Frame Rate")]
    [SerializeField] private float walkFps = 8f;
    [SerializeField] private float sprintFps = 13f;

    private SpriteRenderer sr;
    private Rigidbody2D rb;
    private PlayerController controller;
    private float animTimer;
    private int currentRunFrame;

    private void Awake()
    {
        sr = GetComponent<SpriteRenderer>();
        rb = GetComponent<Rigidbody2D>();
        controller = GetComponent<PlayerController>();

        // Ensure white tint so 8-bit sprite colors display accurately
        if (sr != null)
        {
            sr.color = Color.white;
        }

        // Auto-discover sprites if not assigned in Inspector
        if (idleSprite == null || runSprites == null || runSprites.Length == 0)
        {
            Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
            Sprite r1 = null, r2 = null, r3 = null, r4 = null;
            foreach (var s in all)
            {
                if (s == null) continue;
                if (s.name == "player_idle") idleSprite = s;
                else if (s.name == "player_run_1") r1 = s;
                else if (s.name == "player_run_2") r2 = s;
                else if (s.name == "player_run_3") r3 = s;
                else if (s.name == "player_run_4") r4 = s;
                else if (s.name == "player_jump") jumpSprite = s;
            }
            if (r1 != null && r2 != null && r3 != null && r4 != null)
            {
                runSprites = new Sprite[] { r1, r2, r3, r4 };
            }
        }
    }

    private void LateUpdate()
    {
        if (sr == null) return;

        // In air / jumping
        if (rb != null && Mathf.Abs(rb.linearVelocity.y) > 0.4f)
        {
            if (jumpSprite != null) sr.sprite = jumpSprite;
            return;
        }

        // Running / Walking state
        float xVel = rb != null ? Mathf.Abs(rb.linearVelocity.x) : 0f;
        if (xVel > 0.15f && runSprites != null && runSprites.Length > 0)
        {
            float fps = (controller != null && controller.IsSprinting) ? sprintFps : walkFps;
            animTimer += Time.deltaTime;
            if (animTimer >= 1f / fps)
            {
                animTimer -= 1f / fps;
                currentRunFrame = (currentRunFrame + 1) % runSprites.Length;
            }
            sr.sprite = runSprites[currentRunFrame];
        }
        else
        {
            // Idle state
            currentRunFrame = 0;
            animTimer = 0f;
            if (idleSprite != null)
            {
                sr.sprite = idleSprite;
            }
        }
    }
}
