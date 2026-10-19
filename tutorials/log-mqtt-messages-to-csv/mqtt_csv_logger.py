import csv
import json
import os
import signal
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_HOST", "broker.connectmq.com")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME")          # None on the public broker
PASSWORD = os.environ.get("MQTT_PASSWORD")
CLIENT_ID = os.environ.get("MQTT_CLIENT_ID", f"csv-logger-{uuid.uuid4().hex[:8]}")
TOPICS = os.environ.get("MQTT_TOPICS", "connectmq/demo/csv-4821/#").split(",")
OUT_DIR = Path(os.environ.get("CSV_DIR", "mqtt_logs"))
MAX_BYTES = int(os.environ.get("CSV_MAX_BYTES", str(50 * 1024 * 1024)))
SKIP_RETAINED = os.environ.get("SKIP_RETAINED", "1") == "1"

FIELDS = ["received_at", "topic", "qos", "retain", "value", "payload"]


class RotatingCsvWriter:
    """Writes rows to mqtt_YYYY-MM-DD_NNN.csv, rotating daily and by size."""

    def __init__(self, directory: Path, max_bytes: int):
        self.directory = directory
        self.max_bytes = max_bytes
        self.directory.mkdir(parents=True, exist_ok=True)
        self._file = None
        self._writer = None
        self._day = None
        self._part = 0

    def _open(self, day: str):
        if self._file:
            self._file.close()
        if day != self._day:
            self._day, self._part = day, 0
        while True:
            path = self.directory / f"mqtt_{day}_{self._part:03d}.csv"
            if not path.exists() or path.stat().st_size < self.max_bytes:
                break
            self._part += 1
        new_file = not path.exists()
        # utf-8-sig adds a BOM so Excel detects UTF-8; newline="" is required by csv
        self._file = open(path, "a", newline="", encoding="utf-8-sig" if new_file else "utf-8")
        self._writer = csv.DictWriter(self._file, fieldnames=FIELDS)
        if new_file:
            self._writer.writeheader()
        print(f"Writing to {path}")

    def write(self, row: dict):
        day = row["received_at"][:10]
        if self._file is None or day != self._day or self._file.tell() >= self.max_bytes:
            if self._file is not None and day == self._day:
                self._part += 1
            self._open(day)
        self._writer.writerow(row)
        self._file.flush()

    def close(self):
        if self._file:
            self._file.close()


def extract_value(text: str):
    """Return a float from '21.4' or '{"value": 21.4}', else empty string."""
    try:
        return float(text)
    except ValueError:
        pass
    try:
        data = json.loads(text)
        if isinstance(data, dict) and isinstance(data.get("value"), (int, float)):
            return data["value"]
    except json.JSONDecodeError:
        pass
    return ""


writer = RotatingCsvWriter(OUT_DIR, MAX_BYTES)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Connect failed: {reason_code}")
        return
    print(f"Connected as {CLIENT_ID}")
    for topic in TOPICS:
        client.subscribe(topic.strip(), qos=1)


def on_message(client, userdata, msg):
    if SKIP_RETAINED and msg.retain:
        return
    text = msg.payload.decode("utf-8", errors="replace")
    writer.write({
        "received_at": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "topic": msg.topic,
        "qos": msg.qos,
        "retain": int(msg.retain),
        "value": extract_value(text),
        "payload": text,
    })


def on_disconnect(client, userdata, flags, reason_code, properties):
    print(f"Disconnected: {reason_code}, paho will reconnect")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    if PORT == 8883:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=30)

    def shutdown(*_):
        client.disconnect()
        writer.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever(retry_first_connection=True)


if __name__ == "__main__":
    main()
