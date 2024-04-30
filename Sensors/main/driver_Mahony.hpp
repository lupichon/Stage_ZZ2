#ifndef H__MAHONY__H
#define H__MAHONY__H

#include <Wire.h>
#include <Arduino.h>

extern float q[4];
extern float Kp;
extern float Ki;

void Mahony_update(float ax, float ay, float az, float gx, float gy, float gz, float deltat);

#endif

