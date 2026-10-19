import mqtt from "mqtt";

const id = Math.random().toString(16).slice(2, 10);
const clientId = `node-${id}`;
const topic = `connectmq/demo/${id}/hello`;

const client = mqtt.connect("wss://broker.connectmq.com:8084/mqtt", {
  clientId,
  protocolVersion: 5,
  keepalive: 30,
});

client.on("connect", (connack) => {
  console.log("Connected, CONNACK properties:", connack.properties);
  client.subscribe(topic, { qos: 1 }, (err, granted) => {
    if (err) throw err;
    console.log("Granted:", granted);
    client.publish(topic, JSON.stringify({ temp: 21.5, ts: Date.now() }), { qos: 1 });
  });
});

client.on("message", (t, payload) => {
  console.log(`Received on ${t}: ${payload.toString()}`);
  client.end();
});

client.on("error", (err) => {
  console.error("Connection error:", err.message);
  client.end();
});
