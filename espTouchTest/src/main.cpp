/*
    Based on Neil Kolban example for IDF: 
    https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleServer.cpp
    Ported to Arduino ESP32 by Evandro Copercini
    updates by chegewara
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <Arduino.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLECharacteristic *pCharacteristic;
int i=0;
char buffer[10];

#define N 2
int Tpins [N] = { T8, T9};

bool deviceConnected = false;

// callback when connected and disconnected
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
      deviceConnected = true;
      Serial.println("Connected");
    };

    void onDisconnect(BLEServer* pServer) {
      deviceConnected = false;
      Serial.println("Disconnected");
    }
};

void setup() {
  Serial.begin(250000);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(T8, OUTPUT);
  Serial.println("Starting BLE work!");

  BLEDevice::init("ESP32_ble_server");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(
                                         CHARACTERISTIC_UUID,
                                         BLECharacteristic::PROPERTY_READ |
                                         BLECharacteristic::PROPERTY_WRITE|
                                          BLECharacteristic::PROPERTY_NOTIFY
                                       );

  pCharacteristic->setValue("Hello World says Neil");
  pService->start();
  // BLEAdvertising *pAdvertising = pServer->getAdvertising();  
  // this still is working for backward compatibility
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);
  BLEDevice::startAdvertising();
  Serial.println("Characteristic defined! Now you can read it in your phone!");
}

void loop() {
  // put your main code here, to run repeatedly:
  sprintf(buffer, "%d", touchRead(T8));
  pCharacteristic->setValue(buffer);
  pCharacteristic->notify();
  i++;
  Serial.println(i);
  digitalWrite(LED_BUILTIN, (i%2)==0);
  // handle deconnections
  if (!deviceConnected) {
    // advertising
    BLEDevice::startAdvertising();
    Serial.println("start advertising");
  }
  delay(20);
}