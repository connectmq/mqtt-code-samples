#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>

const char* WIFI_SSID = "YOUR_WIFI";
const char* WIFI_PASS = "YOUR_WIFI_PASSWORD";
const char* TOPIC = "your-project/sensors/temperature";

// Root CA certificate (PEM) of the broker TLS certificate
const char* ROOT_CA = R"PEM(
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
)PEM";

WiFiClientSecure net;
PubSubClient mqtt(net);

// Runs for every message on a subscribed topic
void onMessage(char* topic, byte* payload, unsigned int length) {
  Serial.printf("%s: %.*s\n", topic, length, (char*)payload);
}

void connectMqtt() {
  while (!mqtt.connected()) {
    // Every client needs a unique client ID
    String id = "esp32-" + String((uint32_t)ESP.getEfuseMac(), HEX);
    // Username and password from your ConnectMQ dashboard
    if (mqtt.connect(id.c_str(), "YOUR_USERNAME", "YOUR_PASSWORD")) {
      // Subscribe to the temperature topic
      mqtt.subscribe(TOPIC);
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  // Connect to Wi-Fi first
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  net.setCACert(ROOT_CA);
  // Connect to your private ConnectMQ broker on port 8883
  mqtt.setServer("YOUR_BROKER_HOST", 8883);
  mqtt.setCallback(onMessage);
}

void loop() {
  // Reconnect automatically if the connection drops
  if (!mqtt.connected()) connectMqtt();
  mqtt.loop();
  static unsigned long last = 0;
  if (millis() - last > 10000) {
    last = millis();
    // Publish a JSON reading
    mqtt.publish(TOPIC, "{\"temperature\":21.5}");
  }
}
