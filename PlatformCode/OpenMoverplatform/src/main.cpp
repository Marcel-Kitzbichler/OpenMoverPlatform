#include <Arduino.h>
#include "config.h" 
#include "serialManager.h"



void setup(){
  Serial.begin(115200);
  Serial.println("Starting");
  analogWrite(motor1Pin, pwmCenter);
  analogWrite(motor2Pin, pwmCenter);
  xTaskCreatePinnedToCore(serialManager, "serialManager", 10000, NULL, 1, NULL, 1);
  vTaskDelete(NULL);
}

void loop(){
  vTaskDelete(NULL);
}
