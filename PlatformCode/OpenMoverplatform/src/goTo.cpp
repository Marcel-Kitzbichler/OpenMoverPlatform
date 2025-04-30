#include <Arduino.h> 
#include "goTo.h"
#include "MotorSet.h"
#include "TinyGPSPlus.h"
#include "endMotorTask.h"

extern bool motorHandled;
extern TinyGPSPlus gps;

void executePlainGoTo(void * pvParameters) {
    motorHandled = true; // Mark the task as started
    double* params = (double*)pvParameters;
    double targetLat = params[0];
    double targetLon = params[1];
    int speed = (int)params[2];
    double range = (double)params[3];

    goTo(targetLat, targetLon, speed, range);
    delete[] params;
    endMotorTask(); // Call the function to end the motor task
}

void goTo(double lat, double lon, int speed, double range) {
    while (motorHandled) {
        if (!(gps.location.isValid()&&gps.course.isValid())) {
            setMotorL(0);
            setMotorR(0);
            return;
        }

        double currentLat = gps.location.lat();
        double currentLon = gps.location.lng();
        double distanceToTarget = TinyGPSPlus::distanceBetween(currentLat, currentLon, lat, lon);

        if (distanceToTarget <= range) {
            Serial.println("Target reached within range.");
            setMotorL(0); // Stop left motor
            setMotorR(0); // Stop right motor
            return;
        }

        double courseToTarget = gps.courseTo(currentLat, currentLon, lat, lon);
        double currentCourse = gps.course.deg(); // Assuming current course is available
        double courseError = courseToTarget - currentCourse;

        // Normalize course error to range [-180, 180]
        if (courseError > 180) courseError -= 360;
        if (courseError < -180) courseError += 360;

        // Adjust motor speeds based on course error for tank steering
        int leftMotorSpeed = speed;
        int rightMotorSpeed = speed;

        if (courseError > 0) {
            // Turn right
            leftMotorSpeed = speed;
            rightMotorSpeed = speed - (int)((abs(courseError) / 180.0 * speed / 2));
        } else if (courseError < 0) {
            // Turn left
            leftMotorSpeed = speed - (int)((abs(courseError) / 180.0 * speed / 2));
            rightMotorSpeed = speed;
        }

        leftMotorSpeed = constrain(leftMotorSpeed, 0, 100);
        rightMotorSpeed = constrain(rightMotorSpeed, 0, 100);

        setMotorL(leftMotorSpeed);
        setMotorR(rightMotorSpeed);

        vTaskDelay(500/portTICK_PERIOD_MS); // Adjust delay as needed
    }
}