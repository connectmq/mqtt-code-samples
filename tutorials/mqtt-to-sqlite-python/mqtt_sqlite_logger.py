import queue
import signal
import sqlite3
import time
import uuid
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PORT = 1883
TOPIC = "connectmq/demo/k7f3q2/#"
DB_PATH = "mqtt_messages.db"
BATCH_SIZE = 200
FLUSH_INTERVAL = 1.0  # seconds

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id          INTEGER PRIMARY KEY,
    received_at TEXT    NOT NULL,
    topic       TEXT    NOT NULL,
    payload     TEXT,
    qos         INTEGER NOT NULL,
    retained    INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_topic_time ON messages (topic, received_at);
CREATE INDEX IF NOT EXISTS idx_messages_time ON messages (received_at);
"""

inbox: "queue.Queue[tuple]" = queue.Queue(maxsize=50_000)
running = True


def utc_now() -> str:
    # 2026-10-16T08:15:30.123Z, sortable and understood by SQLite date functions
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Connect failed: {reason_code}")
        return
    print(f"Connected, subscribing to {TOPIC}")
    client.subscribe(TOPIC, qos=1)


def on_message(client, userdata, msg):
    row = (
        utc_now(),
        msg.topic,
        msg.payload.decode("utf-8", errors="replace"),
        msg.qos,
        int(msg.retain),
    )
    try:
        inbox.put_nowait(row)
    except queue.Full:
        print("Queue full, dropping message")  # the database cannot keep up


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"Disconnected: {reason_code}, paho will reconnect")


def open_db(path: str) -> sqlite3.Connection:
    db = sqlite3.connect(path)
    db.execute("PRAGMA journal_mode=WAL")    # readers do not block the writer
    db.execute("PRAGMA synchronous=NORMAL")  # safe with WAL, much faster
    db.executescript(SCHEMA)
    return db


def flush(db: sqlite3.Connection, batch: list) -> None:
    if not batch:
        return
    with db:  # one transaction per batch
        db.executemany(
            "INSERT INTO messages (received_at, topic, payload, qos, retained) VALUES (?, ?, ?, ?, ?)",
            batch,
        )
    print(f"Stored {len(batch)} messages")
    batch.clear()


def stop(*_):
    global running
    running = False


def main():
    signal.signal(signal.SIGINT, stop)
    signal.signal(signal.SIGTERM, stop)

    db = open_db(DB_PATH)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"sqlite-{uuid.uuid4().hex[:8]}")
    # Private ConnectMQ broker:
    # client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
    # client.tls_set(); and use port 8883
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.reconnect_delay_set(min_delay=1, max_delay=60)
    client.connect_async(BROKER, PORT, keepalive=60)
    client.loop_start()

    batch: list = []
    last_flush = time.monotonic()
    try:
        while running:
            try:
                batch.append(inbox.get(timeout=0.2))
            except queue.Empty:
                pass
            if len(batch) >= BATCH_SIZE or time.monotonic() - last_flush >= FLUSH_INTERVAL:
                flush(db, batch)
                last_flush = time.monotonic()
    finally:
        client.disconnect()
        client.loop_stop()
        while not inbox.empty():
            batch.append(inbox.get_nowait())
        flush(db, batch)
        db.close()
        print("Logger stopped cleanly")


if __name__ == "__main__":
    main()
