import { useMemo, useState } from "react";
import { useMqtt } from "./useMqtt";

const BROKER_URL = "wss://broker.connectmq.com:8084/mqtt";
const PREFIX = "connectmq/demo/react-58d2";

function SensorCard({ device, reading }) {
  const ageSeconds = Math.round((Date.now() - reading.receivedAt) / 1000);
  const { temperature, humidity } = reading.value ?? {};
  return (
    <div className="card">
      <h3>{device}</h3>
      <p className="big">{temperature ?? "--"} &deg;C</p>
      <p>Humidity: {humidity ?? "--"} %</p>
      <small>{ageSeconds > 30 ? `stale (${ageSeconds}s)` : "live"}</small>
    </div>
  );
}

export default function App() {
  const [clientId] = useState(() => `react-${Math.random().toString(16).slice(2, 10)}`);
  const { status, messages, publish } = useMqtt(BROKER_URL, { clientId }, [`${PREFIX}/+/telemetry`]);

  const devices = useMemo(
    () =>
      Object.entries(messages)
        .map(([topic, reading]) => ({ device: topic.split("/").at(-2), reading }))
        .sort((a, b) => a.device.localeCompare(b.device)),
    [messages]
  );

  return (
    <main>
      <header>
        <h1>Live Sensors</h1>
        <span className={`status ${status}`}>{status}</span>
      </header>
      <section className="grid">
        {devices.map(({ device, reading }) => (
          <SensorCard key={device} device={device} reading={reading} />
        ))}
      </section>
      <button onClick={() => publish(`${PREFIX}/fan1/cmd`, { action: "toggle" }, { qos: 1 })}>
        Toggle fan1
      </button>
    </main>
  );
}
