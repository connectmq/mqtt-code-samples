import mqtt from "mqtt";

const client = mqtt.connect(`mqtts://${process.env.MQTT_HOST}:8883`, {
  clientId: process.env.MQTT_CLIENT_ID,   // YOUR_CLIENT_ID from the portal
  username: process.env.MQTT_USERNAME,    // YOUR_USERNAME
  password: process.env.MQTT_PASSWORD,    // YOUR_PASSWORD
  protocolVersion: 5,
  clean: false,
  properties: { sessionExpiryInterval: 3600 },
});

client.on("connect", () => console.log("Connected to private broker"));
client.on("error", (err) => console.error(err.message));
