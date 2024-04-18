#include "driver_accelerometer.hpp"
Adafruit_MPU6050 mpu;
sensors_event_t a, g, temp;

void initAcc()
{
  Serial.println("Adafruit MPU6050 test!");

  if (!mpu.begin()) 
  {
    while (1) 
    {
      Serial.println("Failed to find MPU6050 chip");
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  delay(100);
}

void readAcc()
{
  mpu.getEvent(&a, &g, &temp);
}

void sendAcc()
{
  memcpy(buffer + sizeof(peakToPeak), &a.acceleration.x, sizeof(a.acceleration.x));
  memcpy(buffer + sizeof(peakToPeak) + sizeof(a.acceleration.x), &a.acceleration.y, sizeof(a.acceleration.y));
  memcpy(buffer + sizeof(peakToPeak) + sizeof(a.acceleration.x) + sizeof(a.acceleration.y), &a.acceleration.z, sizeof(a.acceleration.z));

  SerialBT.write(buffer, sizeof(buffer));
}


