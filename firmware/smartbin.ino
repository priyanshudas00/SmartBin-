/*
 * SmartBin - IoT Smart Waste Management System
 * Firmware for ESP8266
 * 
 * This code reads ultrasonic sensor data and sends it to a backend server
 */

#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

// WiFi Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server Configuration
const char* serverUrl = "http://your-server-ip:5000/api/data";

// Sensor Pins
const int trigPin = D1;  // GPIO5
const int echoPin = D2;  // GPIO4

// Bin Configuration
const int BIN_HEIGHT = 100;  // Total bin height in cm
const int UPDATE_INTERVAL = 60000;  // Update interval in milliseconds (60 seconds)

// Device ID (unique identifier for this bin)
const char* deviceId = "BIN001";

void setup() {
  Serial.begin(115200);
  delay(10);
  
  // Initialize sensor pins
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  // Connect to WiFi
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Read sensor data
  float distance = getDistance();
  
  if (distance > 0 && distance < 400) {  // Valid range for HC-SR04
    // Calculate fill percentage
    float fillLevel = calculateFillLevel(distance);
    
    // Display on Serial Monitor
    Serial.print("Distance: ");
    Serial.print(distance);
    Serial.print(" cm | Fill Level: ");
    Serial.print(fillLevel);
    Serial.println("%");
    
    // Send data to server
    if (WiFi.status() == WL_CONNECTED) {
      sendDataToServer(distance, fillLevel);
    } else {
      Serial.println("WiFi disconnected. Reconnecting...");
      WiFi.reconnect();
    }
  } else {
    Serial.println("Invalid sensor reading");
  }
  
  // Wait before next reading
  delay(UPDATE_INTERVAL);
}

// Function to get distance from ultrasonic sensor
float getDistance() {
  // Clear the trigger pin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  // Send 10 microsecond pulse to trigger
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Read the echo pin
  long duration = pulseIn(echoPin, HIGH, 30000);  // Timeout after 30ms
  
  // Calculate distance in cm
  float distance = duration * 0.034 / 2;
  
  return distance;
}

// Function to calculate fill level percentage
float calculateFillLevel(float distance) {
  if (distance >= BIN_HEIGHT) {
    return 0.0;  // Empty
  }
  
  float fillLevel = ((BIN_HEIGHT - distance) / BIN_HEIGHT) * 100.0;
  
  // Ensure fill level is between 0 and 100
  if (fillLevel < 0) fillLevel = 0;
  if (fillLevel > 100) fillLevel = 100;
  
  return fillLevel;
}

// Function to send data to server
void sendDataToServer(float distance, float fillLevel) {
  HTTPClient http;
  WiFiClient client;
  
  http.begin(client, serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  // Create JSON payload
  String jsonPayload = "{";
  jsonPayload += "\"device_id\":\"" + String(deviceId) + "\",";
  jsonPayload += "\"distance\":" + String(distance) + ",";
  jsonPayload += "\"fill_level\":" + String(fillLevel) + ",";
  jsonPayload += "\"timestamp\":" + String(millis());
  jsonPayload += "}";
  
  Serial.print("Sending data: ");
  Serial.println(jsonPayload);
  
  int httpResponseCode = http.POST(jsonPayload);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    Serial.print("Response: ");
    Serial.println(response);
  } else {
    Serial.print("Error sending data. HTTP Response code: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}
