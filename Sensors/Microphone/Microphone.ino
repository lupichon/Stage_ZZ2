#include <BluetoothSerial.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

const int sampleWindow = 50;  
int const AMP_PIN = 15; //PIN D15      
unsigned int sample;

BluetoothSerial SerialBT;

void setup()
{
  //Serial.begin(9600);
  Serial.begin(115200);
  SerialBT.begin("ESP32");
}


void loop()
{
  unsigned long startMillis = millis();
  unsigned int peakToPeak = 0; 

  unsigned int signalMax = 0;
  unsigned int signalMin = 1024;

  unsigned int x = analogRead(13);
  unsigned int y = analogRead(12);
  unsigned int z = analogRead(14);

  printf("%d, %d, %d\n",x,y,z);

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
  if (signalMax>=signalMin)
  {
    peakToPeak = signalMax - signalMin;
    printf("%d\n",peakToPeak);
    uint8_t buffer[sizeof(peakToPeak)];
    memcpy(buffer, &peakToPeak, sizeof(peakToPeak));
    SerialBT.write(buffer, sizeof(buffer));
    /*if (Serial.available()) 
    {
    SerialBT.write(Serial.read());
    }
    if (SerialBT.available()) 
    {
      Serial.write(SerialBT.read());
    }
    Serial.println(peakToPeak);*/
  }
}