import mqtt from "mqtt";
import { randomBytes } from "node:crypto";

const clientId = `demo-${randomBytes(3).toString("hex")}`;
const prefix = `connectmq/demo/${clientId}`;

// Option A: MQTT over TLS
const url = "mqtts://broker.connectmq.com:8883";
// Option B: MQTT over Secure WebSocket
// const url = "wss://broker.connectmq.com:8084/mqtt";

const client = mqtt.connect(url, { clientId, protocolVersion: 5 });

client.on("connect", () => {
  console.log("Connected as", clientId);
  client.subscribe(`${prefix}/#`, { qos: 1 });
  client.publish(`${prefix}/humidity`, JSON.stringify({ value: 48 }), { qos: 1 });
});

client.on("message", (topic, payload) => {
  console.log(topic, payload.toString());
});

client.on("error", (err) => console.error(err.message));
