import json
import os
import queue
import threading
import time
import uuid
from datetime import datetime, timezone

import gspread
import paho.mqtt.client as mqtt

BROKER = os.environ.get("MQTT_HOST", "broker.connectmq.com")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME")
PASSWORD = os.environ.get("MQTT_PASSWORD")
CLIENT_ID = os.environ.get("MQTT_CLIENT_ID", f"sheets-bridge-{uuid.uuid4().hex[:8]}")
PREFIX = os.environ.get("TOPIC_PREFIX", "connectmq/demo/gsheet-5307")
SHEET_KEY = os.environ["SHEET_KEY"]
WORKSHEET = os.environ.get("WORKSHEET", "Readings")
FLUSH_SECONDS = int(os.environ.get("FLUSH_SECONDS", "30"))
MAX_BATCH = int(os.environ.get("MAX_BATCH", "500"))

rows: "queue.Queue[list]" = queue.Queue(maxsize=50_000)
stop = threading.Event()


def parse_value(text: str):
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
    return None


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT connect failed: {reason_code}")
        return
    client.subscribe(f"{PREFIX}/+/+", qos=1)
    print(f"Subscribed to {PREFIX}/+/+")


def on_message(client, userdata, msg):
    if msg.retain:
        return  # avoid duplicate rows every time we reconnect
    parts = msg.topic.split("/")
    device, metric = parts[-2], parts[-1]
    value = parse_value(msg.payload.decode("utf-8", errors="replace"))
    if value is None:
        return
    row = [datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), device, metric, value, msg.topic]
    try:
        rows.put_nowait(row)
    except queue.Full:
        print("Buffer full, dropping row")


def flush_worker(ws: gspread.Worksheet):
    backoff = 5
    pending: list = []
    while not stop.is_set() or pending or not rows.empty():
        stop.wait(FLUSH_SECONDS)
        while len(pending) < MAX_BATCH:
            try:
                pending.append(rows.get_nowait())
            except queue.Empty:
                break
        if not pending:
            continue
        try:
            ws.append_rows(pending, value_input_option="USER_ENTERED")
            print(f"Appended {len(pending)} rows")
            pending = []
            backoff = 5
        except gspread.exceptions.APIError as exc:
            # 429 (quota) or 5xx: keep the rows and retry later
            print(f"Sheets API error, retrying in {backoff}s: {exc}")
            time.sleep(backoff)
            backoff = min(backoff * 2, 300)


def main():
    gc = gspread.service_account(filename="service_account.json")
    ws = gc.open_by_key(SHEET_KEY).worksheet(WORKSHEET)

    worker = threading.Thread(target=flush_worker, args=(ws,), daemon=True)
    worker.start()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    if PORT == 8883:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping, flushing remaining rows...")
        client.loop_stop()
        client.disconnect()
        stop.set()
        worker.join(timeout=FLUSH_SECONDS + 30)


if __name__ == "__main__":
    main()
