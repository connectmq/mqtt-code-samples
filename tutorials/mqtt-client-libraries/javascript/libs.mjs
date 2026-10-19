import mqtt from "mqtt";

const clientId = "libs-js-" + Math.random().toString(16).slice(2, 10);
const topic = "connectmq/demo/k3x8p1/libs/javascript";

// Node.js: mqtts://broker.connectmq.com:8883
// Browser: wss://broker.connectmq.com:8084/mqtt
const client = mqtt.connect("mqtts://broker.connectmq.com:8883", {
  clientId,
  protocolVersion: 5,
});

client.on("connect", async () => {
  await client.subscribeAsync(topic, { qos: 1 });
  await client.publishAsync(topic, "hello from MQTT.js", { qos: 1 });
});

client.on("message", (t, payload) => console.log(t, payload.toString()));
client.on("error", (err) => console.error(err.message));
