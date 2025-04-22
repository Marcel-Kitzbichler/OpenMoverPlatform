#include "motorSet.h"
#include "Arduino.h"
#include "config.h"


const double uSecPWM = ((1000000/pwmFreq)/pow(2,pwmResolution));

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
        ledcWrite(pwmChMotor1, (pwmCenter + speed + pwmDeadband) / uSecPWM);
    } else if (speed < 0) {
        ledcWrite(pwmChMotor1, (pwmCenter - speed - pwmDeadband) / uSecPWM);
    } else {
        ledcWrite(pwmChMotor1, pwmCenter / uSecPWM);
    }
}

void setMotorR(int speed) {
    if (speed > 0) {
        ledcWrite(pwmChMotor2, (pwmCenter + speed + pwmDeadband) / uSecPWM);
    } else if (speed < 0) {
        ledcWrite(pwmChMotor2, (pwmCenter - speed - pwmDeadband) / uSecPWM);
    } else {
        ledcWrite(pwmChMotor2, pwmCenter / uSecPWM);
    }
}