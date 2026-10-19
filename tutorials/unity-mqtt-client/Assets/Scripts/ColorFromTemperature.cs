using UnityEngine;

public class ColorFromTemperature : MonoBehaviour
{
    [System.Serializable] private class Reading { public float temperature; }

    [SerializeField] private string topic = "tank1/telemetry";
    [SerializeField] private float min = 20f, max = 90f;
    [SerializeField] private Gradient gradient;
    private Renderer _renderer;
    private string _lastRaw;

    private void Awake() => _renderer = GetComponent<Renderer>();

    private void Update()
    {
        if (MqttManager.Instance == null || !MqttManager.Instance.TryGet(topic, out var raw)) return;
        if (raw == _lastRaw) return; // nothing new
        _lastRaw = raw;
        var reading = JsonUtility.FromJson<Reading>(raw);
        var t = Mathf.InverseLerp(min, max, reading.temperature);
        _renderer.material.color = gradient.Evaluate(t);
    }
}
