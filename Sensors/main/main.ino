#include "driver_microphone.hpp"
#include "driver_accelerometer.hpp"

uint8_t buffer[16];

void setup()
{
  Serial.begin(115200);
  SerialBT.begin("ESP32");

  initAcc();
}


void loop()
{
  readMicro();
  readAcc();

  sendMicro();
  sendAcc();
}
