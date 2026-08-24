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
        Debug.Log("Reached school in time. Level complete!");
        // TODO later: show win screen / load next level
    }

    public void LoseGame(string reason)
    {
        if (IsGameOver) return;
        IsGameOver = true;
        Debug.Log($"Game over. Reason: {reason}");
        // TODO later: show lose screen
    }

    public void RestartLevel()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }
}
