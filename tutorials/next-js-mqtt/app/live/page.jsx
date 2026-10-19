"use client";

import { useMqtt } from "../hooks/useMqtt";

const PREFIX = "connectmq/demo/next-k7f3q2";

export default function LivePage() {
  const { status, messages } = useMqtt(`${PREFIX}/sensors/#`);

  return (
    <main style={{ padding: 24 }}>
      <h1>Live sensors</h1>
      <p>Broker: {status}</p>
      <ul>
        {messages.map((m) => (
          <li key={m.at + m.topic}>{m.topic}: {m.text}</li>
        ))}
      </ul>
    </main>
  );
}
