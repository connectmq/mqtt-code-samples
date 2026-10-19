"use client";

import { useEffect, useRef, useState } from "react";
import mqtt from "mqtt";

const BROKER_URL = process.env.NEXT_PUBLIC_MQTT_URL ?? "wss://broker.connectmq.com:8084/mqtt";

export function useMqtt(topic) {
  const clientRef = useRef(null);
  const [status, setStatus] = useState("connecting");
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const clientId = "next-" + Math.random().toString(16).slice(2, 10);
    const client = mqtt.connect(BROKER_URL, {
      clientId,
      protocolVersion: 5,
      clean: true,
      keepalive: 30,
      reconnectPeriod: 3000,
    });
    clientRef.current = client;

    client.on("connect", () => {
      setStatus("connected");
      client.subscribe(topic, { qos: 1 });
    });
    client.on("reconnect", () => setStatus("reconnecting"));
    client.on("close", () => setStatus("disconnected"));
    client.on("message", (t, payload) => {
      setMessages((prev) => [...prev.slice(-99), { topic: t, text: payload.toString(), at: Date.now() }]);
    });

    return () => {
      client.end(true);
      clientRef.current = null;
    };
  }, [topic]);

  const publish = (t, payload) => clientRef.current?.publish(t, payload, { qos: 1 });

  return { status, messages, publish };
}
