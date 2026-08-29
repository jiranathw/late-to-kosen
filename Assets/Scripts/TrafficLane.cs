using UnityEngine;
using System.Collections.Generic;

// A lane of Chalong Krung Road.
//
// Place one empty GameObject per lane. It spawns vehicles at one end on a
// timer, they drive across, and the player has to read the gaps. This is the
// stage-2 gimmick: unlike every other hazard in the game it is not memorised,
// it is timed, so replaying stage 2 never feels like replaying a solved puzzle.
//
// The rhythm is deliberately regular rather than random. Random traffic can
// deal an unclearable hand, and "the game rolled badly" is the one failure a
// player will not forgive. A fixed period with a fixed gap is always solvable
// and still requires timing.
public class TrafficLane : MonoBehaviour
{
    [Header("Lane geometry")]
    [Tooltip("Where vehicles appear. Negative speed spawns on the right.")]
    [SerializeField] private float laneLength = 26f;

    [Tooltip("Signed. Negative = traffic coming from the right, which is the " +
             "side a Thai player instinctively looks at last.")]
    [SerializeField] private float speed = -6.5f;

    [Header("Rhythm")]
    [SerializeField] private float spawnEverySeconds = 2.2f;
    [SerializeField] private float firstSpawnDelay = 0.4f;

    [Header("Vehicle")]
    [SerializeField] private Vector2 vehicleSize = new Vector2(1.8f, 0.9f);
    [SerializeField] private Color vehicleColor = new Color(0.95f, 0.75f, 0.2f, 1f);
    [SerializeField] private Sprite vehicleSprite;
    [SerializeField] private string playerTag = "Player";

    [Header("Activation")]
    [Tooltip("Vehicles only spawn once the player is within this many units. " +
             "Keeps 40 objects from driving around at the far end of the level.")]
    [SerializeField] private float activationRange = 30f;

    private readonly Stack<Vehicle> pool = new Stack<Vehicle>();
    private readonly List<Vehicle> live = new List<Vehicle>();
    private Transform player;
    private float timer;

    private float SpawnX  => transform.position.x + (speed < 0f ?  laneLength * 0.5f : -laneLength * 0.5f);
    private float DespawnX => transform.position.x + (speed < 0f ? -laneLength * 0.5f :  laneLength * 0.5f);

    private void Start()
    {
        timer = firstSpawnDelay;

        // The lane as a whole is one "trap" for scoring, credited at its far
        // edge so you only bank it once you are actually across.
        GameManager.Instance?.RegisterTrap(transform.position.x + 1f);

        GameObject p = GameObject.FindGameObjectWithTag(playerTag);
        if (p != null) player = p.transform;
    }

    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null || gm.IsPaused || gm.IsGameOver) return;

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag(playerTag);
            if (p != null) player = p.transform;
        }

        bool near = player == null ||
                    Mathf.Abs(player.position.x - transform.position.x) <= activationRange;

        if (!near)
        {
            // Clear the lane rather than leaving vehicles frozen mid-road: the
            // player is about to arrive and a stopped bike reads as scenery.
            for (int i = live.Count - 1; i >= 0; i--) Recycle(live[i]);
            timer = firstSpawnDelay;
            return;
        }

        timer -= Time.deltaTime;
        if (timer <= 0f)
        {
            timer += spawnEverySeconds;
            Spawn();
        }
    }

    private void Spawn()
    {
        Vehicle v = pool.Count > 0 ? pool.Pop() : Create();
        v.transform.position = new Vector3(SpawnX, transform.position.y, 0f);
        v.gameObject.SetActive(true);
        v.Launch(this, speed, DespawnX, playerTag);
        live.Add(v);
    }

    private Vehicle Create()
    {
        GameObject go = new GameObject($"{name}_Vehicle");
        go.transform.SetParent(transform, true);
        go.transform.localScale = Vector3.one;

        SpriteRenderer sr = go.AddComponent<SpriteRenderer>();
        sr.sprite = vehicleSprite != null ? vehicleSprite : SolidSprite.Get();
        sr.color = vehicleColor;
        sr.sortingOrder = 6;
        sr.drawMode = SpriteDrawMode.Sliced;
        sr.size = vehicleSize;

        BoxCollider2D box = go.AddComponent<BoxCollider2D>();
        box.size = vehicleSize;
        box.isTrigger = true;

        return go.AddComponent<Vehicle>();
    }

    public void Recycle(Vehicle v)
    {
        if (v == null) return;
        live.Remove(v);
        v.gameObject.SetActive(false);
        pool.Push(v);
    }

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = new Color(1f, 0.6f, 0.1f, 0.8f);
        Vector3 c = transform.position;
        Gizmos.DrawWireCube(c, new Vector3(laneLength, vehicleSize.y, 0.1f));
    }
}
