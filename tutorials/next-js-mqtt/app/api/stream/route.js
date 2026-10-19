import { getMqttClient } from "@/lib/mqtt-server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request) {
  const client = getMqttClient();
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    start(controller) {
      const onMessage = (topic, payload) => {
        const data = JSON.stringify({ topic, payload: payload.toString() });
        controller.enqueue(encoder.encode(`data: ${data}\n\n`));
      };
      client.on("message", onMessage);
      request.signal.addEventListener("abort", () => {
        client.off("message", onMessage);
        controller.close();
      });
    },
  });

  return new Response(stream, {
    headers: { "Content-Type": "text/event-stream", "Cache-Control": "no-cache", Connection: "keep-alive" },
  });
}
