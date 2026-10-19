import { MongoClient } from "mongodb";

const uri = process.env.MONGO_URI ?? "mongodb://localhost:27017";
const client = new MongoClient(uri);
await client.connect();
const db = client.db("iot");

try {
  await db.createCollection("telemetry", {
    timeseries: { timeField: "ts", metaField: "meta", granularity: "seconds" },
    expireAfterSeconds: 60 * 60 * 24 * 90, // keep 90 days
  });
  console.log("created time-series collection iot.telemetry");
} catch (err) {
  if (err.codeName === "NamespaceExists") console.log("collection already exists");
  else throw err;
}

await db.collection("telemetry").createIndex({ "meta.deviceId": 1, ts: -1 });
await client.close();
