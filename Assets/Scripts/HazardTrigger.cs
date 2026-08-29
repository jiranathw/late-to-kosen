using UnityEngine;

// A tripwire. Walk through it and something else in the level wakes up.
//
// Generalised from Krin's WallTrigger / RockTrigger, which were the same script
// twice with a different field name. One script, one prefab, any hazard: drag
// whatever should fire into `hazard` and it fires once.
//
// One-shot on purpose. Retriggering as the player walks back and forth would
// let a flowerpot drop on their head from a balcony they already passed, which
// reads as a bug rather than as a joke.
[RequireComponent(typeof(Collider2D))]
public class HazardTrigger : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    [Tooltip("The thing that wakes up. Must implement ITriggerable - " +
             "ChaserHazard, FallingObject and RisingWater all do.")]
    [SerializeField] private MonoBehaviour hazard;

    [Tooltip("Extra objects to switch on at the same moment: warning signs, " +
             "the dog sprite, a barrier. Left empty is fine.")]
    [SerializeField] private GameObject[] alsoActivate;

    private bool fired;

    private void Awake()
    {
        // Trigger volumes are invisible by design, but the prefab carries a
        // SpriteRenderer so the zone can be seen while placing it in the editor.
        SpriteRenderer sr = GetComponent<SpriteRenderer>();
        if (sr != null) sr.enabled = false;

        for (int i = 0; i < (alsoActivate?.Length ?? 0); i++)
        {
            if (alsoActivate[i] != null) alsoActivate[i].SetActive(false);
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (fired) return;
        if (!other.CompareTag(playerTag)) return;

        fired = true;

        for (int i = 0; i < (alsoActivate?.Length ?? 0); i++)
        {
            if (alsoActivate[i] != null) alsoActivate[i].SetActive(true);
        }

        if (hazard is ITriggerable t) t.Trigger();
        else if (hazard != null) hazard.SendMessage("Trigger", SendMessageOptions.DontRequireReceiver);
    }

    // Hazards call this on themselves after they kill the player, so the gag
    // is armed again for the retry.
    public void Rearm()
    {
        fired = false;
    }
}

// Implemented by everything a HazardTrigger can set off.
public interface ITriggerable
{
    void Trigger();
}
