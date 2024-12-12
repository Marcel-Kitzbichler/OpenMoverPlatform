#include <ArduinoJson.h>
#include <Arduino.h>


void wpManagerExec(void * pvParameters){
    int* coordinateTableWP = (int*)pvParameters;
    Serial.println("wpManagerExec");
    Serial.println(*coordinateTableWP);
    Serial.println(*(coordinateTableWP+1));
    vTaskDelete(NULL);
    return;
}