#include <Arduino.h>
#include "config.h" 
#include "serialManager.h"


const double uSecPWM = ((1000000/pwmFreq)/pow(2,pwmResolution));

void setup(){
  Serial.begin(115200);
  Serial.println(uSecPWM);
  ledcSetup(pwmChMotor1, pwmFreq, pwmResolution);
  ledcSetup(pwmChMotor2, pwmFreq, pwmResolution);
  ledcAttachPin(motor1Pin, pwmChMotor1);
  ledcAttachPin(motor2Pin, pwmChMotor2);
  ledcWrite(pwmChMotor1, pwmCenter / uSecPWM);
  ledcWrite(pwmChMotor2, pwmCenter / uSecPWM);
  xTaskCreatePinnedToCore(serialManager, "serialManager", 10000, NULL, 1, NULL, 1);
  vTaskDelete(NULL);
}

void loop(){
  vTaskDelete(NULL);
}
