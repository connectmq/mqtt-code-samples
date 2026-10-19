import json
import math
import random
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional

import paho.mqtt.client as mqtt
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

BROKER = "broker.connectmq.com"
PORT = 1883
PREFIX = "connectmq/demo/k7f3q2"
DEVICE = "room1"
SCHEMA_VERSION = 1


@dataclass
class Reading:
    device: str
    ts: str
    seq: int
    temperature_c: Optional[float]
    humidity_pct: Optional[float]
    battery_v: Optional[float] = None
    v: int = SCHEMA_VERSION


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def clean(value: Optional[float], digits: int = 2) -> Optional[float]:
    """Round floats and turn NaN or infinity into None, which becomes JSON null."""
    if value is None or math.isnan(value) or math.isinf(value):
        return None
    return round(value, digits)


def read_sensor() -> tuple:
    # Replace with real sensor code. Occasionally simulate a failed read.
    if random.random() < 0.05:
        return float("nan"), float("nan")
    return random.uniform(20, 25), random.uniform(40, 55)


def to_payload(reading: Reading) -> bytes:
    return json.dumps(asdict(reading), separators=(",", ":"), allow_nan=False).encode("utf-8")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"json-pub-{uuid.uuid4().hex[:8]}",
    protocol=mqtt.MQTTv5,
)
# Private ConnectMQ broker: client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD"); client.tls_set(); port 8883
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

props = Properties(PacketTypes.PUBLISH)
props.ContentType = "application/json"
props.PayloadFormatIndicator = 1  # payload is UTF-8 text

topic = f"{PREFIX}/sensors/{DEVICE}/telemetry"
seq = 0
try:
    while True:
        temperature, humidity = read_sensor()
        reading = Reading(
            device=DEVICE,
            ts=utc_now_iso(),
            seq=seq,
            temperature_c=clean(temperature),
            humidity_pct=clean(humidity, 1),
        )
        payload = to_payload(reading)
        client.publish(topic, payload, qos=1, properties=props)
        print(f"{len(payload):>4} bytes  {payload.decode()}")
        seq += 1
        time.sleep(2)
except KeyboardInterrupt:
    pass
finally:
    client.disconnect()
    client.loop_stop()
