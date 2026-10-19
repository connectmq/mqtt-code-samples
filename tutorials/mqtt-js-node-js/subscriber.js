import mqtt from "mqtt";

const PREFIX = "connectmq/demo/node-a71c";
const clientId = `node-sub-${Math.random().toString(16).slice(2, 10)}`;

const client = mqtt.connect("mqtts://broker.connectmq.com:8883", {
  clientId,
  protocolVersion: 5,
  clean: true,
  keepalive: 30,
  reconnectPeriod: 2000,   // wait 2 s between reconnect attempts
  connectTimeout: 10000,   // give up a single attempt after 10 s
});

client.on("connect", async (connack) => {
  console.log(`Connected as ${clientId}, session present: ${connack.sessionPresent}`);
  const granted = await client.subscribeAsync(`${PREFIX}/+/telemetry`, { qos: 1 });
  console.log("Subscribed:", granted.map((g) => `${g.topic} (qos ${g.qos})`).join(", "));
});

client.on("message", (topic, payload, packet) => {
  let data;
  try {
    data = JSON.parse(payload.toString());
  } catch {
    data = payload.toString();
  }
  const device = topic.split("/").at(-2);
  console.log(`[${device}] qos=${packet.qos} retain=${packet.retain}`, data);
});

client.on("reconnect", () => console.log("Reconnecting..."));
client.on("offline", () => console.log("Offline"));
client.on("error", (err) => console.error("MQTT error:", err.message));

process.on("SIGINT", async () => {
  await client.endAsync();
  process.exit(0);
});
