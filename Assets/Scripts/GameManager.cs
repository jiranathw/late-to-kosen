using UnityEngine;
using UnityEngine.SceneManagement;

// Attach this to one empty GameObject named "GameManager" in the scene.
// Everything else (player, traps, UI) talks to this through GameManager.Instance.
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Timer Settings")]
    [SerializeField] private float startingTime = 90f; // seconds before the bell rings
    public float TimeRemaining { get; private set; }

    [Header("Game State")]
    public bool IsGameOver { get; private set; }
    public int DeathCount { get; private set; }

    // Set when the run ends. DidWin tells the UI which screen to show;
    // LoseReason is a short tag ("time", etc) so we can vary the message later.
    public bool DidWin { get; private set; }
    public string LoseReason { get; private set; }

    [Header("Respawn")]
    [SerializeField] private Transform defaultSpawnPoint; // drag an empty GameObject at the level start
    private Vector3 currentCheckpoint;

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    private void Start()
    {
        TimeRemaining = startingTime;
        IsGameOver = false;
        DeathCount = 0;
        DidWin = false;
        LoseReason = null;
        currentCheckpoint = defaultSpawnPoint != null ? defaultSpawnPoint.position : Vector3.zero;
    }

    private void Update()
    {
        if (IsGameOver) return;

        TimeRemaining -= Time.deltaTime;
        if (TimeRemaining <= 0f)
        {
            TimeRemaining = 0f;
            LoseGame("time");
        }
    }

    public void SetCheckpoint(Vector3 position)
    {
        currentCheckpoint = position;
    }

    public Vector3 GetCheckpoint()
    {
        return currentCheckpoint;
    }

    public void PlayerDied()
    {
        if (IsGameOver) return;
        DeathCount++;
        Debug.Log($"Player died. Death count: {DeathCount}");
    }

    public void WinGame()
    {
        if (IsGameOver) return;
        IsGameOver = true;
        DidWin = true;
        Debug.Log("Reached school in time. Level complete!");
        // ResultUI picks this up automatically and shows the win screen.
    }

    public void LoseGame(string reason)
    {
        if (IsGameOver) return;
        IsGameOver = true;
        DidWin = false;
        LoseReason = reason;
        Debug.Log($"Game over. Reason: {reason}");
        // ResultUI picks this up automatically and shows the lose screen.
    }

    public void RestartLevel()
    {
        Scene active = SceneManager.GetActiveScene();

        // buildIndex is -1 when the scene isn't in File > Build Settings, and
        // LoadScene(-1) throws a confusing exception. Log the real cause first
        // so whoever adds a new level knows exactly what they forgot.
        if (active.buildIndex >= 0)
        {
            SceneManager.LoadScene(active.buildIndex);
        }
        else
        {
            Debug.LogWarning($"Scene '{active.name}' is not in Build Settings. Add it before building!");
            SceneManager.LoadScene(active.name);
        }
    }
}
