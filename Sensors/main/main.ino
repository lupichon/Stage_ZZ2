#include "driver_microphone.hpp"
#include "driver_accelerometer.hpp"
#include "MahonyAHRS.h"

uint8_t buffer[16];

float q[4] = {1.0, 0.0, 0.0, 0.0};
float Kp = 30.0;
float Ki = 0.0;
unsigned long now, last = 0; //millis() timers
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };

float GyroMeasError = PI * (60.0f / 180.0f);     
float beta = sqrt(3.0f / 4.0f) * GyroMeasError;  

float GyroMeasDrift = PI * (1.0f / 180.0f);     
float zeta = sqrt(3.0f / 4.0f) * GyroMeasDrift;  

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
  //MadgwickQuaternionUpdate(a.acceleration.x, a.acceleration.y, a.acceleration.z, g.gyro.x, g.gyro.y, g.gyro.z,deltat);

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

void Mahony_update(float ax, float ay, float az, float gx, float gy, float gz, float deltat) 
{
  float recipNorm;
  float vx, vy, vz;
  float ex, ey, ez;  //error terms
  float qa, qb, qc;
  static float ix = 0.0, iy = 0.0, iz = 0.0;  //integral feedback terms
  float tmp;

  // Compute feedback only if accelerometer measurement valid (avoids NaN in accelerometer normalisation)
  tmp = ax * ax + ay * ay + az * az;

  if (tmp > 0.0)
  {
    Serial.print(a.acceleration.x);
    Serial.print(" ");
    Serial.print(a.acceleration.y);
    Serial.print(" ");
    Serial.println(a.acceleration.z);

    // Normalise accelerometer (assumed to measure the direction of gravity in body frame)
    recipNorm = 1.0 / sqrt(tmp);
    ax *= recipNorm;
    ay *= recipNorm;
    az *= recipNorm;

    // Estimated direction of gravity in the body frame (factor of two divided out)
    vx = q[1] * q[3] - q[0] * q[2];
    vy = q[0] * q[1] + q[2] * q[3];
    vz = q[0] * q[0] - 0.5f + q[3] * q[3];

    // Error is cross product between estimated and measured direction of gravity in body frame
    // (half the actual magnitude)
    ex = (ay * vz - az * vy);
    ey = (az * vx - ax * vz);
    ez = (ax * vy - ay * vx);

    // Compute and apply to gyro term the integral feedback, if enabled
    if (Ki > 0.0f) {
      ix += Ki * ex * deltat;  // integral error scaled by Ki
      iy += Ki * ey * deltat;
      iz += Ki * ez * deltat;
      gx += ix;  // apply integral feedback
      gy += iy;
      gz += iz;
    }

    // Apply proportional feedback to gyro term
    gx += Kp * ex;
    gy += Kp * ey;
    gz += Kp * ez;
  }

  // Integrate rate of change of quaternion, q cross gyro term
  deltat = 0.5 * deltat;
  gx *= deltat;   // pre-multiply common factors
  gy *= deltat;
  gz *= deltat;
  qa = q[0];
  qb = q[1];
  qc = q[2];

  float newValue0 = -qb * gx - qc * gy - q[3] * gz;
  float newValue1 = qa * gx + qc * gz - q[3] * gy;
  float newValue2 = qa * gy - qb * gz + q[3] * gx;
  float newValue3 = qa * gz + qb * gy - qc * gx;

  if(abs(newValue0)>0.003)
  {
    q[0] += newValue0;
  }
  if(abs(newValue1)>0.003)
  {
    q[1] += newValue1;
  }
  if(abs(newValue2)>0.003)
  {
    q[2] += newValue2;
  }
  if(abs(newValue3)>0.003)
  {
    q[3] += newValue3;
  }

  Serial.println(q[3]);

  // renormalise quaternion
  recipNorm = 1.0 / sqrt(q[0] * q[0] + q[1] * q[1] + q[2] * q[2] + q[3] * q[3]);
  q[0] = q[0] * recipNorm;
  q[1] = q[1] * recipNorm;
  q[2] = q[2] * recipNorm;
  //q[3] = q[3] * recipNorm;
  q[3] = 0;

}
