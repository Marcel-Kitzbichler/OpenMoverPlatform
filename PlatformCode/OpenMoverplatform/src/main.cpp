#include <Arduino.h>
#include "config.h" 
#include "serialManager.h"
#include "MotorSet.h"
#include "compass.h"
#include "preferences.h"

extern double MagXMin;
extern double MagXMax;
extern double MagYMax;
extern double MagYMin;

void setup(){
  Preferences preferences;
  preferences.begin("botConfig", false);
  setMotorBias(preferences.getFloat("biasL", 1.0), preferences.getFloat("biasR", 1.0), false);
  MagXMin = preferences.getFloat("magXMin", 0.0);
  MagXMax = preferences.getFloat("magXMax", 0.0);
  MagYMin = preferences.getFloat("magYMin", 0.0);
  MagYMax = preferences.getFloat("magYMax", 0.0);
  preferences.end();
  Serial.begin(115200);
  Serial2.begin(GPSBaud);
  initCompass();
  motorSetup();
  xTaskCreatePinnedToCore(serialManager, "serialManager", 10000, NULL, 1, NULL, 1);
  vTaskDelete(NULL);
}

void loop(){
  vTaskDelete(NULL);
}
