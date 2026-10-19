import mqtt from "mqtt";
import { MongoClient } from "mongodb";
import { randomBytes } from "node:crypto";

const MQTT_URL = process.env.MQTT_URL ?? "mqtts://broker.connectmq.com:8883";
const PREFIX = process.env.MQTT_TOPIC_PREFIX ?? "connectmq/demo/mongo-9d42a7";
const CLIENT_ID = process.env.MQTT_CLIENT_ID ?? `mongo-sink-${randomBytes(4).toString("hex")}`;
const MONGO_URI = process.env.MONGO_URI ?? "mongodb://localhost:27017";

const BATCH_SIZE = 500;
const FLUSH_MS = 1000;
const MAX_BUFFER = 50_000;

const mongo = new MongoClient(MONGO_URI);
await mongo.connect();
const telemetry = mongo.db("iot").collection("telemetry");

let buffer = [];
let flushing = false;

function toDocument(topic, payload) {
  // <prefix>/<site>/<deviceId>/telemetry
  const parts = topic.split("/");
  if (parts.length < 3 || parts.at(-1) !== "telemetry") return null;
  const deviceId = parts.at(-2);
  const site = parts.at(-3);

  let data;
  try {
    data = JSON.parse(payload.toString());
  } catch {
    return null;
  }
  if (typeof data !== "object" || data === null || Array.isArray(data)) return null;

  const { ts, ...fields } = data;
  const when = ts ? new Date(ts) : new Date();
  if (Number.isNaN(when.getTime())) return null;

  const doc = { ts: when, meta: { site, deviceId }, receivedAt: new Date() };
  for (const [key, value] of Object.entries(fields)) {
    if (key.startsWith("$") || key.includes(".")) continue; // unsafe field names
    if (["number", "string", "boolean"].includes(typeof value)) doc[key] = value;
  }
  return doc;
}

async function flush() {
  if (flushing || buffer.length === 0) return;
  flushing = true;
  const batch = buffer;
  buffer = [];
  try {
    await telemetry.insertMany(batch, { ordered: false });
    console.log(`inserted ${batch.length} documents`);
  } catch (err) {
    console.error("insert failed, re-queueing batch:", err.message);
    buffer = batch.concat(buffer).slice(-MAX_BUFFER);
  } finally {
    flushing = false;
  }
}

const timer = setInterval(flush, FLUSH_MS);

const client = mqtt.connect(MQTT_URL, {
  clientId: CLIENT_ID,
  username: process.env.MQTT_USERNAME,
  password: process.env.MQTT_PASSWORD,
  protocolVersion: 5,
  clean: false,                                   // persistent session
  properties: { sessionExpiryInterval: 1800 },    // broker keeps it for 30 min
  keepalive: 30,
  reconnectPeriod: 2000,
});

client.on("connect", (connack) => {
  console.log(`connected as ${CLIENT_ID}, session present: ${connack.sessionPresent}`);
  client.subscribe(`${PREFIX}/+/+/telemetry`, { qos: 1 }, (err) => {
    if (err) console.error("subscribe failed:", err.message);
  });
});

client.on("message", (topic, payload) => {
  const doc = toDocument(topic, payload);
  if (!doc) return;
  if (buffer.length >= MAX_BUFFER) {
    console.error("buffer full, dropping message");
    return;
  }
  buffer.push(doc);
  if (buffer.length >= BATCH_SIZE) flush();
});

client.on("error", (err) => console.error("mqtt error:", err.message));
client.on("reconnect", () => console.log("reconnecting..."));

async function shutdown() {
  console.log("shutting down");
  clearInterval(timer);
  await client.endAsync();
  await flush();
  await mongo.close();
  process.exit(0);
}
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
