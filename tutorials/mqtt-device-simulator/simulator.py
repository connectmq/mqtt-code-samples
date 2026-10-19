import argparse
import heapq
import json
import math
import random
import time
import uuid

import paho.mqtt.client as mqtt


class VirtualSensor:
    """One simulated temperature and humidity sensor with persistent state."""

    def __init__(self, index: int, fault_rate: float):
        self.device_id = f"sensor-{index:04d}"
        self.line = f"line{index % 4 + 1}"
        self.base_temp = random.uniform(19.0, 24.0)
        self.humidity = random.uniform(35.0, 55.0)
        self.phase = random.uniform(0, 2 * math.pi)
        self.drift = 0.0
        self.faulty = random.random() < fault_rate

    def read(self, now: float) -> dict:
        # Slow daily cycle of +/- 2.5 degrees, shifted per device
        daily = 2.5 * math.sin(2 * math.pi * (now % 86400) / 86400 + self.phase)
        # Bounded random walk to mimic calibration drift
        self.drift = max(-3.0, min(3.0, self.drift + random.gauss(0, 0.05)))
        # Gaussian measurement noise
        temp = self.base_temp + daily + self.drift + random.gauss(0, 0.15)
        self.humidity = max(10.0, min(95.0, self.humidity + random.gauss(0, 0.3)))
        # Faulty devices occasionally emit physically implausible spikes
        if self.faulty and random.random() < 0.05:
            temp += random.choice([-40.0, 60.0])
        return {
            "device": self.device_id,
            "ts": int(now * 1000),
            "temperature": round(temp, 2),
            "humidity": round(self.humidity, 1),
        }


def build_client(args, run_id: str) -> mqtt.Client:
    client_id = args.client_id or f"sim-{run_id}"
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    if args.username:
        client.username_pw_set(args.username, args.password)
    if args.tls:
        client.tls_set()  # system CA store; the broker uses a Let's Encrypt certificate

    def on_connect(client, userdata, flags, reason_code, properties):
        print(f"connected: {reason_code}")

    def on_disconnect(client, userdata, flags, reason_code, properties):
        print(f"disconnected: {reason_code}")

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    return client


def main():
    parser = argparse.ArgumentParser(description="MQTT device simulator")
    parser.add_argument("--host", default="broker.connectmq.com")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--tls", action="store_true")
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--client-id")
    parser.add_argument("--prefix", help="topic prefix, default connectmq/demo/<run-id>")
    parser.add_argument("--devices", type=int, default=200)
    parser.add_argument("--interval", type=float, default=30.0)
    parser.add_argument("--max-rate", type=float, default=8.0)
    parser.add_argument("--fault-rate", type=float, default=0.02)
    parser.add_argument("--dropout", type=float, default=0.01)
    args = parser.parse_args()

    run_id = uuid.uuid4().hex[:8]
    prefix = args.prefix or f"connectmq/demo/{run_id}"
    expected = args.devices / args.interval
    if expected > args.max_rate:
        raise SystemExit(f"{expected:.1f} msg/s exceeds --max-rate {args.max_rate}")
    print(f"publishing to {prefix}/# at about {expected:.1f} msg/s")

    sensors = [VirtualSensor(i, args.fault_rate) for i in range(args.devices)]
    client = build_client(args, run_id)
    client.connect_async(args.host, args.port, keepalive=30)
    client.loop_start()

    start = time.time()
    # Spread first readings evenly over one interval
    schedule = [(start + i * args.interval / args.devices, i) for i in range(args.devices)]
    heapq.heapify(schedule)
    min_gap = 1.0 / args.max_rate
    last_send = 0.0

    try:
        while True:
            due, i = heapq.heappop(schedule)
            now = time.time()
            wait = max(due - now, last_send + min_gap - now)
            if wait > 0:
                time.sleep(wait)
            sensor = sensors[i]
            now = time.time()
            if random.random() >= args.dropout and client.is_connected():
                topic = f"{prefix}/{sensor.line}/{sensor.device_id}/telemetry"
                client.publish(topic, json.dumps(sensor.read(now)), qos=0)
                last_send = time.time()
            heapq.heappush(schedule, (due + args.interval, i))
    except KeyboardInterrupt:
        print("stopping")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
