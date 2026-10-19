using System;
using System.Collections.Concurrent;
using System.Threading;
using System.Threading.Tasks;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;
using UnityEngine;

public class MqttManager : MonoBehaviour
{
    public static MqttManager Instance { get; private set; }

    [SerializeField] private string host = "broker.connectmq.com";
    [SerializeField] private int port = 8883;
    [SerializeField] private bool useTls = true;
    [SerializeField] private string topicPrefix = "connectmq/demo/u9n1ty";
    [SerializeField] private string username = "";
    [SerializeField] private string password = "";

    private readonly ConcurrentDictionary<string, string> _latest = new();
    private IMqttClient _client;
    private CancellationTokenSource _cts;
    private string _clientId;

    public bool IsConnected => _client != null && _client.IsConnected;

    public bool TryGet(string relativeTopic, out string payload) =>
        _latest.TryGetValue($"{topicPrefix}/{relativeTopic}", out payload);

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    private void Start()
    {
        // Unity APIs such as Application must be read on the main thread
        _clientId = $"unity-{Application.platform}-{Guid.NewGuid().ToString("N").Substring(0, 8)}";
        _cts = new CancellationTokenSource();
        _client = new MqttFactory().CreateMqttClient();
        _client.ApplicationMessageReceivedAsync += e =>
        {
            _latest[e.ApplicationMessage.Topic] = e.ApplicationMessage.ConvertPayloadToString();
            return Task.CompletedTask;
        };
        _ = Task.Run(() => ConnectionLoop(_cts.Token));
    }

    private async Task ConnectionLoop(CancellationToken ct)
    {
        var builder = new MqttClientOptionsBuilder()
            .WithTcpServer(host, port)
            .WithClientId(_clientId)
            .WithProtocolVersion(MQTTnet.Formatter.MqttProtocolVersion.V500)
            .WithKeepAlivePeriod(TimeSpan.FromSeconds(30));
        if (useTls) builder.WithTlsOptions(o => o.UseTls());
        if (!string.IsNullOrEmpty(username)) builder.WithCredentials(username, password);
        var options = builder.Build();

        var delay = 1;
        while (!ct.IsCancellationRequested)
        {
            try
            {
                if (!_client.IsConnected)
                {
                    await _client.ConnectAsync(options, ct);
                    await _client.SubscribeAsync(new MqttClientSubscribeOptionsBuilder()
                        .WithTopicFilter(f => f.WithTopic($"{topicPrefix}/#")
                            .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtMostOnce))
                        .Build(), ct);
                    Debug.Log("MQTT connected");
                    delay = 1;
                }
            }
            catch (OperationCanceledException) { break; }
            catch (Exception ex)
            {
                Debug.LogWarning($"MQTT connect failed: {ex.Message}");
                delay = Math.Min(delay * 2, 30);
            }
            try { await Task.Delay(TimeSpan.FromSeconds(delay), ct); }
            catch (OperationCanceledException) { break; }
        }
    }

    public Task PublishAsync(string relativeTopic, string payload, bool retain = false)
    {
        if (!IsConnected) return Task.CompletedTask;
        var msg = new MqttApplicationMessageBuilder()
            .WithTopic($"{topicPrefix}/{relativeTopic}")
            .WithPayload(payload)
            .WithRetainFlag(retain)
            .Build();
        return _client.PublishAsync(msg);
    }

    private async void OnDestroy()
    {
        if (Instance != this) return;
        _cts?.Cancel();
        if (_client != null && _client.IsConnected)
        {
            try { await _client.DisconnectAsync(); } catch { }
        }
        _client?.Dispose();
    }
}
