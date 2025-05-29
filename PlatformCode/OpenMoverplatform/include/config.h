#define motor1Pin 13
#define motor2Pin 12  
#define pwmCenter 1460
#define pwmMax 1060
#define pwmMin 1860
#define pwmDeadband 50
#define pwmFreq 50
#define pwmResolution 14
#define pwmChMotor1 0
#define pwmChMotor2 1
#define GPSInterval 920
#define GPSBaud 9600
#ifdef __ESP32D0WDQ6__
    #define magSDAPin 18
    #define magSCLPin 23
#endif
#ifdef __ESP32S3__
    #define magSDAPin 7
    #define magSCLPin 6
#endif
#define batteryADCPin 14
#define MagCalibrationTime 20000
#define MagCalibrationSpeed 20
#define BTSerialBufferSize 512