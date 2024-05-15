import bluetooth
import time
import struct
import socket
import numpy as np
import matplotlib.pyplot as plt

find = True
finish = False
trigger = False

data_microphone = 0
q0 = 0
q1 = 0
q2 = 0
q3 = 0
status = b'0'
CoG = 0

class BluetoothReader:
    def __init__(self, bluetooth_name):
        self.BLUETOOTH_NAME = bluetooth_name
        self.socket = None
        self.connected = False
        self.processing_socket = None
        self.connect_processing = False

    def connect(self):
        global find
        try:
            devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in devices:
                if name == self.BLUETOOTH_NAME:
                    self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    self.socket.connect((addr, 1))
                    self.socket.settimeout(2)
                    self.connected = True
                    break
        except Exception as e:
            print("Error connecting to Bluetooth device:", e)

    def read(self):
        global status, trigger, CoG, data_microphone, finish, q0, q1, q2, q3
        time_before = 0
        i = 0
        try:
            while self.connected and not finish:
                
                data = self.socket.recv(20)
                self.getData(data)
                    
                if status == b'1' and time.time() - time_before > 3 :
                    status = b'0'

                if(data_microphone > 1000 and time.time() - time_before > 10):
                    trigger = True
                    CoG = 1
                    status = b'1'
                    time_before = time.time()


        except Exception as e:
            print("Error reading from Bluetooth device:", e)
            self.connected = False
        
    def getData(self, data):
        global data_microphone, q0, q1, q2, q3

        data_microphone = data[0] + 16**2*data[1]

        q0 = struct.unpack('f', data[4:8])[0]
        q1 = struct.unpack('f', data[8:12])[0]
        q2 = struct.unpack('f', data[12:16])[0]
        q3 = struct.unpack('f', data[16:20])[0]


    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            self.connected = False
            print("Disconnected from Bluetooth device")
        if self.processing_socket:
            self.processing_socket.close()
            print("Disconnected from Processing script")

bluetooth_name = "ESP32"
reader = BluetoothReader(bluetooth_name)


def main():
    reader.connect()
    if reader.connected:
        reader.read()
        reader.disconnect()
