import { getMqttClient } from "@/lib/mqtt-server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const PREFIX = "connectmq/demo/next-k7f3q2";
const ALLOWED = new Set(["on", "off"]);

export async function POST(request) {
  const { deviceId, action } = await request.json();

  if (!/^[a-z0-9-]{1,32}$/.test(deviceId ?? "") || !ALLOWED.has(action)) {
    return Response.json({ error: "invalid command" }, { status: 400 });
  }
  // Check the user's session or role here before publishing.

  await getMqttClient().publishAsync(
    `${PREFIX}/devices/${deviceId}/cmd`,
    JSON.stringify({ action, at: new Date().toISOString() }),
    { qos: 1 }
  );
  return Response.json({ ok: true });
}
