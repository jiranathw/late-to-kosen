using System.Collections.Generic;
using UnityEngine;

public class FallingRock : MonoBehaviour
{
    private static readonly List<FallingRock> allRocks = new List<FallingRock>();

    [Header("Rock Settings")]
    public bool disappearAfter3Seconds = false;

    [Header("Rock Trigger")]
    public RockTrigger rockTrigger;

    private Rigidbody2D rb;
    private Vector3 startPosition;
    private Quaternion startRotation;

    private bool activated = false;
    private bool hasKilledPlayer = false;

    private void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        startPosition = transform.position;
        startRotation = transform.rotation;

        if (rb != null)
        {
            rb.bodyType = RigidbodyType2D.Kinematic;
        }
    }

    private void OnEnable()
    {
        if (!allRocks.Contains(this))
        {
            allRocks.Add(this);
        }
    }

    private void OnDisable()
    {
        allRocks.Remove(this);
    }

    public static void ResetAllRocks()
    {
        // Copy to array to avoid modification issues during iteration
        FallingRock[] rocks = allRocks.ToArray();
        foreach (var rock in rocks)
        {
            if (rock != null)
            {
                rock.ResetRock();
            }
        }

        // Also find any inactive rock objects in the scene and reset them
        RockTrigger[] triggers = Object.FindObjectsByType<RockTrigger>(FindObjectsInactive.Include, FindObjectsSortMode.None);
        foreach (var t in triggers)
        {
            if (t != null)
            {
                t.ResetTrigger();
                if (t.fallingRock != null)
                {
                    t.fallingRock.ResetRock();
                }
            }
        }
    }

    public void Activate()
    {
        if (activated) return;

        // Ensure rock starts at its exact start position
        transform.position = startPosition;
        transform.rotation = startRotation;

        if (rb != null)
        {
            rb.linearVelocity = Vector2.zero;
            rb.angularVelocity = 0f;
            rb.bodyType = RigidbodyType2D.Dynamic;
            rb.gravityScale = 3f;
        }

        activated = true;
        hasKilledPlayer = false;

        if (disappearAfter3Seconds)
        {
            CancelInvoke(nameof(HideRock));
            Invoke(nameof(HideRock), 3f);
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (!collision.gameObject.CompareTag("Player")) return;
        if (hasKilledPlayer) return;

        hasKilledPlayer = true;
        CancelInvoke(nameof(HideRock));

        // Player dies & respawns
        PlayerController player = collision.gameObject.GetComponent<PlayerController>();
        if (player != null)
        {
            player.Die();
        }
        else if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerDied();
        }

        // Reset all rocks immediately upon player death
        ResetAllRocks();
    }

    private void HideRock()
    {
        activated = false;

        if (rb != null)
        {
            rb.linearVelocity = Vector2.zero;
            rb.angularVelocity = 0f;
            rb.bodyType = RigidbodyType2D.Kinematic;
        }

        gameObject.SetActive(false);
    }

    public void ResetRock()
    {
        CancelInvoke(nameof(HideRock));

        gameObject.SetActive(true);

        transform.position = startPosition;
        transform.rotation = startRotation;

        if (rb != null)
        {
            rb.linearVelocity = Vector2.zero;
            rb.angularVelocity = 0f;
            rb.bodyType = RigidbodyType2D.Kinematic;
        }

        activated = false;
        hasKilledPlayer = false;

        if (rockTrigger != null)
        {
            rockTrigger.ResetTrigger();
        }
    }
}