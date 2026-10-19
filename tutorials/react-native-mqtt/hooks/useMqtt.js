import { useEffect, useRef, useState, useCallback } from "react";
import { AppState } from "react-native";
import mqtt from "mqtt";

const BROKER_URL = "wss://broker.connectmq.com:8084/mqtt";

export function useMqtt({ topics, username, password, clientId }) {
  const clientRef = useRef(null);
  const [status, setStatus] = useState("idle");
  const [messages, setMessages] = useState({});
  const idRef = useRef(clientId || `rn-${Math.random().toString(16).slice(2, 10)}`);

  const connect = useCallback(() => {
    if (clientRef.current) return;

    const client = mqtt.connect(BROKER_URL, {
      clientId: idRef.current,
      username,
      password,
      protocolVersion: 5,
      clean: true,
      keepalive: 30,
      reconnectPeriod: 2000,
      connectTimeout: 10000,
    });
    clientRef.current = client;
    setStatus("connecting");

    client.on("connect", () => {
      setStatus("connected");
      client.subscribe(topics, { qos: 1 }, (err) => {
        if (err) console.warn("subscribe failed", err.message);
      });
    });
    client.on("reconnect", () => setStatus("reconnecting"));
    client.on("offline", () => setStatus("offline"));
    client.on("error", (err) => console.warn("mqtt error", err.message));
    client.on("message", (topic, payload) => {
      setMessages((prev) => ({ ...prev, [topic]: payload.toString() }));
    });
  }, [topics, username, password]);

  const disconnect = useCallback(() => {
    const client = clientRef.current;
    clientRef.current = null;
    if (client) client.end(true);
    setStatus("idle");
  }, []);

  const publish = useCallback((topic, message) => {
    clientRef.current?.publish(topic, message, { qos: 1 });
  }, []);

  useEffect(() => {
    connect();
    const sub = AppState.addEventListener("change", (state) => {
      if (state === "active") connect();
      else if (state === "background") disconnect();
    });
    return () => {
      sub.remove();
      disconnect();
    };
  }, [connect, disconnect]);

  return { status, messages, publish, clientId: idRef.current };
}
