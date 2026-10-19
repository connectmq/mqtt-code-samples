using System.Globalization;
using UnityEngine;

public class SpinFromTopic : MonoBehaviour
{
    [SerializeField] private string topic = "fan1/rpm";
    [SerializeField] private Vector3 axis = Vector3.up;
    private float _targetRpm, _currentRpm;

    private void Update()
    {
        if (MqttManager.Instance != null &&
            MqttManager.Instance.TryGet(topic, out var raw) &&
            float.TryParse(raw, NumberStyles.Float, CultureInfo.InvariantCulture, out var rpm))
        {
            _targetRpm = rpm;
        }
        // Smooth toward the target so jumps between messages look natural
        _currentRpm = Mathf.Lerp(_currentRpm, _targetRpm, Time.deltaTime * 2f);
        transform.Rotate(axis, _currentRpm * 6f * Time.deltaTime); // rpm * 360 / 60
    }
}
