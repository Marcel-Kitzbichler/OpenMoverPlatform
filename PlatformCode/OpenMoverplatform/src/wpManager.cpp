#include <ArduinoJson.h>
#include <Arduino.h>
#include "wpManager.h"
#include <TinyGPSPlus.h>
#include "config.h"

extern bool motorHandled;
extern TinyGPSPlus gps;

void wpManagerExec(void * pvParameters){
    motorHandled = true;
    double* coordinateTable = (double*)pvParameters;
    motorHandled = false;
    vTaskDelete(NULL);
    return;
}