using UnityEngine;

// Props only: traps, lift, pots, bike, ajarn, rack.
// Floors and walls live on LevelSurfaceArt so trap sprite work cannot
// restamp or restretch the platforms.
[ExecuteAlways]
[DefaultExecutionOrder(-80)]
public class LevelPropArt : MonoBehaviour
{
    private static Sprite trap, spike, hidden;
    private static Sprite elevator, flowerpot, bicycle, ajarnBike, bikeRack, lizard;
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
        try { ApplyInner(); }
        finally { applying = false; }
    }

    private void ApplyInner()
    {
        SpriteRenderer sr = GetComponent<SpriteRenderer>();
        if (sr == null) return;

        EnsureLoaded();
        string n = gameObject.name;

        if (n.StartsWith("Void_") || n.StartsWith("KillBlock"))
            return;

        if (n.Contains("Lift") || n == "FakeGoal")
        {
            Stamp(sr, elevator, 2);
            return;
        }

        if (n.StartsWith("Pot_") || n == "Flowerpot")
        {
            Stamp(sr, flowerpot, 5);
            return;
        }

        if (n.StartsWith("Bicycle") || n == "Bicycle")
        {
            Stamp(sr, bicycle, 4);
            return;
        }

        if (n.StartsWith("Lizard_") || n == "MonitorLizard")
        {
            Stamp(sr, lizard, 5);
            return;
        }

        if (n.StartsWith("Ajarn_") || n.Contains("Ajarn"))
        {
            Stamp(sr, ajarnBike, 6);
            return;
        }

        if (n.StartsWith("Rack_") || n == "BikeRack")
        {
            Stamp(sr, bikeRack, 1);
            return;
        }

        // SORTING -2, NOT 3. A riser lives inside the slab it comes out of, so
        // it has to draw BEHIND the floor tiles (which sit on order 0) or the
        // player sees the fan sitting in the floorboards from across the room
        // and the trap has nothing left to spring. TrapSpike.prefab was authored
        // at -2 for exactly this reason and stamping it at 3 undid that.
        // Above the surface nothing occludes it, so the moment it rises it is
        // visible - which is the few frames of warning the trap is meant to give.
        if (n.StartsWith("Spike_") || n == "TrapSpike")
        {
            Stamp(sr, NamedTrapSprite(n, spike != null ? spike : trap), -2);
            return;
        }

        if (n.StartsWith("Hidden_") || n == "TrapHidden")
        {
            Stamp(sr, NamedTrapSprite(n, hidden != null ? hidden : trap), 2);
            return;
        }

        if (n.StartsWith("Trap_") || n == "Trap")
        {
            Stamp(sr, NamedTrapSprite(n, trap), 3);
        }
    }

    private static void EnsureLoaded()
    {
        if (loaded && trap != null) return;
        trap = Load("spr_trap");
        spike = Load("spr_trap_spike");
        hidden = Load("spr_trap_hidden");
        elevator = Load("spr_elevator");
        flowerpot = Load("spr_flowerpot");
        bicycle = Load("spr_bicycle");
        ajarnBike = Load("spr_ajarn_bike");
        bikeRack = Load("spr_bike_rack");
        lizard = Load("spr_lizard");
        loaded = true;
    }

    private static Sprite Load(string name)
    {
        return Resources.Load<Sprite>("Sprites/" + name);
    }

    private static Sprite NamedTrapSprite(string objectName, Sprite fallback)
    {
        int i = objectName.LastIndexOf('_');
        if (i < 0 || i >= objectName.Length - 1) return fallback;
        string key = objectName.Substring(i + 1).ToLowerInvariant();
        Sprite named = Load("spr_trap_" + key);
        return named != null ? named : fallback;
    }

    private static void Stamp(SpriteRenderer sr, Sprite sprite, int sorting)
    {
        if (sr == null || sprite == null) return;
        sr.forceRenderingOff = false;
        sr.sprite = sprite;
        sr.color = Color.white;
        sr.drawMode = SpriteDrawMode.Simple;
        sr.sortingOrder = sorting;
    }
}
