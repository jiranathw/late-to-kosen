using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

// Attach this to one empty GameObject named "GameManager" in the scene.
// Everything else (player, traps, UI) talks to this through GameManager.Instance.
//
// SCOPE: this object is per-STAGE. It is destroyed and rebuilt every time a
// scene loads, which is exactly why lives, the timer and the checkpoint live
// here - all three are supposed to reset when you enter a new stage. Anything
// that has to survive a scene load belongs in GameSession instead.
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    [Header("Stage")]
    [Tooltip("1 or 2. Must match the scene: Level1 -> 1, Level2 -> 2.")]
    [SerializeField] private int levelIndex = 1;

    public int LevelIndex => Mathf.Clamp(levelIndex, 1, GameSession.LevelCount);
    public string LevelTitle => GameSession.TitleFor(LevelIndex);
    public string LevelSubtitle => GameSession.SubtitleFor(LevelIndex);
    public bool IsFinalLevel => GameSession.IsFinalLevel(LevelIndex);

    [Header("Stage Intro")]
    [SerializeField] private float introDuration = 2.2f;
    public bool IsIntroActive { get; private set; } = true;
    public float IntroDuration => introDuration;
    public float IntroRemaining => Mathf.Max(0f, introTimer);
    private float introTimer;

    [Header("Timer Settings")]
    [SerializeField] private float startingTime = 85f; // seconds before the bell rings
    public float TimeRemaining { get; private set; }
    public float StartingTime => startingTime;
    public float TimeUsed => Mathf.Max(0f, startingTime - TimeRemaining);

    [Header("Lives")]
    [SerializeField] private int startingLives = 3;
    public int Lives { get; private set; }
    public int StartingLives => startingLives;

    [Header("Score")]
    [SerializeField] private int pointsPerSecondLeft = 10;
    [SerializeField] private int pointsPerTrapSurvived = 100;
    [SerializeField] private int penaltyPerDeath = 50;

    [Header("Game State")]
    public bool IsGameOver { get; private set; }
    public bool IsPaused { get; private set; }
    public int DeathCount { get; private set; }

    // Set when the run ends. DidWin tells the UI which screen to show;
    // LoseReason is a short tag ("time" / "lives") so we can vary the message.
    public bool DidWin { get; private set; }
    public string LoseReason { get; private set; }

    [Header("Respawn")]
    [SerializeField] private Transform defaultSpawnPoint; // drag an empty GameObject at the level start
    private Vector3 currentCheckpoint;

    // --- traps survived -----------------------------------------------------
    // Every trap registers its x position at Awake. A trap counts as "survived"
    // once the player has actually got past it, which we measure with the
    // furthest x the player has ever reached. Dying ON a trap therefore never
    // scores it, and walking back and forth can never score it twice.
    private readonly List<float> trapPositions = new List<float>();
    private Transform playerTransform;
    private float playerMaxX = float.NegativeInfinity;
    private const float PastTrapMargin = 0.6f;

    public int TrapTotal => trapPositions.Count;

    public int TrapsSurvived
    {
        get
        {
            int n = 0;
            for (int i = 0; i < trapPositions.Count; i++)
            {
                if (trapPositions[i] + PastTrapMargin < playerMaxX) n++;
            }
            return n;
        }
    }

    public int Score
    {
        get
        {
            int raw = Mathf.FloorToInt(TimeRemaining) * pointsPerSecondLeft
                    + TrapsSurvived * pointsPerTrapSurvived
                    - DeathCount * penaltyPerDeath;
            return Mathf.Max(0, raw);
        }
    }

    public void RegisterTrap(float worldX)
    {
        trapPositions.Add(worldX);
    }

    // ------------------------------------------------------------------------

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;

        // A previous run may have left the game paused. Scene reload does not
        // reset timeScale, so a stale 0 here would freeze the new run forever.
        Time.timeScale = 1f;
    }

    private void Start()
    {
        TimeRemaining = startingTime;
        Lives = startingLives;
        IsGameOver = false;
        IsPaused = false;
        DeathCount = 0;
        DidWin = false;
        LoseReason = null;
        currentCheckpoint = defaultSpawnPoint != null ? defaultSpawnPoint.position : Vector3.zero;

        IsIntroActive = true;
        introTimer = introDuration;

        GameObject p = GameObject.FindGameObjectWithTag("Player");
        if (p != null)
        {
            playerTransform = p.transform;
            playerMaxX = playerTransform.position.x;
        }
    }

    private void Update()
    {
        if (IsGameOver || IsPaused) return;

        if (IsIntroActive)
        {
            introTimer -= Time.deltaTime;
            if (introTimer <= 0f)
            {
                introTimer = 0f;
                IsIntroActive = false;
            }
            return;
        }

        if (playerTransform != null)
        {
            playerMaxX = Mathf.Max(playerMaxX, playerTransform.position.x);
        }

        TimeRemaining -= Time.deltaTime;
        if (TimeRemaining <= 0f)
        {
            TimeRemaining = 0f;
            LoseGame("time");
        }
    }

    // --- pause --------------------------------------------------------------

    public void TogglePause()
    {
        if (IsGameOver) return;
        SetPaused(!IsPaused);
    }

    public void SetPaused(bool paused)
    {
        if (IsGameOver) return;
        IsPaused = paused;
        Time.timeScale = paused ? 0f : 1f;
    }

    // --- timer --------------------------------------------------------------

    // Burn seconds off the clock. Used by trolls whose punishment is time
    // rather than a life - FakeGoal is the only one right now. Routed through
    // LoseGame like the normal countdown is, so "the bell rang" stays a
    // single-entry code path no matter what took the last second.
    public void SpendTime(float seconds)
    {
        if (IsGameOver || seconds <= 0f) return;

        TimeRemaining -= seconds;
        if (TimeRemaining <= 0f)
        {
            TimeRemaining = 0f;
            LoseGame("time");
        }
    }

    // --- respawn notification -----------------------------------------------

    // Raised after the player has been put back at a checkpoint. Hazards that
    // carry state across a death subscribe to this and undo themselves.
    // RisingWater is the reason it exists: respawning at a checkpoint that is
    // already nine metres underwater is not a level, it is a cutscene about
    // drowning.
    public event System.Action PlayerRespawned;

    public void NotifyRespawned()
    {
        PlayerRespawned?.Invoke();
    }

    // --- state transitions --------------------------------------------------

    public void SetCheckpoint(Vector3 position)
    {
        currentCheckpoint = position;
    }

    public Vector3 GetCheckpoint()
    {
        return currentCheckpoint;
    }

    [Header("Testing")]
    [Tooltip("Keep true during development so deaths always respawn without game over screen")]
    [SerializeField] private bool infiniteLives = true;

    // Returns true if the player still has a life left and should respawn.
    // Returns false when that was the last life, i.e. the run is over.
    public bool PlayerDied()
    {
        if (IsGameOver) return false;

        DeathCount++;
        if (!infiniteLives)
        {
            Lives--;
            if (Lives <= 0)
            {
                Lives = 0;
                LoseGame("lives");
                return false;
            }
        }
        return true;
    }

    public void WinGame()
    {
        if (IsGameOver) return;
        // The form's win condition: reach school in time AND still have a life.
        // Lives can only be 0 once LoseGame has already fired, so reaching here
        // always means at least one life is left - but assert it anyway.
        if (Lives <= 0) return;

        IsGameOver = true;
        DidWin = true;
        Time.timeScale = 1f;

        AudioManager.Instance?.PlayStageClearSFX();
        GameSession.Instance?.RecordClear(LevelIndex, Score, DeathCount, TimeUsed);
    }

    public void LoseGame(string reason)
    {
        if (IsGameOver) return;
        IsGameOver = true;
        IsPaused = false;
        DidWin = false;
        LoseReason = reason;
        Time.timeScale = 1f;

        // Banked now rather than on restart, because the player may quit from
        // the result screen instead of retrying, and the deaths still happened.
        GameSession.Instance?.RecordFailedAttempt(LevelIndex, DeathCount);
    }

    // --- level flow ---------------------------------------------------------

    // Stage cleared and there is another one. Called from the result screen.
    public void NextLevel()
    {
        if (!IsGameOver || !DidWin || IsFinalLevel) return;

        GameSession session = GameSession.Instance;
        if (session == null)
        {
            Debug.LogError("No GameSession - cannot advance. Is GameSession.cs in Assets/Scripts?");
            return;
        }
        session.LoadLevel(LevelIndex + 1);
    }

    // Retry the current stage only. Lives come back to full because the new
    // scene builds a fresh GameManager; that is the whole point of the split.
    public void RestartLevel()
    {
        Time.timeScale = 1f;
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

    // Wipe the run and go back to stage 1. Offered on the final results screen.
    public void RestartRun()
    {
        Time.timeScale = 1f;
        GameSession session = GameSession.Instance;
        if (session != null) session.StartNewRun();
        else RestartLevel();
    }

    public void QuitGame()
    {
        Time.timeScale = 1f;
#if UNITY_EDITOR
        UnityEditor.EditorApplication.isPlaying = false;
#else
        Application.Quit();
#endif
    }
}
