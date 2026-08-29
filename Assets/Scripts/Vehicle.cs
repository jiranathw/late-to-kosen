using UnityEngine;

// One motorbike, songthaew or pickup on Chalong Krung Road.
//
// Spawned and owned by TrafficLane; you never place one of these by hand. It
// drives in a straight line, kills the player on contact, and reports back to
// the lane when it leaves the screen so the lane can recycle it.
public class Vehicle : MonoBehaviour
{
    private TrafficLane lane;
    private float speed;      // signed: negative drives left
    private float despawnX;
    private string playerTag = "Player";

    public void Launch(TrafficLane owner, float signedSpeed, float despawnAtX, string tagToKill)
    {
        lane = owner;
        speed = signedSpeed;
        despawnX = despawnAtX;
        playerTag = tagToKill;

        // Face the way it is going. Bun's sprite will be drawn facing right.
        Vector3 s = transform.localScale;
        s.x = Mathf.Abs(s.x) * (speed < 0f ? -1f : 1f);
        transform.localScale = s;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null || gm.IsPaused || gm.IsGameOver) return;

        transform.position += Vector3.right * (speed * Time.deltaTime);

        bool gone = speed < 0f ? transform.position.x < despawnX
                               : transform.position.x > despawnX;
        if (gone) Recycle();
    }

    private void OnTriggerEnter2D(Collider2D other) { TryKill(other); }
    private void OnCollisionEnter2D(Collision2D c)  { TryKill(c.collider); }

    private void TryKill(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        PlayerController player = other.GetComponent<PlayerController>();
        if (player != null) player.Die();
        else GameManager.Instance?.PlayerDied();
    }

    private void Recycle()
    {
        if (lane != null) lane.Recycle(this);
        else Destroy(gameObject);
    }
}
