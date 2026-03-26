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
    ledcSetup(pwmChMotor1, pwmFreq, pwmResolution);
    ledcSetup(pwmChMotor2, pwmFreq, pwmResolution);
    ledcAttachPin(motor1Pin, pwmChMotor1);
    ledcAttachPin(motor2Pin, pwmChMotor2);
    ledcWrite(pwmChMotor1, pwmCenter / uSecPWM);
    ledcWrite(pwmChMotor2, pwmCenter / uSecPWM);
}

void setMotorL(int speed) {
    if (speed > 0) {
        ledcWrite(pwmChMotor1, (pwmCenter + (speed * biasL) + pwmDeadband) / uSecPWM);
    } else if (speed < 0) {
        ledcWrite(pwmChMotor1, (pwmCenter + (speed * biasL) - pwmDeadband) / uSecPWM);
    } else {
        ledcWrite(pwmChMotor1, pwmCenter / uSecPWM);
    }
    setPointL = speed;
}

void setMotorR(int speed) {
    if (speed > 0) {
        ledcWrite(pwmChMotor2, (pwmCenter + (speed * biasR) + pwmDeadband) / uSecPWM);
    } else if (speed < 0) {
        ledcWrite(pwmChMotor2, (pwmCenter + (speed * biasR) - pwmDeadband) / uSecPWM);
    } else {
        ledcWrite(pwmChMotor2, pwmCenter / uSecPWM);
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