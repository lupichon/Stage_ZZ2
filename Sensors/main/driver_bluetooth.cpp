#include "driver_bluetooth.hpp"

int LEN = 4;
int LENx2 = 2*LEN;
int LENx3 = 3*LEN;
int LENx4 = 4*LEN;
int LENx5 = 5*LEN;
int LENx6 = 6*LEN;
int LENx7 = 7*LEN;

void sendData()
{
  peakToPeak = 0;
  if (signalMax>=signalMin)
  {
    peakToPeak = signalMax - signalMin;
  }
  memcpy(buffer, &peakToPeak, sizeof(peakToPeak));

  memcpy(buffer + LEN, &a.acceleration.x, LEN);
  memcpy(buffer + LENx2, &a.acceleration.y, LEN);
  memcpy(buffer + LENx3, &a.acceleration.z, LEN);

  memcpy(buffer + LENx4, &q[0], LEN);
  memcpy(buffer + LENx5, &q[1], LEN);
  memcpy(buffer + LENx6, &q[2], LEN);
  memcpy(buffer + LENx7, &q[3], LEN);

  SerialBT.write(buffer,sizeof(buffer));
}