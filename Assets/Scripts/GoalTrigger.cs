using UnityEngine;

// Attach to the "school gate" object at the end of the level.
public class GoalTrigger : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    private void Awake()
    {
        SpriteRenderer sr = GetComponent<SpriteRenderer>();
        if (sr != null)
        {
            sr.color = Color.white;
            if (sr.sprite == null || sr.sprite.name.StartsWith("Square") || sr.sprite.name.StartsWith("Knob"))
            {
                sr.sprite = Resources.Load<Sprite>("Sprites/spr_elevator");
            }
        }
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;
        GameManager.Instance?.WinGame();
    }
}
