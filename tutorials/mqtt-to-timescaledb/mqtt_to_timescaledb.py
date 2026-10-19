import json
import logging
import os
import queue
import signal
import threading
import time
import uuid
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
import psycopg
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("bridge")

MQTT_HOST = os.getenv("MQTT_HOST", "broker.connectmq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USER = os.getenv("MQTT_USERNAME")
MQTT_PASS = os.getenv("MQTT_PASSWORD")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID") or f"tsdb-bridge-{uuid.uuid4().hex[:8]}"
PREFIX = os.getenv("MQTT_TOPIC_PREFIX", "connectmq/demo/tsdb-5b7e21")
DSN = os.getenv("PG_DSN", "postgresql://postgres:change-me@localhost:5432/postgres")

BATCH_SIZE = 1000
FLUSH_SECONDS = 1.0
MAX_QUEUE = 100_000

rows: "queue.Queue[tuple]" = queue.Queue(maxsize=MAX_QUEUE)
stop = threading.Event()


def parse(topic: str, payload: bytes):
    """Turn one MQTT message into (time, device_id, metric, value) rows."""
    parts = topic.split("/")
    if len(parts) < 2 or parts[-1] != "telemetry":
        return []
    device_id = parts[-2]
    data = json.loads(payload)
    if not isinstance(data, dict):
        return []
    ts = data.pop("ts", None)
    when = (datetime.fromtimestamp(float(ts), tz=timezone.utc)
            if isinstance(ts, (int, float)) else datetime.now(timezone.utc))
    out = []
    for metric, value in data.items():
        if isinstance(value, bool):
            value = float(value)
        if isinstance(value, (int, float)):
            out.append((when, device_id, metric[:64], float(value)))
    return out


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        log.error("connect failed: %s", reason_code)
        return
    log.info("connected (session present: %s)", flags.session_present)
    client.subscribe(f"{PREFIX}/+/telemetry", qos=1)


def on_message(client, userdata, msg):
    try:
        for row in parse(msg.topic, msg.payload):
            rows.put_nowait(row)
    except (ValueError, json.JSONDecodeError):
        log.warning("bad payload on %s", msg.topic)
    except queue.Full:
        log.error("queue full, dropping message from %s", msg.topic)


def writer():
    conn = None
    batch = []
    last_flush = time.monotonic()
    while not (stop.is_set() and rows.empty() and not batch):
        try:
            batch.append(rows.get(timeout=0.2))
            if len(batch) < BATCH_SIZE and time.monotonic() - last_flush < FLUSH_SECONDS:
                continue
        except queue.Empty:
            if not batch:
                continue
        try:
            if conn is None or conn.closed:
                conn = psycopg.connect(DSN, autocommit=False)
            with conn.cursor() as cur:
                with cur.copy("COPY readings (time, device_id, metric, value) FROM STDIN") as cp:
                    for r in batch:
                        cp.write_row(r)
            conn.commit()
            log.info("wrote %d rows", len(batch))
            batch.clear()
            last_flush = time.monotonic()
        except psycopg.Error as e:
            log.error("database error, retrying in 5 s: %s", e)
            if conn is not None:
                conn.close()
            conn = None
            time.sleep(5)  # keep the batch and retry
    if conn is not None:
        conn.close()


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID,
                         protocol=mqtt.MQTTv5)
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    if MQTT_PORT == 8883:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=60)

    # Persistent session: the broker queues QoS 1 messages while the bridge restarts
    props = Properties(PacketTypes.CONNECT)
    props.SessionExpiryInterval = 1800

    t = threading.Thread(target=writer, daemon=True)
    t.start()

    def shutdown(*_):
        log.info("shutting down")
        client.disconnect()
        stop.set()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    client.connect(MQTT_HOST, MQTT_PORT, keepalive=30, clean_start=False, properties=props)
    client.loop_forever(retry_first_connection=True)
    t.join(timeout=30)


if __name__ == "__main__":
    main()
