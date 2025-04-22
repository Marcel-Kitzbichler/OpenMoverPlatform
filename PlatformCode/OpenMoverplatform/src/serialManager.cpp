#include <Arduino.h>
#include "serialManager.h"
#include "ArduinoJson.h"
#include "config.h"
#include "emerg.h"
#include "wpManager.h" 
#include "BluetoothSerial.h"
#include "battery.h"
#include "motorSet.h"

bool motorHandled = false;

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

            if(messageIntention == 5){ 
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
                setMotorL(0);
                setMotorR(0);
            }

            else if(messageIntention == 4){
                if(motorHandled && directMotorControlSerial){
                    setMotorL(doc["leftPWM"].as<int>());
                    setMotorR(doc["rightPWM"].as<int>());
                }
            }

            else if(messageIntention == 6){
                JsonDocument doc;
                doc["batteryVoltage"] = batteryVoltage();
                serializeJson(doc, Serial);
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

            if(messageIntention == 5){ 
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
                setMotorL(0);
                setMotorR(0);
            }

            else if(messageIntention == 4){
                if(motorHandled && directMotorControlSerial){
                    setMotorL(doc["leftPWM"].as<int>());
                    setMotorR(doc["rightPWM"].as<int>());
                }
            }

            else if(messageIntention == 6){
                JsonDocument doc;
                doc["batteryVoltage"] = batteryVoltage();
                serializeJson(doc, SerialBT);
            }

            else{
                emergencyStop();
            }
        }
        vTaskDelay(250/portTICK_PERIOD_MS);
    }
}