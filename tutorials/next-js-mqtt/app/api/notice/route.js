import mqtt from "mqtt";

export const runtime = "nodejs";

export async function POST(request) {
  const { message } = await request.json();
  const client = await mqtt.connectAsync(process.env.MQTT_URL, {
    clientId: "next-fn-" + Math.random().toString(16).slice(2, 10),
    username: process.env.MQTT_USERNAME,
    password: process.env.MQTT_PASSWORD,
  });
  try {
    await client.publishAsync("connectmq/demo/next-k7f3q2/notices", String(message), { qos: 1 });
  } finally {
    await client.endAsync();
  }
  return Response.json({ ok: true });
}
