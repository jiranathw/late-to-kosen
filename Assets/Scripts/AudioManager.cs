using UnityEngine;
using UnityEngine.SceneManagement;

// Self-bootstraps background music and 8-bit sound effects.
// BGM loops continuously while SFX play independently on a separate audio source.
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
    [Range(0f, 1f)]
    [SerializeField] private float sfxVolume = 0.65f;

    private AudioSource bgmSource;
    private AudioSource sfxSource;

    private AudioClip stage1Clip;
    private AudioClip stage2Clip;

    private AudioClip jumpClip;
    private AudioClip deathClip;
    private AudioClip respawnClip;
    private AudioClip stageClearClip;

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

        sfxSource = gameObject.AddComponent<AudioSource>();
        sfxSource.loop = false;
        sfxSource.playOnAwake = false;
        sfxSource.volume = sfxVolume;

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

        stage1Clip = LoadClip("Audio/" + t1Name);
        stage2Clip = LoadClip("Audio/bgm_stage2_school_corridor");

        jumpClip = LoadClip("Audio/sfx_jump");
        deathClip = LoadClip("Audio/sfx_death");
        respawnClip = LoadClip("Audio/sfx_respawn");
        stageClearClip = LoadClip("Audio/sfx_stage_clear");
    }

    private AudioClip LoadClip(string resourcePath)
    {
        AudioClip clip = Resources.Load<AudioClip>(resourcePath);
        if (clip != null) return clip;

        string simpleName = System.IO.Path.GetFileName(resourcePath);
        AudioClip[] all = Resources.FindObjectsOfTypeAll<AudioClip>();
        foreach (var c in all)
        {
            if (c != null && c.name == simpleName) return c;
        }
        return null;
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

        if (sceneName == "Level1" || sceneName == "MainMenu")
        {
            if (stage1Clip != null && bgmSource.clip != stage1Clip)
            {
                PlayBGM(stage1Clip);
            }
        }
        else if (sceneName == "Level2" || sceneName == "Level1_Krin")
        {
            AudioClip target = stage2Clip != null ? stage2Clip : stage1Clip;
            if (target != null && bgmSource.clip != target)
            {
                PlayBGM(target);
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

    // --- SFX Playback Methods ---

    public void PlayJumpSFX()
    {
        PlaySFX(jumpClip, 0.55f);
    }

    public void PlayDeathSFX()
    {
        PlaySFX(deathClip, 0.85f);
    }

    public void PlayRespawnSFX()
    {
        PlaySFX(respawnClip, 0.75f);
    }

    public void PlayStageClearSFX()
    {
        PlaySFX(stageClearClip, 0.90f);
    }

    public void PlaySFX(AudioClip clip, float volumeScale = 1.0f)
    {
        if (clip == null || sfxSource == null) return;
        sfxSource.PlayOneShot(clip, sfxVolume * volumeScale);
    }

    public void SetMusicVolume(float vol)
    {
        musicVolume = Mathf.Clamp01(vol);
        if (bgmSource != null) bgmSource.volume = musicVolume;
    }

    public void SetSFXVolume(float vol)
    {
        sfxVolume = Mathf.Clamp01(vol);
        if (sfxSource != null) sfxSource.volume = sfxVolume;
    }
}
