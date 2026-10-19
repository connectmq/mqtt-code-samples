import mqtt from "mqtt";

const PREFIX = "connectmq/demo/node-a71c";
const DEVICE = "sensor-01";
const clientId = `node-pub-${Math.random().toString(16).slice(2, 10)}`;

const client = await mqtt.connectAsync("mqtts://broker.connectmq.com:8883", {
  clientId,
  protocolVersion: 5,
  will: {
    topic: `${PREFIX}/${DEVICE}/status`,
    payload: Buffer.from("offline"),
    qos: 1,
    retain: true,
  },
});

console.log("Connected");
await client.publishAsync(`${PREFIX}/${DEVICE}/status`, "online", { qos: 1, retain: true });

let count = 0;
const timer = setInterval(async () => {
  const reading = {
    temperature: +(20 + Math.random() * 5).toFixed(2),
    humidity: +(40 + Math.random() * 10).toFixed(1),
    ts: Date.now(),
  };
  try {
    await client.publishAsync(`${PREFIX}/${DEVICE}/telemetry`, JSON.stringify(reading), {
      qos: 1,
      properties: { messageExpiryInterval: 60, contentType: "application/json" },
    });
    console.log("Published", reading);
  } catch (err) {
    console.error("Publish failed:", err.message);
  }
  if (++count === 20) {
    clearInterval(timer);
    await client.publishAsync(`${PREFIX}/${DEVICE}/status`, "offline", { qos: 1, retain: true });
    await client.endAsync();
  }
}, 2000);
