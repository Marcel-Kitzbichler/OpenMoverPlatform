#include <ArduinoJson.h>
#include <Arduino.h>
#include "wpManager.h"

extern bool motorHandled;

void wpManagerExec(void * pvParameters){
    motorHandled = true;
    int* coordinateTable = (int*)pvParameters;
    Serial.println("wpManagerExec");
    Serial.println(*coordinateTable);
    Serial.println(*(coordinateTable+1));
    vTaskDelay(10000/portTICK_PERIOD_MS);
    Serial.println("wpManagerExec done");
    motorHandled = false;
    vTaskDelete(NULL);
    return;
}