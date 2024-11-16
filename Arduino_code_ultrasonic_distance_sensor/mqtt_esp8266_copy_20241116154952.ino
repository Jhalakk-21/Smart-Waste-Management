#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// WiFi credentials
const char* ssid = "Galaxy A125B9A";
const char* password = "csqe9142";
const char* mqtt_server = "5.196.78.28";

// MQTT client setup
WiFiClient espClient;

PubSubClient client(espClient);

// Ultrasonic sensor pins
#define trigPin1 D4 // First sensor trig pin
#define echoPin1 D2 // First sensor echo pin
#define trigPin2 D7 // Second sensor trig pin
#define echoPin2 D8 // Second sensor echo pin

// Variables for distance measurement
long duration1, duration2;
float distance1, distance2;

unsigned long lastMsg = 0;

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
      // Publish an initial message
      client.publish("jhalak_iot", "Connected to MQTT server");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);

  // Set pin modes for ultrasonic sensors
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
}

float readDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH, 20000); // Timeout of 20ms
  if (duration == 0) {
    return -1; // Indicating no valid reading
  }
  return duration * 0.034 / 2; // Calculate distance in cm
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;

    // Read distance from the first sensor
    distance1 = readDistance(trigPin1, echoPin1);
    if (distance1 == -1) {
      Serial.println("Sensor 1: No echo detected");
    } else {
      Serial.print("Sensor 1 Distance in CM: ");
      Serial.println(distance1);
    }

    // Read distance from the second sensor
    distance2 = readDistance(trigPin2, echoPin2);
    if (distance2 == -1) {
      Serial.println("Sensor 2: No echo detected");
    } else {
      Serial.print("Sensor 2 Distance in CM: ");
      Serial.println(distance2);
    }

    // Create payload to send both distances
    char payload[100];
    snprintf(payload, sizeof(payload), "{\"distance1\":%.2f,\"distance2\":%.2f}", distance1, distance2);

    // Publish data to the MQTT topic
    client.publish("jhalak_iot/distance", payload);
    Serial.print("Published payload: ");
    Serial.println(payload);
  }

  delay(5000); // Delay of 5 seconds between readings
}