#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <FirebaseArduino.h>
#include <OneWire.h>
#include <DallasTemperature.h>


//Setting up firebase and wifi connection
#define FIREBASE_HOST "farmcycle-9ccea-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "SiJ9Ii6VUGOQfTgrOatT3jtUHdRHwX0KmdEw7tQK"
#define WIFI_SSID "jambo hatdog"
#define WIFI_PASSWORD "asdfghjkl1234567890"

//Setting up ultrasonic sensor
const int echoPin = 5; //Green jumper D1
const int trigPin = 4; //Yellow jumper D2

//Setting up DS18B20
const int oneWireBus = 0; //D3     

// defines ultrasonic sensor variables
long duration;
int distance;

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);

// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

//Setting up ultrasonic sensor
void setup() {
  Serial.begin(115200);

  // connect to wifi.
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  sensors.begin();
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
}

void loop() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  Serial.print("Distance: ");
  Serial.println(distance);
  delay(2000);

//change ChickenQuantity to WaterLevel
  Firebase.setFloat("FarmCycle/WaterLevel/waterlvl", distance);
  if (Firebase.failed()) {
      Serial.print("setting /number failed:");
      Serial.println(Firebase.error());  
      return;
  }
  delay(1000);
  Serial.print("Quantity: ");
  Serial.println(Firebase.getFloat("FarmCycle/WaterLevel/waterlvl"));
  delay(1000);

  sensors.requestTemperatures(); 
  float temperatureC = sensors.getTempCByIndex(0);
  float temperatureF = sensors.getTempFByIndex(0);
  Serial.print(temperatureC);
  Serial.println("ºC");
  Serial.print(temperatureF);
  Serial.println("ºF");
  delay(3000);

  Firebase.setFloat("FarmCycle/tTankTemp/Temp", temperatureC);
  if (Firebase.failed()) {
      Serial.print("setting /number failed:");
      Serial.println(Firebase.error());  
      return;
  }
  delay(1000);
  Serial.print("Temp: ");
  Serial.println(Firebase.getFloat("FarmCycle/tTankTemp/Temp"));
  delay(1000);
}

