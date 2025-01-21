#include <Arduino.h>
#include "config.h" 
#include "serialManager.h"


double uSecPWM;

void setup(){
  Serial.begin(115200);
  Serial.println("Starting");
  Serial2.begin(9600);
  uSecPWM = ((1000000/pwmFreq)/pow(2,pwmResolution));
  Serial.println(uSecPWM);
  ledcSetup(0, pwmFreq, pwmResolution);
  ledcSetup(1, pwmFreq, pwmResolution);
  ledcAttachPin(motor1Pin, 0);
  ledcAttachPin(motor2Pin, 1);
  ledcWrite(0, pwmCenter / uSecPWM);
  ledcWrite(1, pwmCenter / uSecPWM);
  xTaskCreatePinnedToCore(serialManager, "serialManager", 10000, NULL, 1, NULL, 1);
  vTaskDelete(NULL);
}

void loop(){
  vTaskDelete(NULL);
}
