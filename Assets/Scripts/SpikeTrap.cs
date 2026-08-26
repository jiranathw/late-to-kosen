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

        if (!up && Mathf.Abs(player.position.x - downPosition.x) < triggerDistance)
        {
            up = true;
            retractTimer = retractDelay;
        }

        if (up)
        {
            transform.position = Vector3.MoveTowards(transform.position, upPosition, riseSpeed * Time.deltaTime);

            retractTimer -= Time.deltaTime;
            // Only go back down once the player has actually left, otherwise it
            // retracts under their feet and the trap does nothing.
            if (retractTimer <= 0f && Mathf.Abs(player.position.x - downPosition.x) > triggerDistance * 1.5f)
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
