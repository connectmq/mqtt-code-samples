import mqtt from "mqtt";

const globalForMqtt = globalThis;

export function getMqttClient() {
  if (!globalForMqtt.__mqttClient) {
    globalForMqtt.__mqttClient = mqtt.connect(process.env.MQTT_URL ?? "mqtts://broker.connectmq.com:8883", {
      clientId: process.env.MQTT_CLIENT_ID ?? "next-server-" + Math.random().toString(16).slice(2, 10),
      username: process.env.MQTT_USERNAME,
      password: process.env.MQTT_PASSWORD,
      protocolVersion: 5,
      clean: true,
      reconnectPeriod: 5000,
    });
  }
  return globalForMqtt.__mqttClient;
}
