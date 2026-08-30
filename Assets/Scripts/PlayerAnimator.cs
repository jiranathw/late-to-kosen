using UnityEngine;

// Cycles through 8-bit sprite frames for the selected KOSEN student character based on movement.
// Supports 3 selectable uniforms (Formal White Shirt, PE Sport Orange, Workshop Dark Navy)
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

        LoadSelectedCharacterSprites();
    }

    public void LoadSelectedCharacterSprites()
    {
        int charId = PlayerPrefs.GetInt("SelectedCharacter", 0);
        string prefix = $"Sprites/char_{charId}_";

        // 1. Foot Sprites for Selected Character
        idleSprite = Resources.Load<Sprite>(prefix + "idle") ?? Resources.Load<Sprite>("Sprites/player_idle");
        jumpSprite = Resources.Load<Sprite>(prefix + "jump") ?? Resources.Load<Sprite>("Sprites/player_jump");
        deadSprite = Resources.Load<Sprite>(prefix + "dead") ?? Resources.Load<Sprite>("Sprites/player_dead");

        Sprite r1 = Resources.Load<Sprite>(prefix + "run_1") ?? Resources.Load<Sprite>("Sprites/player_run_1");
        Sprite r2 = Resources.Load<Sprite>(prefix + "run_2") ?? Resources.Load<Sprite>("Sprites/player_run_2");
        Sprite r3 = Resources.Load<Sprite>(prefix + "run_3") ?? Resources.Load<Sprite>("Sprites/player_run_3");
        Sprite r4 = Resources.Load<Sprite>(prefix + "run_4") ?? Resources.Load<Sprite>("Sprites/player_run_4");

        if (r1 != null && r2 != null && r3 != null && r4 != null)
        {
            runSprites = new Sprite[] { r1, r2, r3, r4 };
        }

        // 2. Bike Riding Sprites (Anywheel Green) for Selected Character
        rideIdleSprite = Resources.Load<Sprite>(prefix + "ride_idle") ?? Resources.Load<Sprite>("Sprites/player_ride_idle");
        rideJumpSprite = Resources.Load<Sprite>(prefix + "ride_jump") ?? Resources.Load<Sprite>("Sprites/player_ride_jump");

        Sprite rd1 = Resources.Load<Sprite>(prefix + "ride_1") ?? Resources.Load<Sprite>("Sprites/player_ride_1");
        Sprite rd2 = Resources.Load<Sprite>(prefix + "ride_2") ?? Resources.Load<Sprite>("Sprites/player_ride_2");
        Sprite rd3 = Resources.Load<Sprite>(prefix + "ride_3") ?? Resources.Load<Sprite>("Sprites/player_ride_3");
        Sprite rd4 = Resources.Load<Sprite>(prefix + "ride_4") ?? Resources.Load<Sprite>("Sprites/player_ride_4");

        if (rd1 != null && rd2 != null && rd3 != null && rd4 != null)
        {
            rideSprites = new Sprite[] { rd1, rd2, rd3, rd4 };
        }

        // 3. Fallback search if needed
        if (idleSprite == null || runSprites == null || runSprites.Length == 0)
        {
            Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
            foreach (var s in all)
            {
                if (s == null) continue;
                if (s.name == $"char_{charId}_idle" || (idleSprite == null && s.name == "player_idle")) idleSprite = s;
                else if (s.name == $"char_{charId}_dead" || (deadSprite == null && s.name == "player_dead")) deadSprite = s;
                else if (s.name == $"char_{charId}_jump" || (jumpSprite == null && s.name == "player_jump")) jumpSprite = s;
            }
        }

        if (sr != null && idleSprite != null)
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
