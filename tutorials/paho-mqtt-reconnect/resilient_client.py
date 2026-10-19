import json
import logging
import random
import threading
import time
import uuid
from collections import deque

import paho.mqtt.client as mqtt
from paho.mqtt.packettypes import PacketTypes
from paho.mqtt.properties import Properties

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("mqtt")


class ResilientClient:
    def __init__(self, host, port, client_id, subscriptions,
                 username=None, password=None, use_tls=False,
                 session_expiry_s=1800, buffer_size=1000):
        self.host = host
        self.port = port
        self.subscriptions = subscriptions  # list of (topic, qos)
        self.session_expiry_s = session_expiry_s
        self.offline = deque(maxlen=buffer_size)  # oldest dropped when full
        self.lock = threading.Lock()
        self.on_payload = None

        c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                        client_id=client_id, protocol=mqtt.MQTTv5)
        if username:
            c.username_pw_set(username, password)
        if use_tls:
            c.tls_set()
        # Exponential backoff; a random floor spreads out reconnecting fleets
        c.reconnect_delay_set(min_delay=random.randint(1, 5), max_delay=60)
        c.on_connect = self._on_connect
        c.on_disconnect = self._on_disconnect
        c.on_connect_fail = self._on_connect_fail
        c.on_message = self._on_message
        self.client = c

    def start(self):
        props = Properties(PacketTypes.CONNECT)
        props.SessionExpiryInterval = self.session_expiry_s
        self.client.connect_async(self.host, self.port, keepalive=30,
                                  clean_start=False, properties=props)
        self.client.loop_start()

    def stop(self):
        self.client.disconnect()
        self.client.loop_stop()

    # --- callbacks -------------------------------------------------------
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            log.warning("connect refused: %s", reason_code)
            return
        log.info("connected, session_present=%s", flags.session_present)
        if self.subscriptions:
            client.subscribe(self.subscriptions)  # always resubscribe
        self._flush()

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            log.info("clean disconnect")
        else:
            log.warning("connection lost: %s, reconnecting", reason_code)

    def _on_connect_fail(self, client, userdata):
        log.warning("connection attempt failed, retrying with backoff")

    def _on_message(self, client, userdata, msg):
        if self.on_payload:
            self.on_payload(msg.topic, msg.payload)

    # --- publishing ------------------------------------------------------
    def publish(self, topic, payload, qos=1, retain=False):
        if self.client.is_connected():
            info = self.client.publish(topic, payload, qos=qos, retain=retain)
            if info.rc == mqtt.MQTT_ERR_SUCCESS:
                return True
        with self.lock:
            self.offline.append((topic, payload, qos, retain))
        return False

    def _flush(self):
        with self.lock:
            pending = list(self.offline)
            self.offline.clear()
        if pending:
            log.info("flushing %d buffered messages", len(pending))
        for topic, payload, qos, retain in pending:
            self.client.publish(topic, payload, qos=qos, retain=retain)


if __name__ == "__main__":
    run_id = uuid.uuid4().hex[:8]
    prefix = f"connectmq/demo/{run_id}"
    rc = ResilientClient(
        host="broker.connectmq.com", port=1883,
        client_id=f"resilient-{run_id}",
        subscriptions=[(f"{prefix}/cmd/#", 1)],
    )
    rc.on_payload = lambda t, p: log.info("command on %s: %s", t, p)
    rc.start()
    print(f"publishing to {prefix}/telemetry, send commands to {prefix}/cmd/...")
    try:
        n = 0
        while True:
            n += 1
            payload = json.dumps({"seq": n, "ts": int(time.time() * 1000)})
            sent = rc.publish(f"{prefix}/telemetry", payload, qos=1)
            log.info("seq %d %s (buffered: %d)", n, "sent" if sent else "buffered", len(rc.offline))
            time.sleep(2)
    except KeyboardInterrupt:
        rc.stop()
