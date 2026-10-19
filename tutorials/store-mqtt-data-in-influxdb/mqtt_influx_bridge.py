import json
import logging
import os
import signal
import time
import uuid

import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WritePrecision, WriteOptions

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("bridge")

# --- configuration ---------------------------------------------------------
MQTT_HOST = os.getenv("MQTT_HOST", "broker.connectmq.com")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TLS = os.getenv("MQTT_TLS", "0") == "1"
MQTT_USER = os.getenv("MQTT_USERNAME")
MQTT_PASS = os.getenv("MQTT_PASSWORD")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID", f"influx-bridge-{uuid.uuid4().hex[:8]}")
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "connectmq/demo/a1b2c3/+/+/telemetry")
# One name per topic level: "_" ignores a level, "@measurement" names the measurement
TOPIC_SCHEMA = os.getenv("TOPIC_SCHEMA", "_/_/_/line/device/@measurement").split("/")

INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.environ["INFLUX_TOKEN"]
INFLUX_ORG = os.getenv("INFLUX_ORG", "iot")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "sensors")

SKIP_KEYS = {"ts", "device"}  # payload keys that are not fields

# --- InfluxDB --------------------------------------------------------------
influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx.write_api(write_options=WriteOptions(
    batch_size=500, flush_interval=5_000, retry_interval=5_000, max_retries=5))

stats = {"written": 0, "skipped": 0}


def to_point(topic: str, payload: bytes):
    levels = topic.split("/")
    if len(levels) != len(TOPIC_SCHEMA):
        return None
    try:
        data = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None

    measurement = "mqtt"
    tags = {}
    for name, value in zip(TOPIC_SCHEMA, levels):
        if name == "_":
            continue
        if name == "@measurement":
            measurement = value
        else:
            tags[name] = value

    point = Point(measurement)
    for k, v in tags.items():
        point = point.tag(k, v)

    fields = 0
    for key, value in data.items():
        if key in SKIP_KEYS:
            continue
        if isinstance(value, bool):
            point = point.field(key, value)
        elif isinstance(value, (int, float)):
            point = point.field(key, float(value))  # avoid int/float type conflicts
        elif isinstance(value, str) and len(value) <= 64:
            point = point.field(key, value)
        else:
            continue
        fields += 1
    if fields == 0:
        return None

    ts = data.get("ts")
    if isinstance(ts, (int, float)) and ts > 1e12:  # looks like milliseconds
        point = point.time(int(ts), WritePrecision.MS)
    else:
        point = point.time(time.time_ns(), WritePrecision.NS)
    return point


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        log.error("MQTT connect failed: %s", reason_code)
        return
    client.subscribe(MQTT_TOPIC, qos=1)
    log.info("subscribed to %s", MQTT_TOPIC)


def on_message(client, userdata, msg):
    point = to_point(msg.topic, msg.payload)
    if point is None:
        stats["skipped"] += 1
        return
    write_api.write(bucket=INFLUX_BUCKET, record=point)  # buffered, non-blocking
    stats["written"] += 1


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=MQTT_CLIENT_ID)
    if MQTT_USER:
        client.username_pw_set(MQTT_USER, MQTT_PASS)
    if MQTT_TLS:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=60)
    client.connect_async(MQTT_HOST, MQTT_PORT, keepalive=30)
    client.loop_start()

    running = True

    def stop(*_):
        nonlocal running
        running = False

    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    while running:
        time.sleep(30)
        log.info("written=%d skipped=%d", stats["written"], stats["skipped"])

    client.loop_stop()
    client.disconnect()
    write_api.close()  # flushes pending points
    influx.close()


if __name__ == "__main__":
    main()
