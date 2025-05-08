#include <arduino.h>
#include "config.h"
#include "compass.h"
#include "endMotorTask.h"
#include "motorSet.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(0);

extern bool motorHandled;

double MagXMax = 0;
double MagXMin = 0;
double MagYMax = 0;
double MagYMin = 0;

float getHeading(){
sensors_event_t event; 
    mag.getEvent(&event);
    
    float heading = atan2(-(event.magnetic.x - (MagXMin + ((MagXMax - MagXMin)/2))),-(event.magnetic.y - (MagYMin + ((MagYMax - MagYMin)/2))));
    
    if(heading < 0)
        heading += 2*PI;
        
    if(heading > 2*PI)
        heading -= 2*PI;
   
    float headingDegrees = heading * 180/M_PI; 
    return headingDegrees;
}

float getMagX(){
    sensors_event_t event; 
    mag.getEvent(&event);
    return event.magnetic.x;
}

float getMagY(){
    sensors_event_t event; 
    mag.getEvent(&event);
    return event.magnetic.y;
}

void initCompass(){
    Wire.begin(magSDAPin,magSCLPin);
    mag.begin();
}

void calibrateMag(void * pvParameters){
    motorHandled = true;
    sensors_event_t event; 
    mag.getEvent(&event);
    MagXMax = event.magnetic.x + 0.1;
    MagXMin = event.magnetic.x;
    MagYMax = event.magnetic.y + 0.1;
    MagYMin = event.magnetic.y;
    unsigned long startTime = millis();
    setMotorL(MagCalibrationSpeed);
    setMotorR(-MagCalibrationSpeed);
    while (motorHandled){
        mag.getEvent(&event);
        if(event.magnetic.x > MagXMax){
            MagXMax = event.magnetic.x;
        }
        if(event.magnetic.x < MagXMin){
            MagXMin = event.magnetic.x;
        }
        if(event.magnetic.y > MagYMax){
            MagYMax = event.magnetic.y;
        }
        if(event.magnetic.y < MagYMin){
            MagYMin = event.magnetic.y;
        }
        vTaskDelay(20/portTICK_PERIOD_MS);
    }
    setMotorL(0);
    setMotorR(0);
    endMotorTask();
}