#include "driver_microphone.hpp"

const int sampleWindow = 50;  
int const AMP_PIN = 15; //PIN D15      
unsigned int sample;
unsigned long startMillis = 0;
unsigned int peakToPeak = 0; 
unsigned int signalMax = 0;
unsigned int signalMin = 0;

BluetoothSerial SerialBT;

void readMicro()
{
  startMillis = millis();
  peakToPeak = 0; 
  signalMax = 0;
  signalMin = 1024;

  while (millis() - startMillis < sampleWindow)
  {
    sample = analogRead(AMP_PIN);

    if (sample < 1024)  
    {
      if (sample > signalMax)
      {
        signalMax = sample; 
      }
      else if (sample < signalMin)
      {
        signalMin = sample;  
      }
    }
  }
}

void sendMicro()
{
  peakToPeak = 0;
  if (signalMax>=signalMin)
  {
    peakToPeak = signalMax - signalMin;
  }
  memcpy(buffer, &peakToPeak, sizeof(peakToPeak));
}