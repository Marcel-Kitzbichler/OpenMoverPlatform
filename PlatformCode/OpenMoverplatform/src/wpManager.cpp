#include <ArduinoJson.h>
#include <Arduino.h>


void wpManagerExec(void * pvParameters){
    int* coordinateTable = (int*)pvParameters;
    Serial.println("wpManagerExec");
    Serial.println(*coordinateTable);
    Serial.println(*(coordinateTable+1));
    vTaskDelete(NULL);
    return;
}