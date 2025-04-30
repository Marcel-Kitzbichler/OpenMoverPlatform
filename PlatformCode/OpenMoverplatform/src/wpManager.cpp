#include <ArduinoJson.h>
#include <Arduino.h>
#include "wpManager.h"
#include <TinyGPSPlus.h>
#include "config.h"
#include "endMotorTask.h"

extern bool motorHandled;
extern TinyGPSPlus gps;

void wpManagerExec(void * pvParameters){
    motorHandled = true;

    // Assuming pvParameters is a pointer to an array of doubles and the size is known
    const int coordinateCount = 100; // Replace with the actual size of the array
    double* inputCoordinates = (double*)pvParameters;
    double* coordinateTable = new double[coordinateCount];

    // Copy data from pvParameters to coordinateTable
    for (int i = 0; i < coordinateCount; i++) {
        coordinateTable[i] = inputCoordinates[i];
    }
    
    // Perform operations with coordinateTable here
    endMotorTask(); // Call the function to end the motor task
}