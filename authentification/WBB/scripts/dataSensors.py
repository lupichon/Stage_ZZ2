import bluetooth
import time
import struct

find = True
finish = False
trigger = False

data_microphone = 0
acceleration_x = 0
acceleration_y = 0
acceleration_z = 0

class BluetoothReader:
    def __init__(self, bluetooth_name):
        self.BLUETOOTH_NAME = bluetooth_name
        self.socket = None
        self.connected = False

    def connect(self):
        global find
        try:
            devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in devices:
                if name == self.BLUETOOTH_NAME:
                    self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    self.socket.connect((addr, 1))
                    self.connected = True
                    break
            if not self.connected:
                find = False
                raise Exception("Bluetooth device not found")
            else:
                print("Connected to Bluetooth device")
        except Exception as e:
            print("Error connecting to Bluetooth device:", e)

    def read(self):
        global trigger, data_microphone, finish, acceleration_x, acceleration_y, acceleration_z
        time_before = 0
        try:
            while self.connected and not finish:
                data = self.socket.recv(16)
                data_microphone = data[0] + 16**2*data[1]
                acceleration_x = struct.unpack('f', data[4:8])[0]
                acceleration_y = struct.unpack('f', data[8:12])[0]
                acceleration_z = struct.unpack('f', data[12:16])[0]
            
                if(data_microphone>1000 and time.time() - time_before >5):
                    trigger = True
                    time_before = time.time()

        except Exception as e:
            print("Error reading from Bluetooth device:", e)
            self.connected = False
            if self.socket:
                self.socket.close()

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.connected = False
            print("Disconnected from Bluetooth device")

bluetooth_name = "ESP32"
reader = BluetoothReader(bluetooth_name)

def main():
    reader.connect()
    if reader.connected:
        reader.read()
        reader.disconnect()
