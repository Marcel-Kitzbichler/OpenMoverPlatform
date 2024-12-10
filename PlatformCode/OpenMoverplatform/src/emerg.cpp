#include <Arduino.h>
#include <config.h>

void emergencyStop(){
  Serial.println("Emergency Stop");
  analogWrite(motor1Pin, pwmCenter);
  analogWrite(motor2Pin, pwmCenter);
  while(true){};
}