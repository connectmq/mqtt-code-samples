import { ref, reactive, readonly, onMounted, onBeforeUnmount } from "vue";
import mqtt from "mqtt";

export function useMqtt(url, options = {}, topics = []) {
  const status = ref("idle");
  const error = ref(null);
  // latest message per topic: { [topic]: { value, receivedAt } }
  const messages = reactive({});
  // plain variable, NOT reactive: Vue must never proxy the MQTT client
  let client = null;

  function parse(payload) {
    const text = payload.toString();
    try {
      return JSON.parse(text);
    } catch {
      return text;
    }
  }

  function connect() {
    status.value = "connecting";
    client = mqtt.connect(url, {
      protocolVersion: 5,
      reconnectPeriod: 3000,
      connectTimeout: 10000,
      ...options,
    });

    client.on("connect", () => {
      status.value = "connected";
      error.value = null;
      if (topics.length) client.subscribe(topics, { qos: 0 });
    });
    client.on("reconnect", () => (status.value = "reconnecting"));
    client.on("offline", () => (status.value = "offline"));
    client.on("error", (err) => (error.value = err.message));
    client.on("message", (topic, payload) => {
      messages[topic] = { value: parse(payload), receivedAt: Date.now() };
    });
  }

  function publish(topic, message, publishOptions = { qos: 0 }) {
    if (!client || !client.connected) return false;
    const body = typeof message === "string" ? message : JSON.stringify(message);
    client.publish(topic, body, publishOptions);
    return true;
  }

  function disconnect() {
    if (client) {
      client.end(true);
      client = null;
    }
    status.value = "disconnected";
  }

  onMounted(connect);
  onBeforeUnmount(disconnect);

  return {
    status: readonly(status),
    error: readonly(error),
    messages: readonly(messages),
    publish,
    disconnect,
  };
}
