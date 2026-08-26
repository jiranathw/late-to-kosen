using UnityEngine;

// TROLL TRAP TYPE 2 - the platform that isn't.
//
// Looks and behaves exactly like Ground: same layer, same solid collider, so
// the player's ground check accepts it and they can stand and jump on it.
// A moment after they land it wobbles as a warning, then drops out of the
// world. It never kills directly - the fall does that, which is much funnier.
//
// Put these over a pit. Over solid ground they are just decoration.
[RequireComponent(typeof(Collider2D))]
public class FakePlatform : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";
    [SerializeField] private float delayBeforeFalling = 0.35f;
    [SerializeField] private float wobbleAmount = 0.06f;
    [SerializeField] private float wobbleSpeed = 60f;
    [SerializeField] private float fallGravity = 4f;
    [SerializeField] private float destroyAfter = 2.5f;

    private Vector3 restPosition;
    private bool triggered;

    private void Awake()
    {
        restPosition = transform.position;
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (triggered) return;
        if (!collision.collider.CompareTag(playerTag)) return;

        // Only if they landed on top of it. Clipping the side shouldn't set it off.
        foreach (ContactPoint2D contact in collision.contacts)
        {
            if (contact.normal.y < -0.5f) // normal points from player into platform
            {
                triggered = true;
                StartCoroutine(Collapse());
                return;
            }
        }
    }

    private System.Collections.IEnumerator Collapse()
    {
        float t = 0f;
        while (t < delayBeforeFalling)
        {
            t += Time.deltaTime;
            float offset = Mathf.Sin(t * wobbleSpeed) * wobbleAmount;
            transform.position = restPosition + new Vector3(offset, 0f, 0f);
            yield return null;
        }
        transform.position = restPosition;

        Collider2D col = GetComponent<Collider2D>();
        if (col != null) col.enabled = false;

        Rigidbody2D rb = GetComponent<Rigidbody2D>();
        if (rb == null) rb = gameObject.AddComponent<Rigidbody2D>();
        rb.bodyType = RigidbodyType2D.Dynamic;
        rb.gravityScale = fallGravity;

        Destroy(gameObject, destroyAfter);
    }
}
