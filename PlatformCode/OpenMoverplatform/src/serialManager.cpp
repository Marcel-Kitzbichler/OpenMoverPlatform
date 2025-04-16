#include <Arduino.h>
#include "serialManager.h"
#include "ArduinoJson.h"
#include "config.h"
#include "emerg.h"
#include "wpManager.h" 
#include "BluetoothSerial.h"

bool motorHandled = false;
const double uSecPWM = ((1000000/pwmFreq)/pow(2,pwmResolution));

void serialManager(void * pvParameters){
    bool directMotorControlSerial = false;
    BluetoothSerial SerialBT;
    SerialBT.begin("OpenMoverPlatformBTSerial");
    int64_t coordinateTable[100];
    TaskHandle_t* motorControlHandle = NULL;
    while (true){
        if(Serial.available()){
            JsonDocument doc;
            DeserializationError error = deserializeJson(doc, Serial);
            if(error){
                Serial.print("deserializeJson() failed: ");
                Serial.println(error.f_str());
                emergencyStop();
            }

            int messageIntention = doc["intent"];

            if(messageIntention == 0){ 
                copyArray(doc["coordinates"], coordinateTable);
            }

            else if(messageIntention == 1){
                JsonDocument doc;
                copyArray(coordinateTable, doc["coordinates"]);
                serializeJson(doc, Serial);
            }

            else if(messageIntention == 2){
                if(!motorHandled){
                    motorHandled = true;
                    xTaskCreatePinnedToCore(wpManagerExec, "wpManagerExec", 10000,(void *) coordinateTable, 1, motorControlHandle, 1);
                }
            }

            else if(messageIntention == 3){
                if(motorControlHandle != NULL){
                    vTaskDelete(motorControlHandle);
                }
                motorHandled = doc["setStatus"].as<bool>();
                directMotorControlSerial = doc["setStatus"].as<bool>();
                ledcWrite(pwmChMotor1, (pwmCenter) / uSecPWM);
                ledcWrite(pwmChMotor2, (pwmCenter) / uSecPWM);
            }

            else if(messageIntention == 4){
                if(motorHandled && directMotorControlSerial){
                    ledcWrite(pwmChMotor1, (pwmCenter + doc["leftPWM"].as<int>()) / uSecPWM);
                    ledcWrite(pwmChMotor2, (pwmCenter + doc["rightPWM"].as<int>()) / uSecPWM);
                }
            }

            else{
                emergencyStop();
            }
        }
        
        if(SerialBT.available()){
            JsonDocument doc;
            DeserializationError error = deserializeJson(doc, SerialBT);
            if(error){
                Serial.print("deserializeJson() failed: ");
                Serial.println(error.f_str());
                emergencyStop();
            }

            int messageIntention = doc["intent"];

            if(messageIntention == 0){ 
                copyArray(doc["coordinates"], coordinateTable);
            }

            else if(messageIntention == 1){
                JsonDocument doc;
                copyArray(coordinateTable, doc["coordinates"]);
                serializeJson(doc, SerialBT);
            }

            else if(messageIntention == 2){
                if(!motorHandled){
                    motorHandled = true;
                    xTaskCreatePinnedToCore(wpManagerExec, "wpManagerExec", 10000,(void *) coordinateTable, 1, motorControlHandle, 1);
                }
            }

            else if(messageIntention == 3){
                if(motorControlHandle != NULL){
                    vTaskDelete(motorControlHandle);
                }
                motorHandled = doc["setStatus"].as<bool>();
                directMotorControlSerial = doc["setStatus"].as<bool>();
                ledcWrite(pwmChMotor1, (pwmCenter) / uSecPWM);
                ledcWrite(pwmChMotor2, (pwmCenter) / uSecPWM);
            }

            else if(messageIntention == 4){
                if(motorHandled && directMotorControlSerial){
                    ledcWrite(pwmChMotor1, (pwmCenter + doc["leftPWM"].as<int>()) / uSecPWM);
                    ledcWrite(pwmChMotor2, (pwmCenter + doc["rightPWM"].as<int>()) / uSecPWM);
                }
            }

            else{
                emergencyStop();
            }
        }
        vTaskDelay(500/portTICK_PERIOD_MS);
    }
}