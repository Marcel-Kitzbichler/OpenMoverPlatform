#include <Arduino.h>
#include <config.h>

void emergencyStop(){
  Serial.println("Emergency Stop");
  while(true){};
}