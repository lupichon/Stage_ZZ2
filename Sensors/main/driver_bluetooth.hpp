#ifndef H__DRIVER_B__H
#define H__DRIVER_B__H

#include <BluetoothSerial.h>

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

extern BluetoothSerial SerialBT;
extern uint8_t buffer[16]; 
#endif