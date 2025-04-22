#include <ArduinoJson.h>
#include <Arduino.h>
#include "wpManager.h"
#include <TinyGPSPlus.h>
#include "config.h"

extern bool motorHandled;

void wpManagerExec(void * pvParameters){
    motorHandled = true;
    int* coordinateTable = (int*)pvParameters;
    TinyGPSPlus gps;
    Serial2.begin(GPSBaud);
    /*
    while(!gps.location.isValid()){
        while (Serial2.available() > 0)
        {
            gps.encode(Serial2.read());
            Serial.println("Waiting for GPS");
        }
    }
    float lastLat = gps.location.lat();
    float lastLon = gps.location.lng();
    unsigned long lastUpdate = millis();
    while (true)
    {
        while (Serial2.available() > 0)
        {
            gps.encode(Serial2.read());
        }
        if (gps.location.isValid() && gps.location.isUpdated())
        {
            lastLat = gps.location.lat();
            lastLon = gps.location.lng();
            lastUpdate = millis();
            Serial.println(lastLat,10);
            Serial.println(lastLon,10);
        }
        if(lastUpdate + GPSTineout < millis()){
            break;
        }
    }
    */
    Serial2.end();
    motorHandled = false;
    vTaskDelete(NULL);
    return;
}