using System.Text.Json;
using System.Threading.Channels;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Options;
using MQTTnet;
using MQTTnet.Formatter;
using MQTTnet.Protocol;

public class MqttIngestService(
    IOptions<MqttOptions> options,
    IServiceScopeFactory scopeFactory,
    IHubContext<TelemetryHub> hub,
    ILogger<MqttIngestService> logger) : BackgroundService
{
    private readonly MqttOptions _opt = options.Value;
    private readonly Channel<Reading> _queue =
        Channel.CreateBounded<Reading>(new BoundedChannelOptions(10_000)
        { FullMode = BoundedChannelFullMode.DropOldest });

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var client = new MqttClientFactory().CreateMqttClient();
        client.ApplicationMessageReceivedAsync += OnMessageAsync;

        var builder = new MqttClientOptionsBuilder()
            .WithTcpServer(_opt.Host, _opt.Port)
            .WithClientId(_opt.ClientId)
            .WithProtocolVersion(MqttProtocolVersion.V500)
            .WithCleanStart(false)
            .WithSessionExpiryInterval(1800);
        if (_opt.UseTls) builder.WithTlsOptions(o => o.UseTls());
        if (!string.IsNullOrEmpty(_opt.Username))
            builder.WithCredentials(_opt.Username, _opt.Password);
        var mqttOptions = builder.Build();

        var writer = Task.Run(() => WriteLoopAsync(stoppingToken), stoppingToken);
        var delay = TimeSpan.FromSeconds(1);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                if (!await client.TryPingAsync(stoppingToken))
                {
                    var result = await client.ConnectAsync(mqttOptions, stoppingToken);
                    logger.LogInformation("MQTT connected, session present: {Present}",
                        result.IsSessionPresent);
                    if (!result.IsSessionPresent)
                    {
                        await client.SubscribeAsync(new MqttClientSubscribeOptionsBuilder()
                            .WithTopicFilter(f => f.WithTopic(_opt.TopicFilter)
                                .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce))
                            .Build(), stoppingToken);
                    }
                    delay = TimeSpan.FromSeconds(1);
                }
            }
            catch (OperationCanceledException) { break; }
            catch (Exception ex)
            {
                logger.LogWarning("MQTT connect failed: {Message}", ex.Message);
                delay = TimeSpan.FromSeconds(Math.Min(delay.TotalSeconds * 2, 60));
            }

            try { await Task.Delay(delay, stoppingToken); }
            catch (OperationCanceledException) { break; }
        }

        if (client.IsConnected) await client.DisconnectAsync();
        client.Dispose();
        _queue.Writer.TryComplete();
        await writer;
    }

    private Task OnMessageAsync(MqttApplicationMessageReceivedEventArgs e)
    {
        try
        {
            // Topic: connectmq/demo/<prefix>/<deviceId>/telemetry
            var parts = e.ApplicationMessage.Topic.Split('/');
            var deviceId = parts[^2];
            using var doc = JsonDocument.Parse(e.ApplicationMessage.ConvertPayloadToString());
            var reading = new Reading
            {
                DeviceId = deviceId,
                Temperature = doc.RootElement.GetProperty("temperature").GetDouble(),
                ReceivedAt = DateTimeOffset.UtcNow
            };
            _queue.Writer.TryWrite(reading);
        }
        catch (Exception ex)
        {
            logger.LogWarning("Dropping bad payload on {Topic}: {Message}",
                e.ApplicationMessage.Topic, ex.Message);
        }
        return Task.CompletedTask;
    }

    private async Task WriteLoopAsync(CancellationToken ct)
    {
        var batch = new List<Reading>(100);
        await foreach (var first in _queue.Reader.ReadAllAsync(CancellationToken.None))
        {
            batch.Add(first);
            while (batch.Count < 100 && _queue.Reader.TryRead(out var next))
                batch.Add(next);

            using (var scope = scopeFactory.CreateScope())
            {
                var db = scope.ServiceProvider.GetRequiredService<DeviceDb>();
                db.Readings.AddRange(batch);
                await db.SaveChangesAsync(CancellationToken.None);
            }

            foreach (var r in batch)
                await hub.Clients.All.SendAsync("reading", r, CancellationToken.None);

            batch.Clear();
        }
    }
}
