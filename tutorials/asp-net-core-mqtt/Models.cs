using Microsoft.EntityFrameworkCore;

public class Reading
{
    public long Id { get; set; }
    public string DeviceId { get; set; } = "";
    public double Temperature { get; set; }
    public DateTimeOffset ReceivedAt { get; set; }
}

public class DeviceDb(DbContextOptions<DeviceDb> options) : DbContext(options)
{
    public DbSet<Reading> Readings => Set<Reading>();
}

public class MqttOptions
{
    public string Host { get; set; } = "";
    public int Port { get; set; } = 8883;
    public bool UseTls { get; set; } = true;
    public string ClientId { get; set; } = "";
    public string? Username { get; set; }
    public string? Password { get; set; }
    public string TopicFilter { get; set; } = "";
}
