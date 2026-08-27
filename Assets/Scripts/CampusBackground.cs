using UnityEngine;

// Self-bootstraps or updates the KOSEN KMITL campus 8-bit background onto the Main Camera.
public class CampusBackground : MonoBehaviour
{
    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        Camera cam = Camera.main;
        if (cam == null) return;

        // Set camera clear color to soft morning sky blue
        cam.backgroundColor = new Color(0.60f, 0.78f, 0.95f, 1f);

        Transform bg = cam.transform.Find("KosenBackground");
        GameObject bgObj;
        if (bg != null)
        {
            bgObj = bg.gameObject;
        }
        else
        {
            bgObj = new GameObject("KosenBackground");
            bgObj.transform.SetParent(cam.transform);
            bgObj.transform.localPosition = new Vector3(0f, 0f, 10f);
            bgObj.transform.localRotation = Quaternion.identity;
        }

        // Scale up to cover widescreen and free aspect
        bgObj.transform.localScale = new Vector3(1.25f, 1.25f, 1f);

        SpriteRenderer sr = bgObj.GetComponent<SpriteRenderer>();
        if (sr == null) sr = bgObj.AddComponent<SpriteRenderer>();

        sr.sortingOrder = -100;
        // Soft opacity (40%) so background stays subtle and doesn't clash with character
        sr.color = new Color(1f, 1f, 1f, 0.40f);

        if (sr.sprite == null)
        {
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
}
