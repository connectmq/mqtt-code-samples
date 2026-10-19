import json
import time
import uuid
from collections import deque

import pandas as pd
import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PORT = 1883
RUN_ID = "3f9a1c2e"  # replace with your simulator run ID
TOPIC = f"connectmq/demo/{RUN_ID}/+/+/telemetry"
WINDOW = pd.Timedelta(minutes=15)  # how much history to keep in memory
ANALYSE_EVERY_S = 10
EXPECTED_INTERVAL_S = 30

inbox: deque = deque(maxlen=100_000)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"connect failed: {reason_code}")
        return
    client.subscribe(TOPIC, qos=0)
    print(f"subscribed to {TOPIC}")


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return  # ignore non-JSON payloads
    levels = msg.topic.split("/")
    inbox.append({
        "ts": data.get("ts", int(time.time() * 1000)),
        "line": levels[3],
        "device": levels[4],
        "temperature": data.get("temperature"),
        "humidity": data.get("humidity"),
    })


def drain() -> pd.DataFrame:
    rows = []
    while inbox:
        rows.append(inbox.popleft())
    if not rows:
        return pd.DataFrame()
    df = pd.DataFrame(rows)
    df["ts"] = pd.to_datetime(df["ts"], unit="ms", utc=True)
    df["temperature"] = pd.to_numeric(df["temperature"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    return df


def analyse(window: pd.DataFrame) -> None:
    now = pd.Timestamp.now(tz="UTC")
    w = window.sort_values("ts")

    # 1. Rolling 5-minute mean per device (time-based window)
    rolling = (
        w.groupby("device")
        .rolling("5min", on="ts")["temperature"]
        .mean()
        .groupby(level=0)
        .last()
        .rename("temp_5min_mean")
    )

    # 2. Per-line, per-minute resample
    per_minute = (
        w.set_index("ts")
        .groupby("line")["temperature"]
        .resample("1min")
        .mean()
        .unstack(level=0)
        .round(2)
    )

    # 3. Robust anomaly flag: distance from the device median in MAD units
    med = w.groupby("device")["temperature"].transform("median")
    mad = (w["temperature"] - med).abs().groupby(w["device"]).transform("median")
    w = w.assign(score=(w["temperature"] - med).abs() / (mad * 1.4826 + 1e-9))
    anomalies = w[(w["score"] > 6) & (w["ts"] > now - pd.Timedelta(seconds=ANALYSE_EVERY_S * 2))]

    # 4. Stale devices: not seen for more than two intervals
    last_seen = w.groupby("device")["ts"].max()
    stale = last_seen[last_seen < now - pd.Timedelta(seconds=EXPECTED_INTERVAL_S * 2)]

    print(f"\n=== {now:%H:%M:%S} | rows {len(w)} | devices {w['device'].nunique()} ===")
    print("Per-line means, last 3 minutes:")
    print(per_minute.tail(3).to_string())
    print("Hottest devices by 5-min mean:")
    print(rolling.sort_values(ascending=False).head(5).round(2).to_string())
    if not anomalies.empty:
        print("Anomalies:")
        print(anomalies[["ts", "device", "temperature"]].to_string(index=False))
    if not stale.empty:
        print(f"Stale devices: {', '.join(stale.index[:10])}")


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"pandas-{uuid.uuid4().hex[:8]}")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=30)
    client.loop_start()

    window = pd.DataFrame()
    try:
        while True:
            time.sleep(ANALYSE_EVERY_S)
            new = drain()
            if not new.empty:
                window = pd.concat([window, new], ignore_index=True)
            if window.empty:
                continue
            cutoff = pd.Timestamp.now(tz="UTC") - WINDOW
            window = window[window["ts"] >= cutoff].reset_index(drop=True)
            analyse(window)
    except KeyboardInterrupt:
        window.to_csv("mqtt_snapshot.csv", index=False)
        print("saved mqtt_snapshot.csv")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
