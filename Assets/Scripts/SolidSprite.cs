using UnityEngine;

// A 1x1 white sprite, made in memory.
//
// Several hazards are spawned at runtime rather than placed as prefabs, and a
// SpriteRenderer with no sprite draws nothing at all - which during a playtest
// reads as "the motorbikes are invisible" rather than "someone forgot to assign
// a sprite". This gives every runtime-built object a guaranteed visible
// placeholder that Bun's real art replaces field-by-field later.
public static class SolidSprite
{
    private static Sprite cached;

    public static Sprite Get()
    {
        if (cached != null) return cached;

        Texture2D tex = new Texture2D(1, 1, TextureFormat.RGBA32, false)
        {
            name = "SolidWhite",
            filterMode = FilterMode.Point,   // 8-bit art is Point everywhere else too
            wrapMode = TextureWrapMode.Clamp,
            hideFlags = HideFlags.HideAndDontSave,
        };
        tex.SetPixel(0, 0, Color.white);
        tex.Apply();

        // pixelsPerUnit 1 means transform scale and SpriteRenderer.size are both
        // measured in world units, which is what every caller assumes.
        //
        // FullRect is not optional. Sprite.Create defaults to a Tight mesh, and
        // both callers (TrafficLane, RisingWater) use SpriteDrawMode.Sliced,
        // which needs a full quad to stret