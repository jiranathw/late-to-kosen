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
        // localPosition is measured in the parent's squashed units too 