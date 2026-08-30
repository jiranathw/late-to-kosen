using UnityEngine;

// Cycles through 8-bit sprite frames for the KOSEN student based on movement.
// Handles:
// 1. Walking/running foot-stepping animation on foot
// 2. Anywheel Green Bicycle riding animation (pedaling cycle + mid-air bunny hop) when IsRiding == true
// 3. Air/jump pose
// 4. Knocked-out death pose
[RequireComponent(typeof(SpriteRenderer))]
[RequireComponent(typeof(PlayerController))]
public class PlayerAnimator : MonoBehaviour
{
    [Header("Sprites - On Foot")]
    [SerializeField] private Sprite idleSprite;
    [SerializeField] private Sprite[] runSprites;
    [SerializeField] private Sprite jumpSprite;
    [SerializeField] private Sprite deadSprite;

    [Header("Sprites - Riding Anywheel Bike")]
    [SerializeField] private Sprite rideIdleSprite;
    [SerializeField] private Sprite[] rideSprites;
    [SerializeField] private Sprite rideJumpSprite;

    [Header("Frame Rate")]
    [SerializeField] private float walkFps = 9f;
    [SerializeField] private float sprintFps = 14f;

    private SpriteRenderer sr;
    private Rigidbody2D rb;
    private PlayerController controller;
    private float animTimer;
    private int currentFrame;
    private bool isDeadPose;

    private void Awake()
    {
        sr = GetComponent<SpriteRenderer>();
        rb = GetComponent<Rigidbody2D>();
        controller = GetComponent<PlayerController>();

        if (sr != null)
        {
            sr.color = Color.white;
        }

        LoadSprites();
    }

    private void LoadSprites()
    {
        // 1. Foot Sprites
        if (idleSprite == null) idleSprite = Resources.Load<Sprite>("Sprites/player_idle");
        if (jumpSprite == null) jumpSprite = Resources.Load<Sprite>("Sprites/player_jump");
        if (deadSprite == null) deadSprite = Resources.Load<Sprite>("Sprites/player_dead");

        if (runSprites == null || runSprites.Length == 0 || runSprites[0] == null)
        {
            Sprite r1 = Resources.Load<Sprite>("Sprites/player_run_1");
            Sprite r2 = Resources.Load<Sprite>("Sprites/player_run_2");
            Sprite r3 = Resources.Load<Sprite>("Sprites/player_run_3");
            Sprite r4 = Resources.Load<Sprite>("Sprites/player_run_4");

            if (r1 != null && r2 != null && r3 != null && r4 != null)
            {
                runSprites = new Sprite[] { r1, r2, r3, r4 };
            }
        }

        // 2. Bike Riding Sprites (Anywheel Green)
        if (rideIdleSprite == null) rideIdleSprite = Resources.Load<Sprite>("Sprites/player_ride_idle");
        if (rideJumpSprite == null) rideJumpSprite = Resources.Load<Sprite>("Sprites/player_ride_jump");

        if (rideSprites == null || rideSprites.Length == 0 || rideSprites[0] == null)
        {
            Sprite rd1 = Resources.Load<Sprite>("Sprites/player_ride_1");
            Sprite rd2 = Resources.Load<Sprite>("Sprites/player_ride_2");
            Sprite rd3 = Resources.Load<Sprite>("Sprites/player_ride_3");
            Sprite rd4 = Resources.Load<Sprite>("Sprites/player_ride_4");

            if (rd1 != null && rd2 != null && rd3 != null && rd4 != null)
            {
                rideSprites = new Sprite[] { rd1, rd2, rd3, rd4 };
            }
        }

        // 3. Fallback: Search all loaded sprites by name
        Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
        foreach (var s in all)
        {
            if (s == null) continue;
            if (s.name == "player_idle" && idleSprite == null) idleSprite = s;
            else if (s.name == "player_dead" && deadSprite == null) deadSprite = s;
            else if (s.name == "player_jump" && jumpSprite == null) jumpSprite = s;
            else if (s.name == "player_ride_idle" && rideIdleSprite == null) rideIdleSprite = s;
            else if (s.name == "player_ride_jump" && rideJumpSprite == null) rideJumpSprite = s;
        }

        if (sr != null && idleSprite != null && sr.sprite == null)
        {
            sr.sprite = idleSprite;
        }
    }

    public void SetDeadPose(bool dead)
    {
        isDeadPose = dead;
        if (sr == null) return;

        if (dead)
        {
            if (deadSprite != null) sr.sprite = deadSprite;
        }
        else
        {
            if (idleSprite != null) sr.sprite = idleSprite;
        }
    }

    private void Update()
    {
        if (sr == null || isDeadPose) return;

        bool riding = controller != null && controller.IsRiding;

        // --- 1. In Air / Jumping ---
        if (rb != null && Mathf.Abs(rb.linearVelocity.y) > 0.35f)
        {
            if (riding)
            {
                if (rideJumpSprite != null) sr.sprite = rideJumpSprite;
                else if (rideSprites != null && rideSprites.Length > 0) sr.sprite = rideSprites[0];
            }
            else
            {
                if (jumpSprite != null) sr.sprite = jumpSprite;
            }
            return;
        }

        // --- 2. Moving (Running or Pedaling Bike) ---
        float inputX = Input.GetAxisRaw("Horizontal");
        float velX = rb != null ? Mathf.Abs(rb.linearVelocity.x) : 0f;
        bool isMoving = Mathf.Abs(inputX) > 0.05f || velX > 0.1f;

        if (riding)
        {
            // Bike Riding Cycle
            Sprite[] currentCycle = (rideSprites != null && rideSprites.Length > 0) ? rideSprites : runSprites;
            if (isMoving && currentCycle != null && currentCycle.Length > 0)
            {
                animTimer += Time.deltaTime;
                if (animTimer >= 1f / sprintFps)
                {
                    animTimer -= 1f / sprintFps;
                    currentFrame = (currentFrame + 1) % currentCycle.Length;
                }
                sr.sprite = currentCycle[currentFrame];
            }
            else
            {
                currentFrame = 0;
                animTimer = 0f;
                if (rideIdleSprite != null) sr.sprite = rideIdleSprite;
                else if (currentCycle != null && currentCycle.Length > 0) sr.sprite = currentCycle[0];
            }
        }
        else
        {
            // Foot Running Cycle
            if (isMoving && runSprites != null && runSprites.Length > 0)
            {
                animTimer += Time.deltaTime;
                if (animTimer >= 1f / walkFps)
                {
                    animTimer -= 1f / walkFps;
                    currentFrame = (currentFrame + 1) % runSprites.Length;
                }
                sr.sprite = runSprites[currentFrame];
            }
            else
            {
                currentFrame = 0;
                animTimer = 0f;
                if (idleSprite != null) sr.sprite = idleSprite;
            }
        }
    }
}
