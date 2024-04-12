import bluetooth

class BluetoothReader:
    def __init__(self, bluetooth_name):
        self.BLUETOOTH_NAME = bluetooth_name
        self.socket = None
        self.connected = False

    def connect(self):
        try:
            devices = bluetooth.discover_devices(lookup_names=True)
            for addr, name in devices:
                if name == self.BLUETOOTH_NAME:
                    self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                    self.socket.connect((addr, 1))
                    self.connected = True
                    break
            if not self.connected:
                raise Exception("Bluetooth device not found")
            else:
                print("Connected to Bluetooth device")
        except Exception as e:
            print("Error connecting to Bluetooth device:", e)

    def read(self):
        try:
            while self.connected:
                data = self.socket.recv(4)
                print("Received:",data[0] + 16**2*data[1])
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
reader.connect()
if reader.connected:
    reader.read()
    reader.disconnect()
