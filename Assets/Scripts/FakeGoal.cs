using UnityEngine;

// The thing that looks like the end of the stage and is not.
//
// Stage 2 uses it as the bus stop you sprint to before remembering the bus does
// not come this way, stage 1 as the lift with the OUT OF ORDER sign. It is the
// purest troll in the game because it costs nothing: it does not kill you, it
// just wastes the one resource the whole game is about, which is seconds.
//
// It deliberately does NOT kill. A fake goal that kills is a hidden trap wearing
// a costume; a fake goal that only wastes your time is a joke you tell once and
// the player still gets to finish the stage.
[RequireComponent(typeof(Collider2D))]
public class FakeGoal : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    [Tooltip("What the sign says once you have walked into it.")]
    [SerializeField] private string revealText = "OUT OF ORDER";

    [Tooltip("Seconds burned off the clock as the punchline. Keep it small - " +
             "the joke is the realisation, not the penalty.")]
    [SerializeField] private float timePenalty = 0f;

    [SerializeField] private Color revealedColor = new Color(0.55f, 0.55f, 0.6f, 1f);

    private SpriteRenderer sprite;
    private Signpost sign;
    private bool revealed;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();
        sign = GetComponentInChildren<Signpost>(true);
        if (sprite != null)
        {
            sprite.color = Color.white;
            if (sprite.sprite == null || sprite.sprite.name.StartsWith("Square") || sprite.sprite.name.StartsWith("Knob"))
            {
                sprite.sprite = Resources.Load<Sprite>("Sprites/spr_elevator");
            }
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (revealed) return;
        if (!other.CompareTag(playerTag)) return;

        revealed = true;

        if (sprite != null)
        {
            if (sprite.sprite == null || sprite.sprite.name == "Square")
                sprite.color = revealedColor;
            else
                sprite.color = Color.white;
        }
        if (sign != null) sign.Say(revealText, true);
        if (timePenalty > 0f) GameManager.Instance?.SpendTime(timePenalty);
    }
}
