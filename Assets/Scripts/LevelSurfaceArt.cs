using UnityEngine;

// Floors, walls, road, kerb only. Kept off the trap prefabs so trap art
// changes cannot restamp these surfaces.
//
// Platforms store their size on Transform scale (Room_Floor is 12 x 1).
// Tiling on that renderer would stretch one 32px tile across the whole slab.
// A DontSave child cancels the scale, then repeats the tile in world units.
[ExecuteAlways]
[DefaultExecutionOrder(-80)]
public class LevelSurfaceArt : MonoBehaviour
{
    private const string ChildName = "_TiledArt";

    private static Sprite dormFloor, dormWall, road, kerb;
    private static bool loaded;
    private bool applying;

    private void OnEnable()
    {
        Apply();
    }

#if UNITY_EDITOR
    private void OnValidate()
    {
        if (!isActiveAndEnabled) return;
        UnityEditor.EditorApplication.delayCall += ApplyIfAlive;
    }

    private void ApplyIfAlive()
    {
        if (this == null) return;
        Apply();
    }
#endif

    private void Apply()
    {
        if (applying) return;
        applying = true;
        try
        {
            ApplyInner();
        }
        finally
        {
            applying = false;
        }
    }

    private void ApplyInner()
    {
#if UNITY_EDITOR
        if (!Application.isPlaying && UnityEditor.PrefabUtility.IsPartOfPrefabAsset(gameObject))
            return;
#endif
        SpriteRenderer sr = GetComponent<SpriteRenderer>();
        if (sr == null) return;

        EnsureLoaded();
        string n = gameObject.name;
        Sprite sprite = SpriteFor(n);
        if (sprite == null) return;

        TileOnChild(sr, sprite);
    }

    private static Sprite SpriteFor(string n)
    {
        if (n.StartsWith("Wall_"))
            return dormWall != null ? dormWall : dormFloor;
        if (n.StartsWith("Ground_Soi") || n.StartsWith("Road_"))
            return road;
        if (n.StartsWith("Kerb_") || n == "Forecourt")
            return kerb != null ? kerb : road;
        return dormFloor;
    }

    private static void EnsureLoaded()
    {
        if (loaded && dormFloor != null) return;
        dormFloor = Resources.Load<Sprite>("Sprites/tile_dorm_floor");
        dormWall = Resources.Load<Sprite>("Sprites/tile_dorm_wall");
        road = Resources.Load<Sprite>("Sprites/tile_road");
        kerb = Resources.Load<Sprite>("Sprites/tile_kerb");
        loaded = dormFloor != null;
    }

    private static void TileOnChild(SpriteRenderer host, Sprite sprite)
    {
        host.sprite = sprite;
        host.color = Color.white;
        host.drawMode = SpriteDrawMode.Simple;
        host.forceRenderingOff = true;

        Transform t = host.transform;
        Vector3 scale = t.localScale;
        float w = Mathf.Max(0.01f, Mathf.Abs(scale.x));
        float h = Mathf.Max(0.01f, Mathf.Abs(scale.y));

        Transform child = t.Find(ChildName);
        if (child == null)
        {
            GameObject go = new GameObject(ChildName);
            go.hideFlags = HideFlags.DontSave | HideFlags.NotEditable;
            child = go.transform;
            child.SetParent(t, false);
        }

        child.localPosition = Vector3.zero;
        child.localRotation = Quaternion.identity;
        child.localScale = new Vector3(
            Mathf.Sign(scale.x) / w,
            Mathf.Sign(scale.y) / h,
            1f);

        SpriteRenderer vis = child.GetComponent<SpriteRenderer>();
        if (vis == null) vis = child.gameObject.AddComponent<SpriteRenderer>();
        vis.sprite = sprite;
        vis.color = Color.white;
        vis.drawMode = SpriteDrawMode.Tiled;
        vis.tileMode = SpriteTileMode.Continuous;
        vis.size = new Vector2(w, h);
        vis.sortingLayerID = host.sortingLayerID;
        vis.sortingOrder = host.sortingOrder;
        vis.forceRenderingOff = false;
    }
}
