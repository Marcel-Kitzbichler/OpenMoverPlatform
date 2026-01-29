#include <Arduino.h>
#include "serialManager.h"
#include "ArduinoJson.h"
#include "config.h"
#include "emerg.h"
#include "wpManager.h" 
#include "battery.h"
#include "motorSet.h"
#include "TinyGPSPlus.h"
#include "goTo.h"
#include "compass.h"

#ifdef __ESP32D0WDQ6__
    #include "BluetoothSerial.h"
    BluetoothSerial SerialBT;
#endif

#ifdef __ESP32S3__
    #include "BLESerial.h"
    BLESerial<> SerialBT;
#endif

bool motorHandled = false;
TaskHandle_t motorControlHandle = NULL;
TinyGPSPlus gps;
extern double MagXMin;
extern double MagXMax;
extern double MagYMax;
extern double MagYMin;

void serialManager(void * pvParameters){
    Serial.begin(115200);
    Serial2.begin(GPSBaud, SERIAL_8N1, 16, 15);

    bool directMotorControlSerial = false;
    unsigned long lastGPS = millis();
    SerialBT.begin("OpenMoverPlatformBTSerial");
    double coordinateTable[100];
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
                    motorControlHandle = NULL;
                    if(!xTaskCreatePinnedToCore(wpManagerExec, "wpManagerExec", 10000,(void *) coordinateTable, 1, &motorControlHandle, 1)){
                        motorHandled = false;
                    }
                }
            }

            else if(messageIntention == 3){
                if(motorControlHandle != NULL){
                    vTaskDelete(motorControlHandle);
                    motorControlHandle = NULL;
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
                doc["numSats"] = gps.satellites.value();
                doc["fix"] = gps.location.isValid();
                doc["locationAge"] = gps.location.age();
                doc["lat"] = gps.location.lat();
                doc["lon"] = gps.location.lng();
                doc["heading"] = getHeading();
                doc["serialControl"] = directMotorControlSerial;
                doc["motorHandled"] = motorHandled;
                doc["magXMin"] = MagXMin;
                doc["magXMax"] = MagXMax;
                doc["magYMin"] = MagYMin;
                doc["magYMax"] = MagYMax;
                doc["setPointL"] = getMotorL();
                doc["setPointR"] = getMotorR();
                serializeJson(doc, Serial);
            }

            else if(messageIntention == 7){
                double* params = new double[4]; // Dynamically allocate memory for params
                params[0] = doc["lat"].as<double>();
                params[1] = doc["lon"].as<double>();
                params[2] = doc["speed"].as<double>();
                params[3] = doc["range"].as<double>();
                if (!motorHandled){
                    motorHandled = true;
                    motorControlHandle = NULL;
                    if(!xTaskCreatePinnedToCore(executePlainGoTo, "executePlainGoTo", 10000, (void *) params, 1, &motorControlHandle, 1)){
                        motorHandled = false;
                        delete[] params; // Free memory if task creation fails
                    }
                }
            }

            else if (messageIntention == 8) {
                if (!motorHandled){
                    motorHandled = true;
                    motorControlHandle = NULL;
                    if(!xTaskCreatePinnedToCore(calibrateMag, "calibrateCompass", 10000, NULL, 1, &motorControlHandle, 1)){
                        motorHandled = false;
                    }
                }
            }

            else if (messageIntention == 9) {
                JsonDocument doc;
                doc["magXMin"] = MagXMin;
                doc["magXMax"] = MagXMax;
                doc["magYMin"] = MagYMin;
                doc["magYMax"] = MagYMax;
                doc["magX"] = getMagX();
                doc["magY"] = getMagY();
                serializeJson(doc, Serial);
            }

            else if (messageIntention == 10) {
                setMotorBias(doc["biasL"].as<float>(), doc["biasR"].as<float>());
            }

            else{
                emergencyStop();
            }
        }
        
        if(SerialBT.available()){
            
            char buffer[BTSerialBufferSize];

            const int availableBytes = SerialBT.available();
            for(int i=0; SerialBT.available() && i < BTSerialBufferSize; i++)
            {
                buffer[i] = SerialBT.read();
                if(buffer[i] == '}'){ // Check for end of JSON message
                    break;
                }
                SerialBT.flush();
            }

            buffer[0] = '{';

            JsonDocument doc;
            DeserializationError error = deserializeJson(doc, buffer);

            if(error){
                Serial.print("deserializeJson() failed: ");
                Serial.println(error.f_str());
                //emergencyStop();
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
                    motorControlHandle = NULL;
                    if(!xTaskCreatePinnedToCore(wpManagerExec, "wpManagerExec", 10000,(void *) coordinateTable, 1, &motorControlHandle, 1)){
                        motorHandled = false;
                    }
                }
            }

            else if(messageIntention == 3){
                if(motorControlHandle != NULL){
                    vTaskDelete(motorControlHandle);
                    motorControlHandle = NULL;
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
                doc["numSats"] = gps.satellites.value();
                doc["fix"] = gps.location.isValid();
                doc["locationAge"] = gps.location.age();
                doc["lat"] = gps.location.lat();
                doc["lon"] = gps.location.lng();
                doc["heading"] = getHeading();
                doc["serialControl"] = directMotorControlSerial;
                doc["motorHandled"] = motorHandled;
                doc["magXMin"] = MagXMin;
                doc["magXMax"] = MagXMax;
                doc["magYMin"] = MagYMin;
                doc["magYMax"] = MagYMax;
                doc["setPointL"] = getMotorL();
                doc["setPointR"] = getMotorR();
                char respBuffer[BTSerialBufferSize];
                size_t respLen = serializeJson(doc, respBuffer, sizeof(buffer));
                SerialBT.write((const uint8_t*)respBuffer, respLen);
            }

            else if(messageIntention == 7){
                double* params = new double[4]; // Dynamically allocate memory for params
                params[0] = doc["lat"].as<double>();
                params[1] = doc["lon"].as<double>();
                params[2] = doc["speed"].as<double>();
                params[3] = doc["range"].as<double>();
                if (!motorHandled){
                    motorHandled = true;
                    motorControlHandle = NULL;
                    if(!xTaskCreatePinnedToCore(executePlainGoTo, "executePlainGoTo", 10000, (void *) params, 1, &motorControlHandle, 1)){
                        motorHandled = false;
                        delete[] params; // Free memory if task creation fails
                    }
                }
            }

            else if (messageIntention == 8) {
                if (!motorHandled){
                    motorHandled = true;
                    motorControlHandle = NULL;
                    if(!xTaskCreatePinnedToCore(calibrateMag, "calibrateCompass", 10000, NULL, 1, &motorControlHandle, 1)){
                        motorHandled = false;
                    }
                }
            }

            else if (messageIntention == 9) {
                JsonDocument doc;
                doc["magXMin"] = MagXMin;
                doc["magXMax"] = MagXMax;
                doc["magYMin"] = MagYMin;
                doc["magYMax"] = MagYMax;
                doc["magX"] = getMagX();
                doc["magY"] = getMagY();
                char respBuffer[BTSerialBufferSize];
                size_t respLen = serializeJson(doc, respBuffer, sizeof(buffer));
                SerialBT.write((const uint8_t*)respBuffer, respLen);
            }

            else if (messageIntention == 10) {
                setMotorBias(doc["biasL"].as<float>(), doc["biasR"].as<float>());
            }

            else{
                //emergencyStop();
            }
        }

        if(Serial2.available() && millis() - lastGPS > GPSInterval){
            lastGPS = millis();
            while(Serial2.available() > 0 && millis() - lastGPS < GPSInterval){ // this while loop takes around 6ms to complete
                gps.encode(Serial2.read());
            }
        }
        vTaskDelay(50/portTICK_PERIOD_MS);
    }
}