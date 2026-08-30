using UnityEngine;

// Wrong building.
//
// Krin's original, kept almost intact because the idea is the best troll on the
// branch: you walk into what is obviously the entrance, and you come out
// somewhere else with your checkpoint moved, so the mistake actually costs you
// the walk back. Every KOSEN student has gone to the wrong building for an exam
// at least once.
//
// Two changes from the original:
//   - the checkpoint move is now optional and defaults to the EXIT, not the
//     entrance. Krin's version set the respawn point back at the door you came
//     in, which meant dying after the teleport sent you through the teleport
//     again, forever.
//   - it moves the Rigidbody2D, not the Transform. With autoSyncTransforms off
//     (the project default) writing transform.position mid-physics-step leaves
//     the body behind for a frame and the player can land inside geometry.
[RequireComponent(typeof(Collider2D))]
public class Teleporter : MonoBehaviour
{
    [Tooltip("Where you come out, in world coordinates. A plain Vector2 rather " +
             "than a Transform on purpose: it means a teleporter is described " +
             "entirely by its own fields, with no second object in the scene " +
             "that someone can move, rename or delete without noticing.")]
    [SerializeField] private Vector2 destination;

    [Tooltip("Optional override. If set, this wins over `destination`.")]
    [SerializeField] private Transform destinationTransform;

    [SerializeField] private string playerTag = "Player";

    [Tooltip("Move the respawn point to the exit as well. On means dying after " +
             "the troll does not replay the troll.")]
    [SerializeField] private bool moveCheckpointToExit = true;

    [SerializeField] private float cooldownSeconds = 1.2f;

    [Tooltip("Fire once per life and then stay quiet. On by default, and it has " +
             "to be: the exit is BEHIND the entrance, so a repeating teleporter " +
             "bounces the player between the two points until the bell rings. " +
             "A troll you cannot walk away from is not a troll, it is a bug.")]
    [SerializeField] private bool oneShot = true;

    private float cooldownLeft;
    private bool spent;

    private Vector3 Exit => destinationTransform != null
        ? destinationTransform.position
        : new Vector3(destination.x, destination.y, 0f);

    private void Awake()
    {
        SpriteRenderer sr = GetComponent<SpriteRenderer>();
        if (sr != null)
        {
            sr.color = Color.white;
            if (sr.sprite == null || sr.sprite.name.StartsWith("Knob") || sr.sprite.name.StartsWith("Unity") || sr.sprite.name.Contains("Square"))
            {
                sr.sprite = Resources.Load<Sprite>("Sprites/spr_teleporter") ?? Resources.Load<Sprite>("Sprites/spr_heaven_door");
            }
        }
    }

    private void Start()
    {
        // Counts as a hazard survived, credited at the exit.
        GameManager.Instance?.RegisterTrap(Exit.x);
    }

    // Deliberately NOT re-armed on respawn. The exit is behind the entrance, so
    // a teleporter that comes back after a death would catch the player again
    // on the walk forward, and again, and again, without ever costing a life -
    // an unloseable, unwinnable loop. Once per stage load is the whole design:
    // you get trolled once, you learn where Building 12 actually is, you move on.
    public void Rearm()
    {
        spent = false;
        cooldownLeft = 0f;
    }

    private void Update()
    {
        if (cooldownLeft > 0f) cooldownLeft -= Time.deltaTime;
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (spent || cooldownLeft > 0f) return;
        if (!other.CompareTag(playerTag)) return;

        if (oneShot) spent = true;
        cooldownLeft = cooldownSeconds;
        Vector3 exit = Exit;

        Rigidbody2D rb = other.attachedRigidbody;
        if (rb != null)
        {
            rb.position = exit;
            rb.linearVelocity = Vector2.zero;
        }
        else
        {
            other.transform.position = exit;
        }

        if (moveCheckpointToExit) GameManager.Instance?.SetCheckpoint(exit);
    }
}
