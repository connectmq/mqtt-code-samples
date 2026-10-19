import json
import os
import threading
import time
import uuid
from functools import wraps

import paho.mqtt.client as mqtt
from flask import Flask, abort, jsonify, request

BROKER = os.environ.get("MQTT_HOST", "broker.connectmq.com")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME")
PASSWORD = os.environ.get("MQTT_PASSWORD")
CLIENT_ID = os.environ.get("MQTT_CLIENT_ID", f"flask-bridge-{uuid.uuid4().hex[:8]}")
PREFIX = os.environ.get("TOPIC_PREFIX", "connectmq/demo/flask-3391")
API_KEY = os.environ.get("API_KEY", "change-me")
STALE_AFTER = int(os.environ.get("STALE_AFTER", "120"))  # seconds

app = Flask(__name__)
cache = {}                 # device -> {"data": ..., "topic": ..., "received_at": ...}
cache_lock = threading.Lock()
mqtt_connected = threading.Event()


# ---------- MQTT ----------

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT connect failed: {reason_code}")
        return
    mqtt_connected.set()
    client.subscribe(f"{PREFIX}/+/state", qos=1)


def on_disconnect(client, userdata, flags, reason_code, properties):
    mqtt_connected.clear()


def on_message(client, userdata, msg):
    device = msg.topic.split("/")[-2]
    try:
        data = json.loads(msg.payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        data = msg.payload.decode("utf-8", errors="replace")
    with cache_lock:
        cache[device] = {"data": data, "topic": msg.topic, "received_at": time.time()}


mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
if USERNAME:
    mqttc.username_pw_set(USERNAME, PASSWORD)
if PORT == 8883:
    mqttc.tls_set()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message
mqttc.connect_async(BROKER, PORT, keepalive=60)
mqttc.loop_start()


# ---------- HTTP ----------

def require_api_key(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if request.headers.get("X-API-Key") != API_KEY:
            abort(401)
        return view(*args, **kwargs)
    return wrapper


def serialize(device, entry):
    age = time.time() - entry["received_at"]
    return {
        "device": device,
        "data": entry["data"],
        "topic": entry["topic"],
        "age_seconds": round(age, 1),
        "stale": age > STALE_AFTER,
    }


@app.get("/health")
def health():
    ok = mqtt_connected.is_set()
    return jsonify({"mqtt_connected": ok}), (200 if ok else 503)


@app.get("/api/devices")
@require_api_key
def list_devices():
    with cache_lock:
        items = [serialize(d, e) for d, e in sorted(cache.items())]
    return jsonify(items)


@app.get("/api/devices/<device>")
@require_api_key
def get_device(device):
    with cache_lock:
        entry = cache.get(device)
        if entry is None:
            abort(404)
        return jsonify(serialize(device, entry))


@app.post("/api/devices/<device>/command")
@require_api_key
def send_command(device):
    if any(ch in device for ch in "/+#"):
        abort(400)
    body = request.get_json(silent=True)
    if not isinstance(body, dict) or "action" not in body:
        return jsonify({"error": "JSON body with an 'action' field is required"}), 400
    if not mqtt_connected.is_set():
        return jsonify({"error": "MQTT broker not connected"}), 503

    body["request_id"] = uuid.uuid4().hex
    info = mqttc.publish(f"{PREFIX}/{device}/cmd", json.dumps(body), qos=1)
    try:
        info.wait_for_publish(timeout=5)
    except (ValueError, RuntimeError):
        pass
    if not info.is_published():
        return jsonify({"error": "publish not acknowledged"}), 504
    return jsonify({"published": True, "request_id": body["request_id"]}), 202


if __name__ == "__main__":
    # use_reloader=False is essential: the reloader would start a second MQTT client
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
