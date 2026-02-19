#include <Arduino.h>	
#include "endMotorTask.h"
#include "motorSet.h"

extern TaskHandle_t motorControlHandle;
extern bool motorHandled;

void endMotorTask() {
    setMotorL(0);
    setMotorR(0);
    motorHandled = false; // Mark the task as finished
    motorControlHandle = NULL; // Reset the handle to NULL
    vTaskDelete(NULL); // Delete the task
}