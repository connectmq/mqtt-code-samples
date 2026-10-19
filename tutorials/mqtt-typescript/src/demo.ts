import { randomUUID } from "node:crypto";
import { contracts } from "./contracts.js";
import { TypedMqttClient } from "./typed-client.js";

const mq = new TypedMqttClient("mqtts://broker.connectmq.com:8883", {
  clientId: `ts-demo-${randomUUID().slice(0, 8)}`,
});

// payload is fully typed: { deviceId: string; temperature: number; humidity: number; ts: number }
mq.subscribe("telemetry", (payload, topic) => {
  console.log(`${payload.deviceId}: ${payload.temperature.toFixed(1)} C (${topic})`);
});

mq.subscribe("command", (cmd) => {
  console.log(`Command ${cmd.action} (${cmd.requestId})`);
});

await mq.publish("status", ["sensor-42"], "online");

const timer = setInterval(() => {
  mq.publish("telemetry", ["sensor-42"], {
    deviceId: "sensor-42",
    temperature: 20 + Math.random() * 5,
    humidity: 40 + Math.random() * 10,
    ts: Date.now(),
  }).catch((err) => console.error("Rejected by schema:", err.message));
}, 2000);

setTimeout(async () => {
  await mq.publish("command", ["sensor-42"], { action: "reboot", requestId: randomUUID() });
}, 5000);

// These lines do not compile, which is the point:
// mq.publish("command", ["sensor-42"], { action: "explode", requestId: "x" });
// mq.publish("telemetry", [], { deviceId: "a", temperature: "21", humidity: 1, ts: 0 });

process.on("SIGINT", async () => {
  clearInterval(timer);
  await mq.publish("status", ["sensor-42"], "offline");
  await mq.close();
  process.exit(0);
});

console.log("Telemetry topic example:", contracts.telemetry.topic("sensor-42"));
