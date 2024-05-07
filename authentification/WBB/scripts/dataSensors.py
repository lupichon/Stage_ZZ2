import bluetooth
import time
import struct
import socket

find = True
finish = False
trigger = False
visualisation = False

data_microphone = 0
acceleration_x = 0
acceleration_y = 0
acceleration_z = 0
q0 = 0
q1 = 0
q2 = 0
q3 = 0
status = 0
CoG = 0

HOST = '127.0.0.1'
PORT = 12345



class BluetoothReader:
    def __init__(self, bluetooth_name):
        self.BLUETOOTH_NAME = bluetooth_name
        self.socket = None
        self.connected = False
        self.processing_socket = None
        self.connect_processing = False

    def connect(self):
        global find, HOST, PORT
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
                try : 
                    self.processing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.processing_socket.connect((HOST, PORT))
                    self.connect_processing = True
                except Exception as e : 
                    print(e)
        except Exception as e:
            print("Error connecting to Bluetooth device:", e)

    def read(self):
        global status, trigger, CoG, data_microphone, finish, acceleration_x, acceleration_y, acceleration_z, q0, q1, q2, q3
        time_before = 0
        i = 0
        try:
            while self.connected and not finish:
                data = self.socket.recv(32)
                data_microphone = data[0] + 16**2*data[1]

                acceleration_x = round(struct.unpack('f', data[4:8])[0], 2)
                acceleration_y = round(struct.unpack('f', data[8:12])[0], 2)
                acceleration_z = round(struct.unpack('f', data[12:16])[0], 2)

                q0 = struct.unpack('f', data[16:20])[0]
                q1 = struct.unpack('f', data[20:24])[0]
                q2 = struct.unpack('f', data[24:28])[0]
                q3 = struct.unpack('f', data[28:32])[0]

                if status == b'1' and time.time() - time_before > 3 :
                    status = b'0'

                if(data_microphone > 1000 and time.time() - time_before > 10):
                    trigger = True
                    CoG = 1
                    status = b'1'
                    time_before = time.time()

                if self.connect_processing == True and not visualisation:
                    try : 
                        self.processing_socket.sendall(data[16:32] + status)
                    except : 
                        self.connect_processing = False

                elif i==19 and not visualisation:
                    try : 
                        self.processing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.processing_socket.connect((HOST, PORT))
                        self.connect_processing = True
                    except Exception as e: 
                        print(e)

                i = (i+1)%20

        except Exception as e:
            print("Error reading from Bluetooth device:", e)
            self.connected = False

    def disconnect(self):
        if self.socket:
            self.socket.close()
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
