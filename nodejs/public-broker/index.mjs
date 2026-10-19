import mqtt from "mqtt";

const topic = "your-project/sensors/temperature"; // Use a unique topic prefix: everyone can read the public broker

// Connect to the free public broker (no account needed)
const client = mqtt.connect("mqtt://broker.connectmq.com:1883");

// Runs when the connection is established
client.on("connect", () => {
  // Subscribe to the temperature topic
  client.subscribe(topic, { qos: 1 });
  // Publish a JSON reading
  client.publish(topic, JSON.stringify({ temperature: 21.5 }), { qos: 1 });
});

// Runs for every message on a subscribed topic
client.on("message", (t, payload) => console.log(t, payload.toString()));
