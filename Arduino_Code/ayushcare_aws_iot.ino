#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include "MAX30105.h"

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";

const char* mqtt_server =
"YOUR_AWS_IOT_ENDPOINT";

WiFiClientSecure net;

PubSubClient client(net);

MAX30105 particleSensor;

void setup() {

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  client.setServer(mqtt_server, 8883);

  particleSensor.begin();
}

void loop() {

  long irValue = particleSensor.getIR();

  int heartRate = random(70, 90);
  int spo2 = random(95, 100);
  float temp = random(36, 38);

  String payload = "{";
  payload += "\"patient_id\":\"P001\",";
  payload += "\"heart_rate\":" + String(heartRate) + ",";
  payload += "\"spo2\":" + String(spo2) + ",";
  payload += "\"temperature\":" + String(temp);
  payload += "}";

  client.publish(
      "ayushcare/vitals",
      payload.c_str()
  );

  delay(5000);
}
