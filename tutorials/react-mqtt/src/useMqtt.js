import { useCallback, useEffect, useRef, useState } from "react";
import mqtt from "mqtt";

export function useMqtt(url, options, topics) {
  const [status, setStatus] = useState("connecting");
  const [messages, setMessages] = useState({});
  const clientRef = useRef(null);
  const pendingRef = useRef({});

  // Stable keys so inline objects/arrays do not trigger reconnects
  const optionsKey = JSON.stringify(options);
  const topicsKey = JSON.stringify(topics);

  useEffect(() => {
    const opts = JSON.parse(optionsKey);
    const filters = JSON.parse(topicsKey);
    const client = mqtt.connect(url, {
      protocolVersion: 5,
      reconnectPeriod: 3000,
      connectTimeout: 10000,
      ...opts,
    });
    clientRef.current = client;

    client.on("connect", () => {
      setStatus("connected");
      client.subscribe(filters, { qos: 0 });
    });
    client.on("reconnect", () => setStatus("reconnecting"));
    client.on("offline", () => setStatus("offline"));
    client.on("error", (err) => {
      console.error("MQTT error", err);
      setStatus("error");
    });
    client.on("message", (topic, payload) => {
      let value;
      try {
        value = JSON.parse(payload.toString());
      } catch {
        value = payload.toString();
      }
      pendingRef.current[topic] = { value, receivedAt: Date.now() };
    });

    // Flush buffered messages into React state at most 4 times per second
    const timer = setInterval(() => {
      const pending = pendingRef.current;
      if (Object.keys(pending).length === 0) return;
      pendingRef.current = {};
      setMessages((prev) => ({ ...prev, ...pending }));
    }, 250);

    return () => {
      clearInterval(timer);
      client.end(true);
      clientRef.current = null;
    };
  }, [url, optionsKey, topicsKey]);

  const publish = useCallback((topic, message, publishOptions = { qos: 0 }) => {
    const client = clientRef.current;
    if (!client || !client.connected) return false;
    const body = typeof message === "string" ? message : JSON.stringify(message);
    client.publish(topic, body, publishOptions);
    return true;
  }, []);

  return { status, messages, publish };
}
