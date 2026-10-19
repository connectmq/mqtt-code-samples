import json
import uuid

import paho.mqtt.client as mqtt

PREFIX = "connectmq/demo/k7f3q2"
REQUIRED = {"v", "device", "ts", "seq"}


def parse_reading(raw: bytes):
    try:
        data = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"not valid JSON: {exc}")
    if not isinstance(data, dict) or not REQUIRED <= data.keys():
        raise ValueError("missing required fields")
    if data["v"] != 1:
        raise ValueError(f"unsupported schema version {data['v']}")
    return data


def on_connect(client, userdata, flags, reason_code, properties):
    client.subscribe(f"{PREFIX}/sensors/+/telemetry", qos=1)


def on_message(client, userdata, msg):
    try:
        r = parse_reading(msg.payload)
    except ValueError as exc:
        print(f"Rejected message on {msg.topic}: {exc}")
        return
    print(f"{r['device']} #{r['seq']} at {r['ts']}: {r.get('temperature_c')} C, {r.get('humidity_pct')} %")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"json-sub-{uuid.uuid4().hex[:8]}")
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.connectmq.com", 1883, keepalive=60)
client.loop_forever()
