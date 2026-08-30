using UnityEngine;
using UnityEngine.SceneManagement;

// Self-bootstraps the KOSEN KMITL campus 8-bit background onto the Main Camera.
//
// RuntimeInitializeOnLoadMethod fires ONCE, at game start, not once per scene.
// Every stage has its own camera, so a one-shot bootstrap would leave stages 2
// and 3 on Unity's default grey-blue clear colour with no background sprite -
// which reads as "the art is broken" rather than "the art is missing". Hooking
// sceneLoaded costs one static event subscription and fixes it for every scene
// that will ever be added.
//
// SIZING. background_kosen.png is 800x450 imported at 32 pixels per unit, so it
// is 25 x 14.06 WORLD UNITS before any scaling - already bigger than the 17.8 x
// 10 the camera can see at orthographicSize 5. The old code then scaled it a
// further 1.25x and pushed it 3.5u up, which meant the player was looking at a
// 1.75x zoom into the middle of one building: the KOSEN-KMITL banner filled a
// third of the screen and read as squashed, because it was.
//
// So the scale is no longer a magic number. It is derived from the camera every
// time the view changes, using a COVER fit - scale by whichever axis needs more,
// so the image always fills the screen with no letterbox and no distortion. At
// 16:9 the sprite and the view have the same aspect and the fit is exact.
public class CampusBackground : MonoBehaviour
{
    // 8-bit art at full strength fights the player sprite and the traps for
    // attention. Knocking it back leaves it as scenery, which is the job.
    private const float Opacity = 0.45f;

    private Camera cam;
    private SpriteRenderer sr;
    private int lastWidth;
    private int lastHeight;
    private float lastOrthoSize;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        SceneManager.sceneLoaded -= OnSceneLoaded;   // never subscribe twice
        SceneManager.sceneLoaded += OnSceneLoaded;
        Apply();
    }

    private static void OnSceneLoaded(Scene scene, LoadSceneMode mode)
    {
        Apply();
    }

    private static void Apply()
    {
        Camera cam = Camera.main;
        if (cam == null) return;

        cam.backgroundColor = new Color(0.60f, 0.78f, 0.95f, 1f);   // morning sky

        Transform found = cam.transform.Find("KosenBackground");
        GameObject bgObj;
        if (found != null)
        {
            bgObj = found.gameObject;
        }
        else
        {
            bgObj = new GameObject("KosenBackground");
            // worldPositionStays: false. The camera moves with the player, and
            // keeping the world position on reparent would drop the background
            // wherever the camera happened to be on frame one.
            bgObj.transform.SetParent(cam.transform, false);
        }

        // Centred, not offset. The image is composed with the horizon low and
        // the sky at the top; shifting it up cropped the sky away and put the
        // building's blank white facade across the middle of the play area.
        bgObj.transform.localPosition = new Vector3(0f, 0f, 10f);
        bgObj.transform.localRotation = Quaternion.identity;

        SpriteRenderer sr = bgObj.GetComponent<SpriteRenderer>();
        if (sr == null) sr = bgObj.AddComponent<SpriteRenderer>();

        sr.sortingOrder = -100;
        sr.color = new Color(1f, 1f, 1f, Opacity);
        sr.sprite = FindSprite();

        CampusBackground fitter = bgObj.GetComponent<CampusBackground>();
        if (fitter == null) fitter = bgObj.AddComponent<CampusBackground>();
        fitter.Bind(cam, sr);
    }

    private static Sprite FindSprite()
    {
        string sceneName = SceneManager.GetActiveScene().name;
        string spriteName = (sceneName == "Level1" || sceneName == "MainMenu") ? "background_stage1" : "background_kosen";

        // Try stage-specific sprite first
        Sprite loaded = Resources.Load<Sprite>("Sprites/" + spriteName);
        if (loaded != null) return loaded;

        Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
        foreach (Sprite s in all)
        {
            if (s != null && s.name == spriteName) return s;
        }

        // Fallback to background_kosen if stage1 is missing
        Sprite fallback = Resources.Load<Sprite>("Sprites/background_kosen");
        if (fallback != null) return fallback;

        foreach (Sprite s in all)
        {
            if (s != null && s.name == "background_kosen") return s;
        }
        return null;
    }

    private void Bind(Camera camera, SpriteRenderer renderer)
    {
        cam = camera;
        sr = renderer;
        Fit();
    }

    // Cheap enough to poll: three comparisons a frame, and it catches the two
    // things that actually change the required scale - the player resizing the
    // window, and the Game view aspect dropdown during a playtest.
    private void LateUpdate()
    {
        if (cam == null) return;

        if (Screen.width == lastWidth &&
            Screen.height == lastHeight &&
            Mathf.Approximately(cam.orthographicSize, lastOrthoSize)) return;

        Fit();
    }

    private void Fit()
    {
        if (cam == null || sr == null || sr.sprite == null) return;

        Vector2 sprite = sr.sprite.bounds.size;      // world units, PPU applied
        if (sprite.x <= 0f || sprite.y <= 0f) return;

        float viewHeight = cam.orthographic ? cam.orthographicSize * 2f : 10f;
        float viewWidth = viewHeight * cam.aspect;

        // Max, not min: contain would letterbox and expose the clear colour at
        // the edges. Cover overfills and crops, which for scenery is free.
        float k = Mathf.Max(viewWidth / sprite.x, viewHeight / sprite.y);
        transform.localScale = new Vector3(k, k, 1f);

        lastWidth = Screen.width;
        lastHeight = Screen.height;
        lastOrthoSize = cam.orthographicSize;
    }
}
