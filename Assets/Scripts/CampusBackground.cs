using UnityEngine;

// Self-bootstraps the KOSEN KMITL campus 8-bit background onto the Main Camera.
// Follows the same runtime architecture as HudUI / PauseMenu / ResultUI.
public class CampusBackground : MonoBehaviour
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        Camera cam = Camera.main;
        if (cam == null) return;

        // If background already exists on camera, don't duplicate
        if (cam.transform.Find("KosenBackground") != null) return;

        GameObject bgObj = new GameObject("KosenBackground");
        bgObj.transform.SetParent(cam.transform);
        bgObj.transform.localPosition = new Vector3(0f, 0f, 10f);
        bgObj.transform.localRotation = Quaternion.identity;
        bgObj.transform.localScale = Vector3.one;

        SpriteRenderer sr = bgObj.AddComponent<SpriteRenderer>();
        sr.sortingOrder = -100; // Always render behind grounds, traps, and player
        sr.color = Color.white;

        Sprite[] all = Resources.FindObjectsOfTypeAll<Sprite>();
        foreach (var s in all)
        {
            if (s != null && s.name == "background_kosen")
            {
                sr.sprite = s;
                break;
            }
        }
    }
}
