#include <Arduino.h>
#include "config.h" 
#include "serialManager.h"
#include "MotorSet.h"


void setup(){
  Serial.begin(115200);
  motorSetup();
  xTaskCreatePinnedToCore(serialManager, "serialManager", 10000, NULL, 1, NULL, 1);
  vTaskDelete(NULL);
}

void loop(){
  vTaskDelete(NULL);
}
