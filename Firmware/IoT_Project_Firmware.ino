#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

const char* ssid = "Huawei mate 20 pro";        // must be 2.4GHz
const char* password = "huaweinet";
const char* serverURL = "http://192.168.43.171:5000/api/add_data";

#define DHTPIN 4
#define DHTTYPE DHT22
#define TRIG_PIN 5
#define ECHO_PIN 18
#define MQ135_PIN 34
#define ACS712_PIN 15

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  dht.begin();

  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected!");
  Serial.print("ESP32 IP: "); Serial.println(WiFi.localIP());
}

void loop() {
  // ---------- Ultrasonic ----------
  digitalWrite(TRIG_PIN, LOW); delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH); delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  long duration = pulseIn(ECHO_PIN, HIGH, 30000);
  float distance = (duration > 0) ? duration * 0.034 / 2 : -1;

  // ---------- DHT22 ----------
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  // ---------- MQ135 ----------
  int mq135 = analogRead(MQ135_PIN);

  // ---------- ACS712 ----------
  int acs_raw = analogRead(ACS712_PIN);
  float voltage = (acs_raw / 4095.0) * 3.3;
  float current_mA = (voltage - 1.65) / (0.066 * 3.3 / 5) * 1000; // approximate

  // ---------- Print ----------
  Serial.println("📊 SENSOR DATA");
  Serial.println(distance);
  Serial.println(temperature);
  Serial.println(humidity);
  Serial.println(mq135);
  Serial.println(current_mA);

  // ---------- POST to Flask ----------
  if(WiFi.status() == WL_CONNECTED){
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<256> doc;
    doc["ultrasonic"] = distance;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["mq135"] = mq135;
    doc["current_mA"] = current_mA;

    String payload;
    serializeJson(doc, payload);

    Serial.println("📤 Sending JSON: " + payload);
    int httpResponseCode = http.POST(payload);
    Serial.print("🌐 HTTP Response: "); Serial.println(httpResponseCode);

    http.end();
  } else {
    Serial.println("❌ WiFi not connected");
  }

  delay(5000);
}
