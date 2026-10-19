import { ref, reactive, readonly, onBeforeUnmount } from "vue";
import mqtt from "mqtt";

const status = ref("idle");
const messages = reactive({});
const topicUsers = new Map();
let client = null;
let users = 0;

function ensureClient(url, options) {
  if (client) return;
  client = mqtt.connect(url, { protocolVersion: 5, reconnectPeriod: 3000, ...options });
  client.on("connect", () => {
    status.value = "connected";
    const filters = [...topicUsers.keys()];
    if (filters.length) client.subscribe(filters);
  });
  client.on("reconnect", () => (status.value = "reconnecting"));
  client.on("offline", () => (status.value = "offline"));
  client.on("message", (topic, payload) => {
    let value = payload.toString();
    try { value = JSON.parse(value); } catch { /* keep text */ }
    messages[topic] = { value, receivedAt: Date.now() };
  });
}

export function useSharedMqtt(url, options, topicFilter) {
  ensureClient(url, options);
  users++;
  const count = topicUsers.get(topicFilter) ?? 0;
  topicUsers.set(topicFilter, count + 1);
  if (count === 0 && client.connected) client.subscribe(topicFilter);

  onBeforeUnmount(() => {
    const left = topicUsers.get(topicFilter) - 1;
    if (left === 0) {
      topicUsers.delete(topicFilter);
      client?.unsubscribe(topicFilter);
    } else {
      topicUsers.set(topicFilter, left);
    }
    if (--users === 0) {
      client.end(true);
      client = null;
      status.value = "disconnected";
    }
  });

  return { status: readonly(status), messages: readonly(messages) };
}
