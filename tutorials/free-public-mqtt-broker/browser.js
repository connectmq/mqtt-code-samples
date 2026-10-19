import mqtt from "mqtt";

const clientId = "web-" + Math.random().toString(16).slice(2, 8);
const prefix = `connectmq/demo/${clientId}`;

const client = mqtt.connect("wss://broker.connectmq.com:8084/mqtt", {
  clientId,
  protocolVersion: 5,
});

client.on("connect", () => {
  client.subscribe(`${prefix}/#`);
  client.publish(`${prefix}/hello`, "Hello from the browser");
});

client.on("message", (topic, payload) => {
  const line = document.createElement("div");
  line.textContent = `${topic}: ${payload.toString()}`;
  document.body.appendChild(line);
});
