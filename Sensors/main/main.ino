#include <BluetoothSerial.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif


//Microphone
const int sampleWindow = 50;  
int const AMP_PIN = 15; //PIN D15      
unsigned int sample;
unsigned long startMillis = 0;
unsigned int peakToPeak = 0; 
unsigned int signalMax = 0;
unsigned int signalMin = 0;

//Accelerometer
const int PIN_X = 13;
const int PIN_Y = 12;
const int PIN_Z = 14;
unsigned int x = 0;
unsigned int y = 0;
unsigned int z = 0;

BluetoothSerial SerialBT;

void setup()
{
  //Serial.begin(9600);
  Serial.begin(115200);
  SerialBT.begin("ESP32");
}


void loop()
{
  readAcc();
  readMicro();
  sendMicro();
}

void readAcc()
{
  unsigned int x = analogRead(PIN_X);
  unsigned int y = analogRead(PIN_Y);
  unsigned int z = analogRead(PIN_Z);
  //printf("%d, %d, %d\n",x,y,z);
}

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
  uint8_t buffer[sizeof(peakToPeak)];
  memcpy(buffer, &peakToPeak, sizeof(peakToPeak));
  SerialBT.write(buffer, sizeof(buffer));
}