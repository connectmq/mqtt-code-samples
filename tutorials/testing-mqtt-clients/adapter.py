import threading

import paho.mqtt.client as mqtt
from thermostat import Thermostat


def build_client(host, port, client_id, prefix, username=None, password=None, tls=False):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
    if username:
        client.username_pw_set(username, password)
    if tls:
        client.tls_set()

    thermostat = Thermostat(
        prefix=prefix,
        publish=lambda t, p, q, r: client.publish(t, p, qos=q, retain=r),
    )

    def on_connect(client, userdata, flags, reason_code, properties):
        if not reason_code.is_failure:
            client.subscribe(f"{prefix}/+/temperature", qos=1)

    ready = threading.Event()

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        ready.set()

    def on_message(client, userdata, msg):
        thermostat.on_temperature(msg.topic, msg.payload)

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(host, port, keepalive=30)
    return client, thermostat, ready
