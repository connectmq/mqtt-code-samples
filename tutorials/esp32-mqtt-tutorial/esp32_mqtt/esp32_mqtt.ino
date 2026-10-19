#include <WiFi.h>
#include <PubSubClient.h>

// ---- Wi-Fi ----
const char* WIFI_SSID     = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";

// ---- MQTT ----
const char* MQTT_HOST = "broker.connectmq.com";
const uint16_t MQTT_PORT = 1883;

const int LED_PIN = 2;                 // onboard LED on most ESP32 DevKits
const unsigned long PUBLISH_INTERVAL_MS = 5000;

WiFiClient netClient;
PubSubClient mqtt(netClient);

String deviceId;
String topicTelemetry, topicLedSet, topicLedState;
unsigned long lastPublish = 0;
unsigned long lastReconnectAttempt = 0;
bool ledOn = false;

void connectWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nWi-Fi connected, IP: ");
  Serial.println(WiFi.localIP());
}

String makeDeviceId() {
  uint8_t mac[6];
  WiFi.macAddress(mac);
  char buf[20];
  snprintf(buf, sizeof(buf), "esp32-%02x%02x%02x%02x%02x%02x",
           mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  return String(buf);
}

void publishLedState() {
  mqtt.publish(topicLedState.c_str(), ledOn ? "ON" : "OFF", true);  // retained
}

void onMessage(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned int i = 0; i < length; i++) msg += (char)payload[i];
  msg.trim();
  Serial.printf("Message on %s: %s\n", topic, msg.c_str());

  if (String(topic) != topicLedSet) return;
  if (msg.equalsIgnoreCase("ON"))          ledOn = true;
  else if (msg.equalsIgnoreCase("OFF"))    ledOn = false;
  else if (msg.equalsIgnoreCase("TOGGLE")) ledOn = !ledOn;
  else return;                             // ignore anything else

  digitalWrite(LED_PIN, ledOn ? HIGH : LOW);
  publishLedState();
}

bool connectMqtt() {
  Serial.printf("Connecting to MQTT as %s ... ", deviceId.c_str());
  if (mqtt.connect(deviceId.c_str())) {     // no username/password: public area
    Serial.println("connected");
    mqtt.subscribe(topicLedSet.c_str(), 1);
    publishLedState();
    return true;
  }
  Serial.printf("failed, state=%d\n", mqtt.state());
  return false;
}

float readTemperature() {
  // Simulated sensor: 22-25 °C with a little noise
  return 23.5 + 1.5 * sin(millis() / 60000.0) + random(-20, 20) / 100.0;
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  connectWiFi();
  deviceId = makeDeviceId();
  String base = "connectmq/demo/" + deviceId;
  topicTelemetry = base + "/telemetry";
  topicLedSet    = base + "/led/set";
  topicLedState  = base + "/led/state";
  Serial.println("Topic prefix: " + base);

  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setCallback(onMessage);
  mqtt.setBufferSize(512);   // default is 256 bytes, see below
  mqtt.setKeepAlive(30);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
  }

  if (!mqtt.connected()) {
    unsigned long now = millis();
    if (now - lastReconnectAttempt > 5000) {   // non-blocking retry every 5 s
      lastReconnectAttempt = now;
      if (connectMqtt()) lastReconnectAttempt = 0;
    }
    return;
  }

  mqtt.loop();   // process incoming messages and keepalive

  if (millis() - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = millis();
    char json[96];
    snprintf(json, sizeof(json), "{\"temperature\":%.2f,\"uptime\":%lu}",
             readTemperature(), millis() / 1000);
    mqtt.publish(topicTelemetry.c_str(), json);
    Serial.printf("Published %s\n", json);
  }
}
