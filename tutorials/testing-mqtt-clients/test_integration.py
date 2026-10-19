import os
import queue
import uuid

import paho.mqtt.client as mqtt
import pytest

from adapter import build_client

HOST = os.getenv("MQTT_TEST_HOST", "localhost")
PORT = int(os.getenv("MQTT_TEST_PORT", "1883"))


@pytest.fixture
def prefix():
    return f"test/{uuid.uuid4().hex[:8]}"


@pytest.fixture
def probe(prefix):
    received = queue.Queue()
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"probe-{uuid.uuid4().hex[:8]}")
    c.on_message = lambda cl, ud, m: received.put((m.topic, m.payload.decode(), m.retain))
    c.connect(HOST, PORT)
    c.subscribe(f"{prefix}/#", qos=1)
    c.loop_start()
    yield c, received
    c.loop_stop()
    c.disconnect()


def wait_for(q, predicate, timeout=5.0):
    while True:
        topic, payload, retain = q.get(timeout=timeout)  # raises queue.Empty on timeout
        if predicate(topic, payload):
            return topic, payload, retain


def test_temperature_drives_heater(prefix, probe):
    pc, received = probe
    client, _, ready = build_client(HOST, PORT, f"sut-{uuid.uuid4().hex[:8]}", prefix)
    client.loop_start()
    try:
        assert ready.wait(5), "SUT did not subscribe in time"
        pc.publish(f"{prefix}/office/temperature", '{"value": 18.5}', qos=1)
        topic, payload, _ = wait_for(received, lambda t, p: t.endswith("/heater/set"))
        assert topic == f"{prefix}/office/heater/set"
        assert payload == "ON"
    finally:
        client.loop_stop()
        client.disconnect()


def test_heater_command_is_retained(prefix, probe):
    pc, received = probe
    client, _, ready = build_client(HOST, PORT, f"sut-{uuid.uuid4().hex[:8]}", prefix)
    client.loop_start()
    try:
        assert ready.wait(5), "SUT did not subscribe in time"
        pc.publish(f"{prefix}/hall/temperature", '{"value": 15}', qos=1)
        wait_for(received, lambda t, p: t.endswith("/heater/set"))
    finally:
        client.loop_stop()
        client.disconnect()

    # A late subscriber must get the retained command immediately
    late = queue.Queue()
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"late-{uuid.uuid4().hex[:8]}")
    c.on_message = lambda cl, ud, m: late.put((m.topic, m.payload.decode(), m.retain))
    c.connect(HOST, PORT)
    c.subscribe(f"{prefix}/hall/heater/set", qos=1)
    c.loop_start()
    try:
        _, payload, retain = late.get(timeout=5)
        assert payload == "ON" and retain is True
    finally:
        c.loop_stop()
        c.disconnect()
