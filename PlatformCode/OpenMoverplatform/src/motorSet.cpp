#include "motorSet.h"
#include "Arduino.h"
#include "config.h"
#include "Preferences.h"


const double uSecPWM = ((1000000/pwmFreq)/pow(2,pwmResolution));
float biasL = 1.0;
float biasR = 1.0;

int setPointL = 0;
int setPointR = 0;

void motorSetup() {
    ledcAttach(motor1Pin, pwmFreq, pwmResolution);
    ledcAttach(motor2Pin, pwmFreq, pwmResolution);
    ledcWrite(motor1Pin, pwmCenter / uSecPWM);
    ledcWrite(motor2Pin, pwmCenter / uSecPWM);
}

void setMotorL(int speed) {
    if (speed > 0) {
        ledcWrite(motor1Pin, (pwmCenter + (speed * biasL) + pwmDeadband) / uSecPWM);
    } else if (speed < 0) {
        ledcWrite(motor1Pin, (pwmCenter + (speed * biasL) - pwmDeadband) / uSecPWM);
    } else {
        ledcWrite(motor1Pin, pwmCenter / uSecPWM);
    }
    setPointL = speed;
}

void setMotorR(int speed) {
    if (speed > 0) {
        ledcWrite(motor2Pin, (pwmCenter + (speed * biasR) + pwmDeadband) / uSecPWM);
    } else if (speed < 0) {
        ledcWrite(motor2Pin, (pwmCenter + (speed * biasR) - pwmDeadband) / uSecPWM);
    } else {
        ledcWrite(motor2Pin, pwmCenter / uSecPWM);
    }
    setPointR = speed;
}

void setMotorBias(float biasL, float biasR, bool saveToPreferences) {
    ::biasL = biasL;
    ::biasR = biasR;
    if (saveToPreferences) {
        Preferences preferences;
        preferences.begin("botConfig", false);
        preferences.putFloat("biasL", biasL);
        preferences.putFloat("biasR", biasR);
        preferences.end();
    }
}

int getMotorL() {
    return setPointL;
} 

int getMotorR() {
    return setPointR;
}