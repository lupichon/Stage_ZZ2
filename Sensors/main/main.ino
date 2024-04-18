#include "driver_microphone.hpp"
//#include "driver_accelerometer.hpp"


void setup()
{
  //Serial.begin(9600);
  Serial.begin(115200);
  SerialBT.begin("ESP32");
  //init();
}


void loop()
{
  readMicro();
  sendMicro();
}
