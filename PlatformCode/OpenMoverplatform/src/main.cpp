#include <Arduino.h>
#include <ArduinoJson.h>
#include <config.h>
#include <emerg.h>


void emergencyStop();

JsonArray coordinates;

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
      coordinates = doc["coordinates"];
      Serial.println("recieved coordinates");
    }
    else if(messageIntention == 1){
      //send the currently stored coordinates via json
      serializeJson(coordinates, Serial);
    }

    else if(messageIntention == 2){
      
    }

    else{
      Serial.println("Invalid intent");
      emergencyStop();
    }
    }
  }
