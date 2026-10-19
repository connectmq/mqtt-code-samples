import json
import threading
import time
import uuid
from collections import deque

import pandas as pd
import paho.mqtt.client as mqtt
import streamlit as st

BROKER = "broker.connectmq.com"
PORT = 1883
PREFIX = "connectmq/demo/k7f3q2"
TOPIC = f"{PREFIX}/sensors/+"
MAX_POINTS = 600


@st.cache_resource
def start_mqtt():
    """Create one MQTT client per Streamlit server process."""
    state = {
        "buffer": deque(maxlen=MAX_POINTS),
        "lock": threading.Lock(),
        "connected": False,
        "received": 0,
    }

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            return
        state["connected"] = True
        client.subscribe(TOPIC, qos=0)

    def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
        state["connected"] = False

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload)
            row = {
                "time": pd.to_datetime(data.get("ts", time.time()), unit="s"),
                "sensor": data.get("sensor", msg.topic.rsplit("/", 1)[-1]),
                "temperature": float(data["temperature"]),
                "humidity": float(data["humidity"]),
            }
        except (ValueError, KeyError, TypeError):
            return  # ignore malformed payloads
        with state["lock"]:
            state["buffer"].append(row)
            state["received"] += 1

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id=f"streamlit-{uuid.uuid4().hex[:8]}",
    )
    # For a private ConnectMQ broker:
    # client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
    # client.tls_set()  and use port 8883
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    client.connect_async(BROKER, PORT, keepalive=60)
    client.loop_start()
    return state


st.set_page_config(page_title="MQTT Sensor Dashboard", layout="wide")
st.title("Live MQTT Sensor Dashboard")
st.caption(f"Subscribed to `{TOPIC}` on {BROKER}")

state = start_mqtt()


@st.fragment(run_every=2)
def live_view():
    with state["lock"]:
        rows = list(state["buffer"])
        received = state["received"]

    status = "Connected" if state["connected"] else "Connecting..."
    c1, c2, c3 = st.columns(3)
    c1.metric("Broker status", status)
    c2.metric("Messages received", received)
    c3.metric("Points in buffer", len(rows))

    if not rows:
        st.info("Waiting for data. Is simulator.py running with the same prefix?")
        return

    df = pd.DataFrame(rows)
    latest = df.groupby("sensor").last()

    cols = st.columns(len(latest))
    for col, (sensor, r) in zip(cols, latest.iterrows()):
        col.metric(f"{sensor} temperature", f"{r['temperature']:.1f} °C")

    temp = df.pivot_table(index="time", columns="sensor", values="temperature")
    hum = df.pivot_table(index="time", columns="sensor", values="humidity")

    left, right = st.columns(2)
    left.subheader("Temperature")
    left.line_chart(temp)
    right.subheader("Humidity")
    right.line_chart(hum)


live_view()
