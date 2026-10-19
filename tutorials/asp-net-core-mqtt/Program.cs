using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

builder.Services.Configure<MqttOptions>(builder.Configuration.GetSection("Mqtt"));
builder.Services.AddDbContext<DeviceDb>(o =>
    o.UseSqlite(builder.Configuration.GetConnectionString("Default")));
builder.Services.AddSignalR();
builder.Services.AddHostedService<MqttIngestService>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
    scope.ServiceProvider.GetRequiredService<DeviceDb>().Database.EnsureCreated();

app.UseDefaultFiles();
app.UseStaticFiles();
app.MapHub<TelemetryHub>("/hubs/telemetry");

app.MapGet("/api/readings/{deviceId}", async (string deviceId, DeviceDb db) =>
    await db.Readings.Where(r => r.DeviceId == deviceId)
        .OrderByDescending(r => r.Id).Take(50).ToListAsync());

app.Run();
