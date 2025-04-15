#include <ArduinoJson.h>
#include <Arduino.h>
#include "wpManager.h"
#include <TinyGPSPlus.h>
#include "config.h"

extern bool motorHandled;
const double uSecPWM = ((1000000/pwmFreq)/pow(2,pwmResolution));

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
    for(int i = 30; i <= 200; i = i + 1){
        ledcWrite(pwmChMotor1, (pwmCenter+i) / uSecPWM);
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }
    vTaskDelay(4000 / portTICK_PERIOD_MS);
    for (int i = 200; i >= 0; i--)
    {
        ledcWrite(pwmChMotor1, (pwmCenter+i) / uSecPWM);
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }

    for(int i = 30; i <= 200; i = i + 1){
        ledcWrite(pwmChMotor1, (pwmCenter-i) / uSecPWM);
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }
    vTaskDelay(4000 / portTICK_PERIOD_MS);
    for (int i = 200; i >= 0; i--)
    {
        ledcWrite(pwmChMotor1, (pwmCenter-i) / uSecPWM);
        vTaskDelay(50 / portTICK_PERIOD_MS);
    }
    
    ledcWrite(pwmChMotor1, (pwmCenter) / uSecPWM);
    Serial2.end();
    motorHandled = false;
    vTaskDelete(NULL);
    return;
}