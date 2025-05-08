#include <ArduinoJson.h>
#include <Arduino.h>
#include "wpManager.h"
#include <TinyGPSPlus.h>
#include "config.h"
#include "endMotorTask.h"
#include "goTo.h"

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

    //coordinate table will look like this: [coordinateAmount, speed, range, lon1, lat1, lon2, lat2, ...] this code will go through the array and got to them one by one
    // The first three elements are coordinateAmount, speed, and range
    // The rest are the coordinates in pairs (lon, lat)
    int coordinateAmount = (int)coordinateTable[0];
    double speed = coordinateTable[1];
    double range = coordinateTable[2];
    double lon, lat;
    if(coordinateAmount > 1 && coordinateAmount < 50){	
        for (int i = 0; i < coordinateAmount; i++) {
            lon = coordinateTable[3 + i * 2];
            lat = coordinateTable[4 + i * 2];
            // Call the goTo function with the coordinates and other parameters
            goTo(lat, lon, speed, range);
        }
    }
    // Perform operations with coordinateTable here
    endMotorTask(); // Call the function to end the motor task
}