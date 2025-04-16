#include <Arduino.h>
#include "config.h"

double batteryVoltage(){
    return analogRead(batteryADCPin) * 0.003223443223443;
}