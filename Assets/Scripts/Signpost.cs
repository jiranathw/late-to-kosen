using System.Collections.Generic;
using UnityEngine;
using TMPro;

// World-space text that fades in when the player is near it.
//
// Three stages of a joke game only land if the player knows what they are
// looking at: "the lift is broken", "the bus does not come here", "wrong
// building". Without signs, a troll is just an unexplained death, and an
// unexplained death is where players stop laughing and start closing the game.
//
// Builds its own TextMeshPro child at runtime so the prefab stays a single
// object and nothing needs assigning in the Inspector.
//
// ASCII only: the bundled TMP font (LiberationSans SDF) has no Thai glyphs and
// no emoji, and both render as empty boxes.
public class Signpost : MonoBehaviour
{
    [SerializeField, TextArea] private string message = "";
    [SerializeField] private float showRange = 5.5f;
    // World-space TMP: roughly fontSize/10 world units per line, against a
    // camera that shows 10 units of height. This is not the same number as the
    // fontSize on a TextMeshProUGUI inside a canvas - do not copy one to the
    // other, which is how this ended up at 0.8 and invisible for a while.
    [SerializeField] private float fontSize = 4f;
    [SerializeField] private Vector3 offset = new Vector3(0f, 1.6f, 0f);
    [SerializeField] private Color color = new Color(1f, 0.95f, 0.6f, 1f);
    [SerializeField] private string playerTag = "Player";

    [Tooltip("Latched signs stay up once shown. Use for punchlines you want the " +
             "player to still be reading while they walk away.")]
    [SerializeField] private bool latch;

    // Typed as the concrete TextMeshPro, not the TMP_Text base class: sortingOrder
    // is declared on TextMeshPro only, so a TMP_Text-typed field will not compile.
    private TextMeshPro label;
    private Transform player;
    private bool latched;

    // Every signpost currently alive in the scene, so each one can tell whether
    // another is closer to the player. See the yield loop in Update.
    private static readonly List<Signpost> live = new List<Signpost>();

    // Last frame's distance to the player, published so the other signs can see
    // it. One frame of staleness is invisible; recomputing it n^2 times a frame
    // would not be.
    private float distance = float.MaxValue;

    private void OnEnable() { live.Add(this); }
    private void OnDisable() { live.Remove(this); }

    private void Awake()
    {
        GameObject go = new GameObject("Label");
        go.transform.SetParent(transform, false);

        // THE SQUEEZED-TEXT FIX.
        //
        // Every object this script lives on is scaled non-uniformly: the
        // signpost body is 0.25 x 1.4, the bike rack 1.6 x 1.2, the fake goal
        // 2 x 3. A child transform inherits that scale, so the label was being
        // drawn at a quarter width and 140% height - tall, thin, unreadable
        // letters. Nothing was wrong with the font; the post was wearing it.
        //
        // Dividing the label's own scale by the parent's puts it back at 1:1 in
        // world space, so a letter is the same shape on a signpost, a rack and
        // a fake goal. The offset is divided by the same numbers because
        // localPosition is measured in the parent's squashed units too - without
        // that, "1.6 above the post" means 2.24 world units on a signpost and
        // 4.8 on a fake goal.
        Vector3 s = transform.lossyScale;
        float sx = Mathf.Approximately(s.x, 0f) ? 1f : s.x;
        float sy = Mathf.Approximately(s.y, 0f) ? 1f : s.y;
        go.transform.localScale = new Vector3(1f / sx, 1f / sy, 1f);
        go.transform.localPosition =
            new Vector3(offset.x / sx, offset.y / sy, offset.z);

        label = go.AddComponent<TextMeshPro>();
        label.text = message;
        label.fontSize = fontSize;
        label.alignment = TextAlignmentOptions.Center;
        label.color = color;
        label.sortingOrder = 30;

        // A dark outline, because a sign gets read against a pale sky, a white
        // floor and a photograph of a lecturer, sometimes within the same three
        // seconds. Pale yellow survives none of those on its own.
        //
        // Touching outlineColor instances this label's material, which is what
        // we want here - eleven signs is eleven small materials and no shared
        // state that one sign can corrupt for the rest. UpdateMeshPadding is
        // not optional: the glyph quads are sized for no outline, and without
        // the extra padding the outline is clipped off at the letter edges.
        label.outlineWidth = 0.25f;
        label.outlineColor = new Color32(10, 10, 18, 255);
        label.UpdateMeshPadding();

        // 10 world units of wrap width against a camera that shows about 17.8.
        // Wide enough for a sentence on two lines, narrow enough that a sign
        // never runs off the side of the screen you are reading it from.
        RectTransform rt = label.rectTransform;
        rt.sizeDelta = new Vector2(10f, 4f);

        SetAlpha(0f);
    }

    private void Update()
    {
        if (label == null) return;

        GameManager gm = GameManager.Instance;
        if (gm != null && gm.IsGameOver)
        {
            SetAlpha(0f);
            return;
        }

        if (player == null)
        {
            GameObject p = GameObject.FindGameObjectWithTag(playerTag);
            if (p == null) return;
            player = p.transform;
        }

        float d = Vector2.Distance(player.position, transform.position);
        distance = d;

        // ONE SIGN AT A TIME.
        //
        // A sign yields to any other sign that is in range and closer than it
        // is. Walking a corridor then reads as one message handing over to the
        // next, instead of two sentences printed across each other - which is
        // what the first two signs of stage 1 did, five units apart with seven
        // units of range each.
        //
        // Spacing those two by hand would have fixed those two. This fixes
        // every pair in the game, including the ones a teammate places next
        // week without reading this file. It costs eleven distance comparisons
        // a frame against cached values, which is nothing.
        //
        // Latched signs are subject to this too. "Stays up while you walk away"
        // is the point of a latch; "stays up on top of the next sign you walk
        // into" is not.
        for (int i = 0; i < live.Count; i++)
        {
            Signpost other = live[i];
            if (other == this) continue;
            if (other.distance <= other.showRange && other.distance < d)
            {
                SetAlpha(0f);
                return;
            }
        }

        if (latched)
        {
            SetAlpha(1f);
            return;
        }

        if (d > showRange)
        {
            SetAlpha(0f);
            return;
        }

        // Fades over the outer third of the range instead of popping on, so a
        // row of signs does not flicker as the player runs past.
        float a = Mathf.Clamp01((showRange - d) / (showRange * 0.34f));
        SetAlpha(a);

        // Arming the latch. The serialized `latch` flag was never read by
        // anything - only FakeGoal's reveal could set `latched` - so every sign
        // built with latch=True, including "ANYWHEEL DOCK - 50m" in the middle
        // of the chase, was quietly fading out again the moment you rode past
        // it. The flag says a sign CAN latch; arriving at it is what latches it.
        if (latch && a >= 1f) latched = true;
    }

    // Used by FakeGoal to change what the sign says at the moment of the reveal.
    public void Say(string text, bool keepShowing)
    {
        message = text;
        if (label != null) label.text = text;
        if (keepShowing) latched = true;
    }

    private void SetAlpha(float a)
    {
        Color c = label.color;
        if (Mathf.Approximately(c.a, a)) return;
        c.a = a;
        label.color = c;

        // The face colour is a vertex colour and fades on its own. The outline
        // is a material property and does not, so it has to be faded by hand -
        // otherwise every sign in the level sits there as a permanent dark
        // ghost of its own text, which is worse than having no signs at all.
        Color32 o = label.outlineColor;
        o.a = (byte)Mathf.RoundToInt(Mathf.Clamp01(a) * 255f);
        label.outlineColor = o;
    }
}
