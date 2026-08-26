using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Esc = Pause / Resume, as specified in the design form.
//
// Same self-bootstrapping trick as ResultUI: it builds its own Canvas at
// runtime and needs nothing wired up in the scene, so nobody can break it by
// unassigning a field in the Inspector.
public class PauseMenu : MonoBehaviour
{
    private static PauseMenu instance;

    private CanvasGroup group;

    [RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]
    private static void Bootstrap()
    {
        if (instance != null) return;

        GameObject host = new GameObject("~PauseMenu");
        DontDestroyOnLoad(host);
        instance = host.AddComponent<PauseMenu>();
    }

    private void Awake()
    {
        instance = this;
        Build();
        Hide();
    }

    private void Build()
    {
        GameObject canvasGo = new GameObject("PauseCanvas");
        canvasGo.transform.SetParent(transform, false);

        Canvas canvas = canvasGo.AddComponent<Canvas>();
        canvas.renderMode = RenderMode.ScreenSpaceOverlay;
        canvas.sortingOrder = 90; // under the result screen, over the HUD

        CanvasScaler scaler = canvasGo.AddComponent<CanvasScaler>();
        scaler.uiScaleMode = CanvasScaler.ScaleMode.ScaleWithScreenSize;
        scaler.referenceResolution = new Vector2(1920f, 1080f);
        scaler.matchWidthOrHeight = 0.5f;

        group = canvasGo.AddComponent<CanvasGroup>();
        group.interactable = false;
        group.blocksRaycasts = false;

        GameObject dim = new GameObject("Dim");
        dim.transform.SetParent(canvasGo.transform, false);
        Image panel = dim.AddComponent<Image>();
        panel.color = new Color(0f, 0f, 0f, 0.66f);
        RectTransform prt = panel.rectTransform;
        prt.anchorMin = Vector2.zero;
        prt.anchorMax = Vector2.one;
        prt.offsetMin = Vector2.zero;
        prt.offsetMax = Vector2.zero;

        MakeText(canvasGo.transform, "PAUSED", 120f, new Vector2(0f, 80f), Color.white);
        MakeText(canvasGo.transform,
                 "Esc  resume        R  restart        Q  quit",
                 46f, new Vector2(0f, -70f), new Color(0.85f, 0.85f, 0.85f));
    }

    private static void MakeText(Transform parent, string content, float size, Vector2 pos, Color color)
    {
        GameObject go = new GameObject("Text");
        go.transform.SetParent(parent, false);

        TextMeshProUGUI text = go.AddComponent<TextMeshProUGUI>();
        text.text = content;
        text.fontSize = size;
        text.alignment = TextAlignmentOptions.Center;
        text.color = color;

        RectTransform rt = text.rectTransform;
        rt.anchorMin = new Vector2(0.5f, 0.5f);
        rt.anchorMax = new Vector2(0.5f, 0.5f);
        rt.pivot = new Vector2(0.5f, 0.5f);
        rt.anchoredPosition = pos;
        rt.sizeDelta = new Vector2(1700f, 220f);
    }

    // Update still ticks while Time.timeScale is 0, which is what makes it
    // possible to unpause at all.
    private void Update()
    {
        GameManager gm = GameManager.Instance;
        if (gm == null)
        {
            Hide();
            return;
        }

        if (gm.IsGameOver)
        {
            Hide();
            return;
        }

        if (Input.GetKeyDown(KeyCode.Escape)) gm.TogglePause();

        if (!gm.IsPaused)
        {
            Hide();
            return;
        }

        group.alpha = 1f;

        if (Input.GetKeyDown(KeyCode.R)) gm.RestartLevel();
        if (Input.GetKeyDown(KeyCode.Q)) gm.QuitGame();
    }

    private void Hide()
    {
        if (group != null) group.alpha = 0f;
    }
}
