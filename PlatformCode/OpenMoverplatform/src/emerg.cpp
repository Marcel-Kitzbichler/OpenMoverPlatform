#include <Arduino.h>
#include <config.h>
#include "emerg.h"
#include "motorSet.h"

void emergencyStop(){
  Serial.println("Emergency Stop");
  setMotorL(0);
  setMotorR(0);
  while(true){};
}