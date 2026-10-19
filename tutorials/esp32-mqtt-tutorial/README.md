# ESP32 MQTT Tutorial: Publish Sensor Data and Control an LED with Arduino IDE

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Connect an ESP32 to an MQTT broker with Arduino IDE and PubSubClient, publish JSON temperature readings, control the onboard LED from the command line and upgrade to TLS with portal credentials.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-intro)

📖 **Full step-by-step tutorial:** [ESP32 MQTT Tutorial: Publish Sensor Data and Control an LED with Arduino IDE](https://connectmq.com/blog/esp32-mqtt-tutorial/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`esp32_mqtt/esp32_mqtt.ino`](esp32_mqtt/esp32_mqtt.ino) | Arduino sketch: Wi-Fi + MQTT with non-blocking reconnect, JSON telemetry every 5 s, LED control via `led/set` and a retained `led/state`. |

## Requirements

- An ESP32 development board (most DevKits have an LED on GPIO 2)
- Arduino IDE 2.x with the **esp32** board package
- The **PubSubClient** library by Nick O'Leary (Library Manager)
- A 2.4 GHz Wi-Fi network
- Optional: Mosquitto command-line clients (`mosquitto_sub`, `mosquitto_pub`)
- Optional: a DHT22 sensor and the Adafruit "DHT sensor library" (the sketch simulates temperature by default)

## Run it on the free public broker

1. Open `esp32_mqtt/esp32_mqtt.ino` in Arduino IDE and set `WIFI_SSID` and `WIFI_PASSWORD`.
2. Select your board and port, upload, and open the Serial Monitor at 115200 baud. Copy the device ID from the printed topic prefix.
3. Watch everything under your device's prefix (replace `esp32-a1b2c3d4e5f6` with your ID):

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i laptop-watch-81f3 \
     -t "connectmq/demo/esp32-a1b2c3d4e5f6/#" -v
   ```

4. Switch the LED from a second terminal:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i laptop-cmd-81f3 \
     -t "connectmq/demo/esp32-a1b2c3d4e5f6/led/set" -q 1 -m "TOGGLE"
   ```

Optional real sensor: wire a DHT22 data pin to GPIO 4 and replace `readTemperature()`:

```cpp
#include <DHT.h>
DHT dht(4, DHT22);   // call dht.begin() in setup()

float readTemperature() {
  float t = dht.readTemperature();
  return isnan(t) ? -127.0 : t;   // send a sentinel instead of NaN
}
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `esp32_mqtt.ino`, switch to `WiFiClientSecure` on port 8883 with credentials and the ISRG Root X1 certificate (download `isrgrootx1.pem` from Let's Encrypt). The post's changes:

   ```cpp
   #include <WiFi.h>
   #include <WiFiClientSecure.h>
   #include <PubSubClient.h>
   #include <time.h>

   const char* MQTT_HOST = "broker.connectmq.com";
   const uint16_t MQTT_PORT = 8883;
   const char* MQTT_USER = "YOUR_USERNAME";
   const char* MQTT_PASS = "YOUR_PASSWORD";
   const char* MQTT_CLIENT_ID = "YOUR_CLIENT_ID_esp32a";

   // ISRG Root X1 (paste the full PEM from isrgrootx1.pem)
   static const char ROOT_CA[] PROGMEM = R"EOF(
   -----BEGIN CERTIFICATE-----
   ...paste the certificate body here...
   -----END CERTIFICATE-----
   )EOF";

   WiFiClientSecure netClient;
   PubSubClient mqtt(netClient);

   void syncClock() {
     configTime(0, 0, "pool.ntp.org", "time.nist.gov");
     time_t now = time(nullptr);
     while (now < 1700000000) { delay(250); now = time(nullptr); }
   }

   // in setup(), after connectWiFi():
   //   syncClock();
   //   netClient.setCACert(ROOT_CA);
   //   mqtt.setServer(MQTT_HOST, MQTT_PORT);
   //   topic base: "plant1/" + String(MQTT_CLIENT_ID) instead of "connectmq/demo/..."

   bool connectMqtt() {
     if (mqtt.connect(MQTT_CLIENT_ID, MQTT_USER, MQTT_PASS)) {
       mqtt.subscribe(topicLedSet.c_str(), 1);
       publishLedState();
       return true;
     }
     return false;
   }
   ```

   Give each device its own `_suffix` of the issued client ID, and keep credentials in a `secrets.h` that is not committed. Verify with your own credentials:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 8883 --cafile isrgrootx1.pem \
     -u YOUR_USERNAME -P YOUR_PASSWORD -i YOUR_CLIENT_ID_laptop \
     -t "plant1/#" -v
   mosquitto_pub -h broker.connectmq.com -p 8883 --cafile isrgrootx1.pem \
     -u YOUR_USERNAME -P YOUR_PASSWORD -i YOUR_CLIENT_ID_cli \
     -t "plant1/YOUR_CLIENT_ID_esp32a/led/set" -q 1 -m "ON"
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [ESP32 MQTT Tutorial: Publish Sensor Data and Control an LED with Arduino IDE](https://connectmq.com/blog/esp32-mqtt-tutorial/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-related) — the full tutorial with explanations
- 🧩 [ESP32 basic example](../../esp32/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-esp32-mqtt-tutorial-footer">Blog</a>
</p>
