#include "driver_microphone.hpp"
#include "driver_accelerometer.hpp"
#include "driver_Mahony.hpp"

uint8_t buffer[16];
unsigned long now, last = 0; 
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };

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

  static float deltat = 0;

  now = micros();
  deltat = (now - last) * 1.0e-6; 
  last = now;

  Mahony_update(a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z,deltat);

  int temp;
  
  temp = (int)(q[0] * 16384.0f);
  teapotPacket[2] = (uint8_t)((temp >> 8) & 0xFF);
  teapotPacket[3] = (uint8_t)(temp & 0xFF);

  temp = (int)(q[1] * 16384.0f);
  teapotPacket[4] = (uint8_t)((temp >> 8) & 0xFF);
  teapotPacket[5] = (uint8_t)(temp & 0xFF);

  temp = (int)(q[2] * 16384.0f);
  teapotPacket[6] = (uint8_t)((temp >> 8) & 0xFF);
  teapotPacket[7] = (uint8_t)(temp & 0xFF);

  temp = (int)(q[3] * 16384.0f);
  teapotPacket[8] = (uint8_t)((temp >> 8) & 0xFF);
  teapotPacket[9] = (uint8_t)(temp & 0xFF);

  Serial.write(teapotPacket, 14);
  teapotPacket[11]++; 
}
