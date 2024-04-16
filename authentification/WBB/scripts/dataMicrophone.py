import bluetooth

find = True
trigger = False
data_microphone = 0

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
        global trigger, data_microphone
        try:
            while self.connected:
                data = self.socket.recv(4)
                data_microphone = data[0] + 16**2*data[1]
                if(data_microphone>1000):
                    trigger = True

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
