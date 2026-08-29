using UnityEngine;

// The only way off an Anywheel bike - and only if it is a real one.
//
// A rack is a wide, obvious, slightly over-designed piece of furniture that the
// player learns to read as "relief" within about four seconds of taking their
// first bike. Which is exactly why some of them are painted on.
//
// The fake rack is the cruellest thing in stage 1 and it has to be built
// honestly to work: same sprite, same size, same sign font, same everything.
// Nothing about a fake rack is distinguishable until you are standing in it and
// the app tells you no. Krin's level does the same trick with FakeGoal and
// FakeGround, and the reason it lands there is that the fake is a pixel-perfect
// copy of the real thing rather than a slightly-off imitation.
//
// A refusal is never a death. The player loses time and the ride continues,
// which is worse, because the bike is heavier and jumps shorter and they now
// have to take the next gap on it.
[RequireComponent(typeof(Collider2D))]
public class BikeRack : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    [Tooltip("Uncheck for a painted-on rack. Keep the sprite and the size " +
             "identical to a real one or the joke does not work.")]
    [SerializeField] private bool isReal = true;

    [Header("Signs")]
    [Tooltip("Shown when the player is not on a bike. Same text on real and " +
             "fake racks - this is the label the player learns to trust.")]
    [SerializeField, TextArea] private string idleMessage = "ANYWHEEL PARKING";

    [SerializeField, TextArea] private string parkedMessage =
        "RIDE ENDED - thanks for using Anywheel";

    [Tooltip("The reveal. Says nothing about this particular rack being fake, " +
             "because the app would not either.")]
    [SerializeField, TextArea] private string refusedMessage =
        "CANNOT END RIDE HERE - outside docking zone";

    [Header("Refusal Cost")]
    [Tooltip("Seconds off the clock each time a fake rack turns the player " +
             "away. The meter does not stop just because you tried.")]
    [SerializeField] private float refusalTimeCost = 0f;

    [Tooltip("A refused player who stands in the rack should not be billed " +
             "every frame, or every physics re-entry.")]
    [SerializeField] private float refusalCooldown = 1.5f;

    private Signpost sign;
    private float refusalTimer;
    private bool parkedHere;

    private void Awake()
    {
        sign = GetComponent<Signpost>();
        if (sign == null) sign = gameObject.AddComponent<Signpost>();
        sign.Say(idleMessage, false);
    }

    private void Update()
    {
        if (refusalTimer > 0f) refusalTimer -= Time.deltaTime;
    }

    private void OnTriggerEnter2D(Collider2D other) { TryPark(other); }
    private void OnTriggerStay2D(Collider2D other)  { TryPark(other); }

    private void TryPark(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        PlayerController player = other.GetComponent<PlayerController>();
        if (player == null || !player.IsRiding) return;

        if (isReal)
        {
            player.ParkBike();
            parkedHere = true;
            if (sign != null) sign.Say(parkedMessage, true);
            return;
        }

        // Painted on. Refuse, charge for the attempt, and let the sign go back
        // to reading like a normal rack afterwards so a player who comes past
        // again has to decide all over whether to trust it.
        if (refusalTimer > 0f) return;
        refusalTimer = refusalCooldown;

        if (sign != null) sign.Say(refusedMessage, false);

        if (refusalTimeCost > 0f)
        {
            GameManager gm = GameManager.Instance;
            if (gm != null) gm.SpendTime(refusalTimeCost);
        }
    }

    private void OnTriggerExit2D(Collider2D other)
    {
        if (parkedHere) return;
        if (!other.CompareTag(playerTag)) return;
        if (sign != null) sign.Say(idleMessage, false);
    }
}
