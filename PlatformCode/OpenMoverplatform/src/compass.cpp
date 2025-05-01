#include <arduino.h>
#include "config.h"
#include "compass.h"
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(0);

float getHeading(){
sensors_event_t event; 
    mag.getEvent(&event);
    
    float heading = atan2(-(event.magnetic.x-57),-(event.magnetic.y-35));
    
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