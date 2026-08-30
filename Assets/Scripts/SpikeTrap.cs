using UnityEngine;

// TROLL TRAP TYPE 3 - the one that comes up out of the floor.
//
// Waits hidden below the platform surface. When the player walks within
// triggerDistance it shoots up and kills whatever is standing there. Unlike
// HiddenTrap it gives you a few frames of warning, so an alert player who is
// already sprinting can sometimes clear it - which is the point.
[RequireComponent(typeof(Collider2D))]
public class SpikeTrap : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private float triggerDistance = 2.2f;
    [SerializeField] private float riseHeight = 1.1f;
    [SerializeField] private float riseSpeed = 14f;
    [SerializeField] private float retractDelay = 1.2f;
    [SerializeField] private float retractSpeed = 3f;

    // SAME STOREY ONLY.
    //
    // The arming test used to be horizontal distance alone, and on a stacked
    // stage that is not enough: stage 1 is a stairwell where every x is spanned
    // by four floors, so Spike_02_Riser at (10, 10) sat directly under Hall_3
    // and Room_Floor and shot up whenever the player walked past overhead. You
    // then watched the trap you were about to walk into spring twice, from two
    // floors up, which is the opposite of the point.
    //
    // A spike rests half a unit under its own surface, so the player standing on
    // it is +1.0 away and at the top of a full jump is +4.11. The floor above
    // puts them at +6.0 and the floor below at -4.0, so requiring the player to
    // be above the spike and inside one floor's spacing separates all three.
    [SerializeField] private float armWithinHeight = 5f;

    private Vector3 downPosition;
    private Vector3 upPosition;
    private Transform player;
    private float retractTimer;
    private bool up;

    private void Awake()
    {
        downPosition = transform.position;
        upPosition = downPosition + Vector3.up * riseHeight;
    }

    private void Start()
    {
        GameManager.Instance?.RegisterTrap(transform.position.x);

        GameObject p = GameObject.FindGameObjectWithTag(playerTag);
        if (p != null) player = p.transform;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm != null && (gm.IsGameOver || gm.IsPaused)) return;
        if (player == null) return;

        float dy = player.position.y - downPosition.y;
        bool sameStorey = dy >= 0f && dy <= armWithinHeight;

        if (!up && sameStorey &&
            Mathf.Abs(player.position.x - downPosition.x) < triggerDistance)
        {
            up = true;
            retractTimer = retractDelay;
        }

        if (up)
        {
            transform.position = Vector3.MoveTowards(transform.position, upPosition, riseSpeed * Time.deltaTime);

            retractTimer -= Time.deltaTime;
            // Only go back down once the player has actually left, otherwise it
            // retracts under their feet and the trap does nothing. Leaving the
            // storey counts as leaving - it is how the spike re-hides itself
            // after a death sends the player back to a checkpoint below.
            bool gone = !sameStorey ||
                        Mathf.Abs(player.position.x - downPosition.x) > triggerDistance * 1.5f;
            if (retractTimer <= 0f && gone)
            {
                up = false;
            }
        }
        else
        {
            transform.position = Vector3.MoveTowards(transform.position, downPosition, retractSpeed * Time.deltaTime);
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        // A resting spike is scenery. Its collider fills the slab and its top
        // edge is flush with the walking surface, so without this guard simply
        // stepping onto the tile kills you before the trap has done anything -
        // which reads as a bug, not a troll. It only bites once it is moving.
        if (!up) return;
        if (!other.CompareTag(playerTag)) return;

        PlayerController pc = other.GetComponent<PlayerController>();
        if (pc != null) pc.Die();
        else GameManager.Instance?.PlayerDied();
    }

    private void OnTriggerStay2D(Collider2D other)
    {
        // Rising into a player who is already standing on the spot never fires
        // OnTriggerEnter, because the collider was already overlapping.
        if (!up) return;
        OnTriggerEnter2D(other);
    }
}
