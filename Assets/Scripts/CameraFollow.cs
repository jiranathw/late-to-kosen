using UnityEngine;

// Attach to Main Camera.
public class CameraFollow : MonoBehaviour
{
    [SerializeField] private Transform target; // drag the Player here
    [SerializeField] private float smoothTime = 0.15f;
    [SerializeField] private Vector3 offset = new Vector3(0f, 1f, -10f);

    private Vector3 velocity = Vector3.zero;

    private void LateUpdate()
    {
        if (target == null) return;
        Vector3 desiredPosition = target.position + offset;
        transform.position = Vector3.SmoothDamp(transform.position, desiredPosition, ref velocity, smoothTime);
    }
}
