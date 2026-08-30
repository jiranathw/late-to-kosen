using UnityEngine;
using UnityEngine.SceneManagement;

// Self-bootstraps background music for each stage.
// BGM loops continuously with smooth volume control.
public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }

    public enum Stage1Track
    {
        MorningPanic,   // Fast, chaotic 8:25 AM rush
        StreetSprint,   // Funky, driving street sprint
        CampusHero      // Melodic, heroic 8-bit theme
    }

    [Header("BGM Tracks for Stage 1 (Select one)")]
    [SerializeField] private Stage1Track selectedStage1Track = Stage1Track.MorningPanic;
    [Range(0f, 1f)]
    [SerializeField] private float musicVolume = 0.45f;

    private AudioSource bgmSource;
    private AudioClip stage1Clip;
    private AudioClip stage2Clip;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (Instance == null)
        {
            GameObject go = new GameObject("AudioManager");
            DontDestroyOnLoad(go);
            Instance = go.AddComponent<AudioManager>();
        }
        Instance.OnSceneReady();
    }

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        bgmSource = gameObject.AddComponent<AudioSource>();
        bgmSource.loop = true;
        bgmSource.playOnAwake = false;
        bgmSource.volume = musicVolume;

        LoadAudioClips();

        SceneManager.sceneLoaded += (scene, mode) => OnSceneReady();
    }

    private void LoadAudioClips()
    {
        string t1Name = "bgm_stage1_morning_panic";
        switch (selectedStage1Track)
        {
            case Stage1Track.StreetSprint:
                t1Name = "bgm_stage1_street_sprint";
                break;
            case Stage1Track.CampusHero:
                t1Name = "bgm_stage1_campus_hero";
                break;
            case Stage1Track.MorningPanic:
            default:
                t1Name = "bgm_stage1_morning_panic";
                break;
        }

        stage1Clip = Resources.Load<AudioClip>("Audio/" + t1Name);
        if (stage1Clip == null)
        {
            // Fallback search
            AudioClip[] all = Resources.FindObjectsOfTypeAll<AudioClip>();
            foreach (var clip in all)
            {
                if (clip != null && clip.name == t1Name)
                {
                    stage1Clip = clip;
                    break;
                }
            }
        }
    }

    public void SwitchStage1Track(Stage1Track newTrack)
    {
        selectedStage1Track = newTrack;
        LoadAudioClips();
        if (SceneManager.GetActiveScene().name == "Level1")
        {
            PlayBGM(stage1Clip);
        }
    }

    private void OnSceneReady()
    {
        string sceneName = SceneManager.GetActiveScene().name;
        if (bgmSource == null) return;

        LoadAudioClips();

        if (sceneName == "Level1")
        {
            if (stage1Clip != null && bgmSource.clip != stage1Clip)
            {
                PlayBGM(stage1Clip);
            }
        }
        else if (sceneName == "Level2" || sceneName == "Level1_Krin")
        {
            // In stage 2, keep playing energetic stage BGM or stage 1 track
            if (stage1Clip != null && !bgmSource.isPlaying)
            {
                PlayBGM(stage1Clip);
            }
        }
    }

    public void PlayBGM(AudioClip clip)
    {
        if (clip == null || bgmSource == null) return;
        if (bgmSource.clip == clip && bgmSource.isPlaying) return;

        bgmSource.clip = clip;
        bgmSource.volume = musicVolume;
        bgmSource.Play();
    }

    public void StopBGM()
    {
        if (bgmSource != null) bgmSource.Stop();
    }

    public void SetVolume(float vol)
    {
        musicVolume = Mathf.Clamp01(vol);
        if (bgmSource != null) bgmSource.volume = musicVolume;
    }
}
