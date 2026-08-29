using System.Collections.Generic;
using UnityEngine;

public class DeathBeam : MonoBehaviour
{
    private static readonly List<DeathBeam> allBeams = new List<DeathBeam>();

    public float growSpeed = 3f;

    [Header("Wall Trap Objects")]
    public GameObject trapWall;
    public GameObject goku;
    public GameObject kamekame;

    [Header("Wall Trigger")]
    public WallTrigger wallTrigger;

    private SpriteRenderer spriteRenderer;
    private BoxCollider2D beamCollider;

    private Vector3 startPosition;
    private Vector2 startSize;

    private bool activated = false;

    private void Awake()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
        beamCollider = GetComponent<BoxCollider2D>();

        startPosition = transform.position;
        if (spriteRenderer != null)
        {
            startSize = spriteRenderer.size;
        }
    }

    private void OnEnable()
    {
        if (!allBeams.Contains(this)) allBeams.Add(this);
    }

    private void OnDisable()
    {
        allBeams.Remove(this);
    }

    public static void ResetAllBeams()
    {
        DeathBeam[] beams = allBeams.ToArray();
        foreach (var beam in beams)
        {
            if (beam != null) beam.ResetBeam();
        }

        WallTrigger[] wallTriggers = Object.FindObjectsByType<WallTrigger>(FindObjectsInactive.Include, FindObjectsSortMode.None);
        foreach (var wt in wallTriggers)
        {
            if (wt != null) wt.ResetTrigger();
        }
    }

    public void Activate()
    {
        transform.position = startPosition;
        if (spriteRenderer != null) spriteRenderer.size = startSize;
        if (beamCollider != null) beamCollider.size = startSize;

        activated = true;
    }

    private void Update()
    {
        if (!activated || spriteRenderer == null) return;

        float growth = growSpeed * Time.deltaTime;

        Vector2 newSize = spriteRenderer.size;
        newSize.x += growth;
        spriteRenderer.size = newSize;

        transform.position += Vector3.left * (growth * 0.5f);

        if (beamCollider != null)
        {
            beamCollider.size = newSize;
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        if (!collision.gameObject.CompareTag("Player")) return;

        ResetBeam();

        PlayerController player = collision.gameObject.GetComponent<PlayerController>();
        if (player != null)
        {
            player.Die();
        }
        else if (GameManager.Instance != null)
        {
            GameManager.Instance.PlayerDied();
        }
    }

    public void ResetBeam()
    {
        activated = false;

        transform.position = startPosition;
        if (spriteRenderer != null) spriteRenderer.size = startSize;
        if (beamCollider != null) beamCollider.size = startSize;

        gameObject.SetActive(false);

        if (trapWall != null) trapWall.SetActive(false);
        if (goku != null) goku.SetActive(false);
        if (kamekame != null) kamekame.SetActive(false);

        if (wallTrigger != null) wallTrigger.ResetTrigger();
    }
}