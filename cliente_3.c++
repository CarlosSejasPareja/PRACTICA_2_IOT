#include "LiquidCrystal_I2C.h"
#include <WiFi.h>
#include <ArduinoJson.h>

const char* WIFI_SSID = "pruebaIOT";
const char* WIFI_PASS = "contra123";
const char* SERVER_ADDRESS = "192.168.123.247";
const int SERVER_PORT = 1000;
const int BUTTON_PIN = 32;
const int BUZZER_PIN = 25; 

int distanceOk = 30;
int currentDistance = distanceOk;
int interval = 5;

DynamicJsonDocument doc(256);

void sendData(int currentDistance, WiFiClient &client) {
  doc["TEST"] = 1;
  doc["distance"] = currentDistance;
  String jsonString;
  serializeJson(doc, jsonString);
  client.print(jsonString);
}

LiquidCrystal_I2C lcd(0x27, 16, 2);

void soundBuzzer(int replay) {
  for(int i = 0; i < replay; i += 1){
    digitalWrite(BUZZER_PIN, HIGH); // Enciende el buzzer
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  }
}

bool checkInterval() {
  return currentDistance > interval;
}

void updateDistance(WiFiClient &client) {
  if (checkInterval()) {
    currentDistance -= interval;
  } else {
    currentDistance = distanceOk;
    soundBuzzer(1);
    client.stop();
  }
}

void updateMessageLCD() {
  lcd.clear();
  lcd.print("Distance:" + String(currentDistance));
  lcd.setCursor(0, 1);
  if (checkInterval()) {
    lcd.print("Next:" + String(currentDistance - interval));
  } else {
    lcd.print("Next:" + String(distanceOk));
  }
}

void setup() {
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
  lcd.init();
  lcd.backlight();
  lcd.print("Press the button");
  lcd.setCursor(0, 1);
  lcd.print("D:" + String(distanceOk) + "-" + String(interval) + " " + "Inter:" + String(interval));
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT); 
}

void loop() {
  delay(100); 
  WiFiClient client;
  if (!client.connect(SERVER_ADDRESS, SERVER_PORT)) {
    Serial.println("Connection failed");
    return;
  }
  if (digitalRead(BUTTON_PIN) == LOW) {
    soundBuzzer(2);
    sendData(currentDistance, client);
    updateMessageLCD();
    updateDistance(client);
  }  
}