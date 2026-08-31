using UnityEngine;

[RequireComponent(typeof(Collider2D))]
public class HiddenTrap : MonoBehaviour
{
    [SerializeField] private string playerTag = "Player";

    [SerializeField]
    private Color revealedColor =
        new Color(1f, 0.25f, 0.3f, 1f);

    private SpriteRenderer sprite;

    private void Awake()
    {
        sprite = GetComponent<SpriteRenderer>();

        // Start invisible
        SetVisible(false);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag(playerTag)) return;

        // Player touched trap → reveal it permanently
        SetVisible(true);

        PlayerController player =
            other.GetComponent<PlayerController>();

        if (player != null)
        {
            player.Die();
        }
        else
        {
            GameManager.Instance?.PlayerDied();
        }
    }

    private void SetVisible(bool visible)
    {
        if (sprite == null) return;

        sprite.enabled = visible;
        sprite.forceRenderingOff = !visible;

        if (visible)
        {
            sprite.color = revealedColor;
        }
    }
}