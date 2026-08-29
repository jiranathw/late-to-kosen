using UnityEngine;

public class WallTrigger : MonoBehaviour
{
    public GameObject trapWall;
    public GameObject goku;
    public GameObject kamekame;
    public DeathBeam deathBeam;

    private bool triggered = false;

    private void Start()
    {
        if (trapWall != null)
            trapWall.SetActive(false);

        if (goku != null)
            goku.SetActive(false);

        if (kamekame != null)
            kamekame.SetActive(false);

        if (deathBeam != null)
            deathBeam.gameObject.SetActive(false);
    }

    private void OnTriggerEnter2D(Collider2D other)
    {
        if (!other.CompareTag("Player")) return;
        if (triggered) return;

        triggered = true;

        if (trapWall != null)
            trapWall.SetActive(true);

        if (goku != null)
            goku.SetActive(true);

        if (kamekame != null)
            kamekame.SetActive(true);

        if (deathBeam != null)
        {
            deathBeam.gameObject.SetActive(true);
            deathBeam.Activate();
        }
    }

    public void ResetTrigger()
    {
        triggered = false;
    }
}