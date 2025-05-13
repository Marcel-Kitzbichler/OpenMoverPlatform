void motorSetup();

void setMotorL(int speed);
void setMotorR(int speed);

void setMotorBias(float biasL, float biasR, bool saveToPreferences = true);

int getMotorL();
int getMotorR();
