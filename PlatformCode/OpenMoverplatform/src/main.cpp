#include <Arduino.h>
#include "ArduinoJson.h"
#include "config.h"
#include "emerg.h"
#include "wpManager.h" 

int coordinateTable[99][2];

void setup(){
  Serial.begin(115200);
  Serial.println("Starting");
  analogWrite(motor1Pin, pwmCenter);
  analogWrite(motor2Pin, pwmCenter);
}

void loop(){
  //wait unitl json data is available on the serial port and then parse it when it is available
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
        
        xTaskCreatePinnedToCore(wpManagerExec, "wpManagerExec", 10000,(void *) coordinateTable, 1, NULL, 1);
      }

      else{
        Serial.println("Invalid intent");
        emergencyStop();
      }
      vTaskDelay(500/portTICK_PERIOD_MS);
    }
  }
