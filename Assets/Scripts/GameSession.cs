using UnityEngine;
using UnityEngine.SceneManagement;

// The run. Survives scene loads; GameManager does not.
//
// "Late to KOSEN" is two stages of one morning, so there are two different
// scopes of state and mixing them up is the classic bug in a level-based game:
//
//   per STAGE  (GameManager, rebuilt every scene) - lives, timer, checkpoint
//   per RUN    (GameSession, this class)          - total score, total deaths
//
// Lives deliberately live in the per-stage scope. Running out of lives in stage
// 2 restarts stage 2, not the whole morning, so a bad stretch costs you seconds
// instead of costing you the run. That was the actual complaint about the old
// single-level build: a checkpoint saved your position but never gave a life
// back, so the third death always meant starting over from x = -7.
//
// Nothing in the scene references this class. It bootstraps itself, exactly
// like HudUI / PauseMenu / ResultUI, so pressing Play on Level2.unity directly
// works and there is no object anyone can delete by accident.
public class GameSession : MonoBehaviour
{
    // Two stages. Stage 3 was cut on the evening of 28 Aug: the team took Krin's level as
    // stage 2 and built the dorm-to-building run as stage 1, which left the
    // third stage with no story to tell and three days to tell it in.
    public const int LevelCount = 2;

    public static GameSession Instance { get; private set; }

    // Scene names must match the file names in Assets/Scenes and the entries in
    // File > Build Settings. Index 0 here is stage 1.
    public static readonly string[] SceneNames = { "Level1", "Level2" };

    public static readonly string[] Titles =
    {
        "LATE",
        "INSIDE",
    };

    public static readonly string[] Subtitles =
    {
        "07:42  -  your room to the gate of Building 12",
        "07:54  -  the building, and it is not done with you",
    };

    private readonly int[] levelScore = new int[LevelCount];
    private readonly int[] levelDeaths = new int[LevelCount];
    private readonly float[] levelTimeUsed = new float[LevelCount];
    private readonly bool[] levelCleared = new bool[LevelCount];

    // Highest stage the player has actually unlocked this run. Used by nothing
    // yet, but it is the one number a stage-select screen would need, and it is
    // free to keep correct now rather than reconstruct later.
    public int FurthestLevel { get; private set; } = 1;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (Instance != null) return;

        GameObject host = new GameObject("~GameSession");
        DontDestroyOnLoad(host);
        Instance = host.AddComponent<GameSession>();
    }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
    }

    // --- totals -------------------------------------------------------------

    public int TotalScore
    {
        get
        {
            int n = 0;
            for (int i = 0; i < LevelCount; i++) n += levelScore[i];
            return n;
        }
    }

    public int TotalDeaths
    {
        get
        {
            int n = 0;
            for (int i = 0; i < LevelCount; i++) n += levelDeaths[i];
            return n;
        }
    }

    public float TotalTimeUsed
    {
        get
        {
            float t = 0f;
            for (int i = 0; i < LevelCount; i++) t += levelTimeUsed[i];
            return t;
        }
    }

    public int LevelsCleared
    {
        get
        {
            int n = 0;
            for (int i = 0; i < LevelCount; i++) if (levelCleared[i]) n++;
            return n;
        }
    }

    public int ScoreFor(int level) => Valid(level) ? levelScore[level - 1] : 0;
    public int DeathsFor(int level) => Valid(level) ? levelDeaths[level - 1] : 0;
    public float TimeUsedFor(int level) => Valid(level) ? levelTimeUsed[level - 1] : 0f;
    public bool ClearedLevel(int level) => Valid(level) && levelCleared[level - 1];

    // --- recording ----------------------------------------------------------

    // Called by GameManager the moment a stage is cleared.
    //
    // Score and time are OVERWRITTEN: they describe the attempt that actually
    // worked, so replaying stage 2 replaces its old score instead of stacking a
    // second copy on top of it. Deaths ACCUMULATE: they describe the morning as
    // a whole, and pretending the six failed attempts never happened would let
    // the player launder a bad run by retrying until the last attempt is clean.
    public void RecordClear(int level, int score, int deaths, float timeUsed)
    {
        if (!Valid(level)) return;

        int i = level - 1;
        levelScore[i] = score;
        levelDeaths[i] += deaths;
        levelTimeUsed[i] = timeUsed;
        levelCleared[i] = true;

        if (level + 1 > FurthestLevel && level < LevelCount) FurthestLevel = level + 1;
    }

    // A failed attempt still costs you deaths. Time is not charged, because the
    // stage timer restarts from full, and no score is banked, because you did
    // not finish.
    public void RecordFailedAttempt(int level, int deaths)
    {
        if (!Valid(level)) return;
        levelDeaths[level - 1] += deaths;
    }

    public void ResetRun()
    {
        for (int i = 0; i < LevelCount; i++)
        {
            levelScore[i] = 0;
            levelDeaths[i] = 0;
            levelTimeUsed[i] = 0f;
            levelCleared[i] = false;
        }
        FurthestLevel = 1;
    }

    // --- flow ---------------------------------------------------------------

    public static bool IsFinalLevel(int level) => level >= LevelCount;

    public static string TitleFor(int level) =>
        Valid(level) ? Titles[level - 1] : "STAGE";

    public static string SubtitleFor(int level) =>
        Valid(level) ? Subtitles[level - 1] : string.Empty;

    public static string SceneNameFor(int level) =>
        Valid(level) ? SceneNames[level - 1] : SceneNames[0];

    public void LoadLevel(int level)
    {
        if (!Valid(level)) level = 1;
        Time.timeScale = 1f;
        LoadByName(SceneNameFor(level));
    }

    public void StartNewRun()
    {
        ResetRun();
        LoadLevel(1);
    }

    // LoadScene(string) throws if the scene is not in Build Settings, and the
    // exception it throws does not say which scene or why. Check first and say
    // it plainly, because "I added the scene and forgot Build Settings" is
    // the single most likely way this breaks for someone else on the team.
    private static void LoadByName(string sceneName)
    {
        if (Application.CanStreamedLevelBeLoaded(sceneName))
        {
            SceneManager.LoadScene(sceneName);
            return;
        }

        Debug.LogError(
            $"Scene '{sceneName}' is not in File > Build Settings. " +
            "Add Level1 and Level2 in that order, then press Play again.");

        // Falling back to a reload of the current scene beats freezing on a
        // result screen that no longer responds to anything.
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
    }

    private static bool Valid(int level) => level >= 1 && level <= LevelCount;
}
