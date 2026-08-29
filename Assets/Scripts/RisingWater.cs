using UnityEngine;

// The flood.
//
// KOSEN KMITL sits on Chalong Krung, and any student there has waded to class
// at least once. Mechanically it is the one hazard in the game that removes the
// option of standing still: everything else punishes moving badly, this
// punishes not moving at all.
//
// It is a wide trigger volume that climbs at `riseSpeed` and kills on contact.
// It starts below the level and only starts rising when tripped, so the early
// part of a stage can still be a normal platforming stretch.
[RequireComponent(typeof(BoxCollider2D))]
public class RisingWater : MonoBehaviour, ITriggerable
{
    [Header("Rise")]
    [SerializeField] private float riseSpeed = 0.62f;
    [SerializeField] private float maxHeight = 9f;
    [SerializeField] private bool risingFromStart;

    [Tooltip("World X the player has to pass before the flood starts. Leave at " +
             "a huge negative number to have it rise from the first frame.")]
    [SerializeField] private float triggerAtPlayerX = 0f;

    [Header("Look")]
    [SerializeField] private Vector2 surfaceSize = new Vector2(120f, 24f);
    [SerializeField] private Color waterColor = new Color(0.35f, 0.55f, 0.75f, 0.72f);

    [Header("Kill")]
    [SerializeField] private string playerTag = "Player";
    [Tooltip("How far below the surface the player has to be before it counts. " +
             "Small positive number, so brushing the top edge is survivable.")]
    [SerializeField] private float graceDepth = 0.35f;

    private SpriteRenderer sprite;
    private BoxCollider2D box;
    private Vector3 restPosition;
    private Transform player;
    private bool rising;

    private void Awake()
    {
        restPosition = transform.position;
        box = GetComponent<BoxCollider2D>();
        box.isTrigger = true;
        box.size = surfaceSize;

        sprite = GetComponent<SpriteRenderer>();
        if (sprite == null) sprite = gameObject.AddComponent<SpriteRenderer>();
        if (sprite.sprite == null) sprite.sprite = SolidSprite.Get();
        sprite.drawMode = SpriteDrawMode.Sliced;
        sprite.size = surfaceSize;
        sprite.color = waterColor;
        sprite.sortingOrder = 20;   // in front of the ground, so submerging reads

        rising = risingFromStart;
    }

    private void Start()
    {
        GameManager.Instance?.RegisterTrap(restPosition.x);

        // Subscribed in Start, not Awake: GameManager.Instance is assigned in
        // GameManager.Awake and script execution order between two Awakes is
        // not guaranteed.
        if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerRespawned += ResetToStart;
        }
    }

    private void OnDestroy()
    {
        if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerRespawned -= ResetToStart;
        }
    }

    public void Trigger() { rising = true; }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null || gm.IsPaused || gm.IsGameOver) return;

        if (!rising)
        {
            CheckProximity();
            return;
        }

        if (transform.position.y - restPosition.y >= maxHeight) return;

        transform.position += Vector3.up * (riseSpeed * Time.deltaTime);

        // Ripple, so it reads as water and not as a rising blue rectangle.
        float wobble = 1f + Mathf.Sin(Time.time * 2.4f) * 0.012f;
        sprite.size = new Vector2(surfaceSize.x, surfaceSize.y * wobble);
    }

    private void OnTriggerEnter2D(Collider2D other) { TryKill(other); }
    private void OnTriggerStay2D(Collider2D other)  { TryKill(other); }

    private void TryKill(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        // Surface = top edge of the box. Only drown once actually under it;
        // OnTriggerStay would otherwise kill on the first frame of contact,
        // which makes a jump that clips the surface feel like a cheat.
        float surfaceY = transform.position.y + surfaceSize.y * 0.5f;
        if (other.bounds.center.y > surfaceY - graceDepth) return;

        PlayerController player = other.GetComponent<PlayerController>();
        if (player != null) player.Die();
        else GameManager.Instance?.PlayerDied();
    }

    private void CheckProximity()
    {
        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag(playerTag);
            if (p == null) return;
            player = p.transform;
        }

        if (player.position.x >= triggerAtPlayerX) rising = true;
    }

    // The player respawned at a checkpoint that is now underwater, which is
    // unwinnable. PlayerController.Respawn does not know about this class, so
    // the water drops itself back instead.
    //
    // Position resets; `rising` deliberately does NOT. The HazardTrigger that
    // started the flood is one-shot, so clearing the flag here would mean the
    // first death permanently switches the stage-3 gimmick off and the retry is
    // a walk in the park.
    public void ResetToStart()
    {
        transform.position = restPosition;
        sprite.size = surfaceSize;
    }
}
