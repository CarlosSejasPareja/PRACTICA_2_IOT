#include <WiFi.h>
#include <ArduinoJson.h>
const char* WIFI_SSID = "pruebaIOT";
const char* WIFI_PASS = "contra123";
const char* SERVER_ADDRESS = "192.168.123.247";
const int SERVER_PORT = 1000;
const int LEDPINS[] = {12, 27, 26, 25, 33, 32};

void setup() {
  for (int i = 0; i < sizeof(LEDPINS) / sizeof(LEDPINS[0]); i++) {
    pinMode(LEDPINS[i], OUTPUT);
  }
  Serial.begin(115200);
  Serial.print("Connecting to: ");
  Serial.println(WIFI_SSID);
  delay(1000);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.print("\nIP address: ");
  Serial.println(WiFi.localIP());
}
void loop() {
  delay(100);
  WiFiClient client;
  if (!client.connect(SERVER_ADDRESS, SERVER_PORT)) {
    Serial.println("Connection failed");
    return;
  } else {
    static int ReadyToPair = 0;
    if (ReadyToPair == 0) {
      Serial.println("The device is ready to pair");
      ReadyToPair = 1;
    }
  }
  DynamicJsonDocument doc(256);
  doc["GET"] = 1;
  String Json_String;
  serializeJson(doc, Json_String);
  client.print(Json_String);
  String SERVER_RESPONSE = client.readStringUntil('\n');
  Serial.println("Respuesta del servidor: " + SERVER_RESPONSE);
  if (SERVER_RESPONSE.length() == 6) {
    for (int i = 0; i < sizeof(LEDPINS) / sizeof(LEDPINS[0]); i++) {
      digitalWrite(LEDPINS[i], SERVER_RESPONSE[i] == '1' ? HIGH : LOW);
    }
  }
}
