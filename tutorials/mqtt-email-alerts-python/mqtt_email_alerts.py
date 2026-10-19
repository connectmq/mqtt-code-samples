import json
import os
import queue
import smtplib
import ssl
import threading
import time
import uuid
from email.message import EmailMessage

import paho.mqtt.client as mqtt

# --- MQTT settings ---
BROKER = os.environ.get("MQTT_HOST", "broker.connectmq.com")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME")
PASSWORD = os.environ.get("MQTT_PASSWORD")
CLIENT_ID = os.environ.get("MQTT_CLIENT_ID", f"mail-alerts-{uuid.uuid4().hex[:8]}")
PREFIX = os.environ.get("TOPIC_PREFIX", "connectmq/demo/mail-6630")

# --- SMTP settings ---
SMTP_HOST = os.environ["SMTP_HOST"]
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ["SMTP_USER"]
SMTP_PASS = os.environ["SMTP_PASS"]
MAIL_FROM = os.environ.get("MAIL_FROM", SMTP_USER)
MAIL_TO = [a.strip() for a in os.environ["MAIL_TO"].split(",")]
COOLDOWN = int(os.environ.get("COOLDOWN_MINUTES", "15")) * 60

# metric -> (trigger above, clear below)
THRESHOLDS = {
    "temperature": (80.0, 75.0),
    "pressure": (3.0, 2.7),
}

outbox: "queue.Queue[EmailMessage]" = queue.Queue()
active = {}      # (device, metric) -> True while in alarm
last_sent = {}   # key -> timestamp of last email


def build_email(subject: str, body: str) -> EmailMessage:
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = ", ".join(MAIL_TO)
    msg.set_content(body)
    return msg


def queue_email(key, subject, body, force=False):
    now = time.time()
    if not force and now - last_sent.get(key, 0) < COOLDOWN:
        print(f"Cooldown active for {key}, not emailing")
        return
    last_sent[key] = now
    outbox.put(build_email(subject, body))


def smtp_worker():
    context = ssl.create_default_context()
    while True:
        msg = outbox.get()
        for attempt in range(1, 4):
            try:
                if SMTP_PORT == 465:
                    server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=20)
                else:
                    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=20)
                    server.starttls(context=context)
                with server:
                    server.login(SMTP_USER, SMTP_PASS)
                    server.send_message(msg)
                print(f"Sent: {msg['Subject']}")
                break
            except (smtplib.SMTPException, OSError) as exc:
                print(f"SMTP attempt {attempt} failed: {exc}")
                time.sleep(10 * attempt)


def check_thresholds(device: str, data: dict):
    for metric, (trigger, clear) in THRESHOLDS.items():
        value = data.get(metric)
        if not isinstance(value, (int, float)):
            continue
        key = (device, metric)
        if not active.get(key) and value > trigger:
            active[key] = True
            queue_email(key, f"[ALERT] {device} {metric} = {value}",
                        f"{device} reported {metric} = {value}, above the limit of {trigger}.\n"
                        f"Topic: {PREFIX}/{device}/telemetry\nTime: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        elif active.get(key) and value < clear:
            active[key] = False
            # always send the resolution, even inside the cooldown window
            queue_email(key, f"[RESOLVED] {device} {metric} = {value}",
                        f"{device} {metric} is back below {clear} (now {value}).", force=True)


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT connect failed: {reason_code}")
        return
    client.subscribe(f"{PREFIX}/+/telemetry", qos=0)
    client.subscribe(f"{PREFIX}/+/alarm", qos=1)
    print("Subscribed to telemetry and alarm topics")


def on_message(client, userdata, msg):
    device, kind = msg.topic.split("/")[-2:]
    try:
        data = json.loads(msg.payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print(f"Ignoring non-JSON payload on {msg.topic}")
        return
    if not isinstance(data, dict):
        return
    if kind == "telemetry":
        check_thresholds(device, data)
    elif kind == "alarm" and not msg.retain:
        severity = str(data.get("severity", "alarm")).upper()
        queue_email((device, "alarm"), f"[{severity}] {device}: {data.get('text', 'alarm')}",
                    json.dumps(data, indent=2))


def main():
    threading.Thread(target=smtp_worker, daemon=True).start()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    if PORT == 8883:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.reconnect_delay_set(min_delay=1, max_delay=60)
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_forever(retry_first_connection=True)


if __name__ == "__main__":
    main()
