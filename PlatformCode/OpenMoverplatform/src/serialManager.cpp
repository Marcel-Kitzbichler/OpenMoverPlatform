#include <Arduino.h>
#include "serialManager.h"
#include "ArduinoJson.h"
#include "config.h"
#include "emerg.h"
#include "wpManager.h" 

bool motorHandled = false;

void serialManager(void * pvParameters){
    int coordinateTable[99][2];
    TaskHandle_t* motorControlHandle = NULL;
    while (true){
        if(Serial.available()){
            StaticJsonDocument<200> doc;
            DeserializationError error = deserializeJson(doc, Serial);
            if(error){
                Serial.print("deserializeJson() failed: ");
                Serial.println(error.f_str());
                emergencyStop();
            }

            int messageIntention = doc["intent"];

            if(messageIntention == 0){ 
                //recieve array of coordinates
                copyArray(doc["coordinates"], coordinateTable);
                Serial.println("recieved coordinates");
            }

            else if(messageIntention == 1){
                //send the currently stored coordinates via json
            }

            else if(messageIntention == 2){
                if(!motorHandled){
                    motorHandled = true;
                    xTaskCreatePinnedToCore(wpManagerExec, "wpManagerExec", 10000,(void *) coordinateTable, 1, motorControlHandle, 1);
                }
                else{
                    Serial.println("Motor is currently busy");
                }
            }

            else{
                Serial.println("Invalid intent");
                emergencyStop();
            }
        }
        vTaskDelay(500/portTICK_PERIOD_MS);
    }
}