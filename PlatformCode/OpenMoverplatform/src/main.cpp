#include <Arduino.h>
#include <ArduinoJson.h>

#define motor1Pin 10
#define motor2Pin 11  
#define pwmCenter 127
#define pwmMax 200
#define pwmMin 50

void emergencyStop();

void setup(){
  Serial.begin(115200);
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
    Serial.print("Intent: ");
    Serial.println(messageIntention);
    switch (messageIntention){
      case 0:
        Serial.println("0");
        break;
      case 1:
        Serial.println("1");
        break;
      case 2:
        Serial.println("2");
        break;
      case 3:
        Serial.println("3");
        break;
      case 4:
        Serial.println("4");
        break;
      default:
        emergencyStop();
        break;
    }
  }
}

void emergencyStop(){
  Serial.println("Emergency Stop");
  analogWrite(motor1Pin, pwmCenter);
  analogWrite(motor2Pin, pwmCenter);
  while(true){};
}