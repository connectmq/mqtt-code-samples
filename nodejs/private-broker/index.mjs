import mqtt from "mqtt";

const topic = "your-project/sensors/temperature";

// Connect to your private ConnectMQ broker on port 8883
const client = mqtt.connect("mqtts://YOUR_BROKER_HOST:8883", {
  // Username and password from your ConnectMQ dashboard
  username: "YOUR_USERNAME",
  password: "YOUR_PASSWORD",
});

// Runs when the connection is established
client.on("connect", () => {
  // Subscribe to the temperature topic
  client.subscribe(topic, { qos: 1 });
  // Publish a JSON reading
  client.publish(topic, JSON.stringify({ temperature: 21.5 }), { qos: 1 });
});

// Runs for every message on a subscribed topic
client.on("message", (t, payload) => console.log(t, payload.toString()));
