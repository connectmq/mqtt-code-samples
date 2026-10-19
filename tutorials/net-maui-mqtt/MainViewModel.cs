using System.Text.Json;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using MQTTnet;
using MQTTnet.Formatter;
using MQTTnet.Protocol;

namespace DeviceControl;

public partial class MainViewModel : ObservableObject
{
    private const string Prefix = "connectmq/demo/m4ui7x/device1";
    private readonly IMqttClient _client = new MqttClientFactory().CreateMqttClient();
    private readonly MqttClientOptions _options;
    private bool _suppressToggle;

    [ObservableProperty] private string connectionText = "Disconnected";
    [ObservableProperty] private string temperatureText = "--";
    [ObservableProperty] private string deviceStatus = "unknown";
    [ObservableProperty] private bool relayOn;

    public MainViewModel()
    {
        _options = new MqttClientOptionsBuilder()
            .WithTcpServer("broker.connectmq.com", 8883)
            .WithTlsOptions(o => o.UseTls())
            .WithClientId(GetOrCreateClientId())
            .WithProtocolVersion(MqttProtocolVersion.V500)
            .WithKeepAlivePeriod(TimeSpan.FromSeconds(30))
            .Build();

        _client.ApplicationMessageReceivedAsync += e =>
        {
            var topic = e.ApplicationMessage.Topic;
            var payload = e.ApplicationMessage.ConvertPayloadToString();
            MainThread.BeginInvokeOnMainThread(() => Apply(topic, payload));
            return Task.CompletedTask;
        };

        _client.DisconnectedAsync += _ =>
        {
            MainThread.BeginInvokeOnMainThread(() => ConnectionText = "Disconnected");
            return Task.CompletedTask;
        };
    }

    private static string GetOrCreateClientId()
    {
        var id = Preferences.Get("mqtt_client_id", null as string);
        if (id is null)
        {
            id = $"maui-{Guid.NewGuid():N}"[..20];
            Preferences.Set("mqtt_client_id", id);
        }
        return id;
    }

    private void Apply(string topic, string payload)
    {
        if (topic.EndsWith("/temperature"))
        {
            try
            {
                using var doc = JsonDocument.Parse(payload);
                TemperatureText = $"{doc.RootElement.GetProperty("value").GetDouble():0.0} °C";
            }
            catch (Exception) { TemperatureText = "invalid"; }
        }
        else if (topic.EndsWith("/status"))
        {
            DeviceStatus = payload;
        }
        else if (topic.EndsWith("/relay/state"))
        {
            _suppressToggle = true;
            RelayOn = payload == "on";
            _suppressToggle = false;
        }
    }

    [RelayCommand]
    public async Task ConnectAsync()
    {
        if (_client.IsConnected) return;
        try
        {
            ConnectionText = "Connecting...";
            await _client.ConnectAsync(_options);
            await _client.SubscribeAsync(new MqttClientSubscribeOptionsBuilder()
                .WithTopicFilter(f => f.WithTopic($"{Prefix}/temperature"))
                .WithTopicFilter(f => f.WithTopic($"{Prefix}/status"))
                .WithTopicFilter(f => f.WithTopic($"{Prefix}/relay/state")
                    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce))
                .Build());
            ConnectionText = "Connected";
        }
        catch (Exception ex)
        {
            ConnectionText = $"Error: {ex.Message}";
        }
    }

    public async Task DisconnectAsync()
    {
        if (_client.IsConnected) await _client.DisconnectAsync();
    }

    partial void OnRelayOnChanged(bool value)
    {
        if (_suppressToggle || !_client.IsConnected) return;
        _ = _client.PublishAsync(new MqttApplicationMessageBuilder()
            .WithTopic($"{Prefix}/relay/set")
            .WithPayload(value ? "on" : "off")
            .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
            .Build());
    }
}
