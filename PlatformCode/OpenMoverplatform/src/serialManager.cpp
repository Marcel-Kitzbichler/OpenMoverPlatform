#include <Arduino.h>
#include "serialManager.h"
#include "ArduinoJson.h"
#include "config.h"
#include "emerg.h"
#include "wpManager.h" 

bool motorHandled = false;

void serialManager(void * pvParameters){
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

            else{
                emergencyStop();
            }
        }
        vTaskDelay(500/portTICK_PERIOD_MS);
    }
}