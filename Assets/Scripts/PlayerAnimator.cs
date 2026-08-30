using UnityEngine;

// Cycles through 8-bit sprite frames for the KOSEN student based on movement.
// Handles walking/running foot-stepping animation, air/jump pose, and knocked-out death pose.
[RequireComponent(typeof(SpriteRenderer))]
[RequireComponent(typeof(PlayerController))]
public class PlayerAnimator : MonoBehaviour
{
    [Header("Sprites")]
    [SerializeField] private Sprite idleSprite;
    [SerializeField] private Sprite[] runSprites;
    [SerializeField] private Sprite jumpSprite;
    [SerializeField] private Sprite deadSprite;

    [Header("Frame Rate")]
    [SerializeField] private float walkFps = 9f;
    [SerializeField] private float sprintFps = 14f;

    private SpriteRenderer sr;
    private Rigidbody2D rb;
    private PlayerController controller;
    private float animTimer;
    private int currentRunFrame;
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
        // 1. Try loading from Resources/Sprites/
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

        // 2. Fallback: Search all loaded sprites by name
        if (idleSprite == null || runSprites == null || runSprites.Length == 0 || deadSprite == null)
        {
            Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
            Sprite r1 = null, r2 = null, r3 = null, r4 = null;
            foreach (var s in all)
            {
                if (s == null) continue;
                if (s.name == "player_idle" && idleSprite == null) idleSprite = s;
                else if (s.name == "player_dead" && deadSprite == null) deadSprite = s;
                else if (s.name == "player_run_1") r1 = s;
                else if (s.name == "player_run_2") r2 = s;
                else if (s.name == "player_run_3") r3 = s;
                else if (s.name == "player_run_4") r4 = s;
                else if (s.name == "player_jump" && jumpSprite == null) jumpSprite = s;
            }
            if (r1 != null && r2 != null && r3 != null && r4 != null)
            {
                runSprites = new Sprite[] { r1, r2, r3, r4 };
            }
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

        // In air / jumping
        if (rb != null && Mathf.Abs(rb.linearVelocity.y) > 0.35f)
        {
            if (jumpSprite != null) sr.sprite = jumpSprite;
            return;
        }

        // Running / Walking state
        float inputX = Input.GetAxisRaw("Horizontal");
        float velX = rb != null ? Mathf.Abs(rb.linearVelocity.x) : 0f;

        if ((Mathf.Abs(inputX) > 0.05f || velX > 0.1f) && runSprites != null && runSprites.Length > 0)
        {
            float fps = (controller != null && controller.IsRiding) ? sprintFps : walkFps;
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
