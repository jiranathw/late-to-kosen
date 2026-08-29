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
            bgObj = found.gameObj