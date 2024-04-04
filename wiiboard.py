import sys
import bluetooth
import threading
import time
import pygame
import socket 
import math 

base = pygame.USEREVENT
WIIBOARD_BUTTON_PRESS = base + 1
WIIBOARD_BUTTON_RELEASE = base + 2
WIIBOARD_MASS = base + 3				
WIIBOARD_CONNECTED = base + 4
WIIBOARD_DISCONNECTED = base + 5

COMMAND_LIGHT = 11
COMMAND_REPORTING = 12
COMMAND_REQUEST_STATUS = 15
COMMAND_REGISTER = 16
COMMAND_READ_REGISTER = 17

BUTTON_DOWN_MASK = 8

BLUETOOTH_NAME = "Nintendo RVL-WBC-01"

#dimensions of the WBB
L = 43			
W = 24.5

class BoardEvent:
	
	def __init__(self, topLeft,topRight,bottomLeft,bottomRight, buttonPressed, buttonReleased):
		self.topLeft = topLeft
		self.topRight = topRight
		self.bottomLeft = bottomLeft
		self.bottomRight = bottomRight
		self.buttonPressed = buttonPressed
		self.buttonReleased = buttonReleased
		self.totalWeight = topLeft + topRight + bottomLeft + bottomRight
		try : 
			self.CoMx = (L/2) * ((topRight + bottomRight) - (topLeft + bottomLeft))/(topRight + bottomRight + topLeft + bottomLeft)
			self.CoMy = (W/2) * ((topRight + topLeft) - (bottomRight + bottomLeft))/(topRight + bottomRight + topLeft + bottomLeft)
		except : 
			pass

class Wiiboard:
	receivesocket = None
	controlsocket = None

	def __init__(self):
		self.calibration = []
		self.LED = False
		self.address = None
		self.buttonDown = False

		self.status = "Disconnected"
		self.lastEvent = BoardEvent(0,0,0,0,False,False)

		try:
			self.receivesocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
			self.controlsocket = bluetooth.BluetoothSocket(bluetooth.L2CAP)
		except ValueError:
			raise Exception("Error: Bluetooth not found")

	def isConnected(self):
		if self.status == "Connected":
			return True
		else:
			return False

	# Connect to the Wiiboard at bluetooth address <address>
	def connect(self, address):
		if address is None:
			print("Non existant address")
			return
		self.receivesocket.connect((address, 0x13))
		self.receivesocket.settimeout(120)
		self.controlsocket.connect((address, 0x11))
		if self.receivesocket and self.controlsocket:
			print("Connected to Wiiboard at address " + address)
			self.status = "Connected"
			self.address = address
			thread = threading.Thread(target=self.receivethread, args=())
			thread.start()
			useExt = ["00", COMMAND_REGISTER, "04", "A4", "00", "40", "00"]
			self.send(useExt)
			
			pygame.event.post(pygame.event.Event(WIIBOARD_CONNECTED))
		else:
			print("Could not connect to Wiiboard at address " + address)


	# Disconnect from the Wiiboard
	def disconnect(self):
		try:
			self.receivesocket.close()
			self.controlsocket.close()
			pygame.event.post(pygame.event.Event(WIIBOARD_DISCONNECTED))
			self.status = "Disconnected"
		except:
			pass
		print("WiiBoard disconnected")

	# Try to discover a Wiiboard
	def discover(self):
		print ("Press the red sync button on the board now")
		address = None
		bluetoothdevices = bluetooth.discover_devices(duration = 3, lookup_names = True)
		for bluetoothdevice in bluetoothdevices:
			if bluetoothdevice[1] == BLUETOOTH_NAME:
				address = bluetoothdevice[0]
				print ("Found Wiiboard at address " + address)
		if address == None:
			print ("No Wiiboards discovered.")
		return address
	
	
	def wait(self,millis):
		time.sleep(millis / 1000.0)
		
	def setLight(self, light):
		val = "00"
		if light == True:
			val = "10"

		message = ["00", COMMAND_LIGHT, val]
		self.send(message)
		self.LED = light
		
	def send(self,data):
		if self.status != "Connected" :
			return
		data[0] = "52"
		senddata = b""
		for byte in data:
			byte = str(byte)
			senddata += bytes.fromhex(byte)
			a = self.controlsocket.send(senddata)
	
	def calibrate(self):
		message = ["00", COMMAND_READ_REGISTER ,"04", "A4", "00", "24", "00", "18"]
		done = False
		while not done : 
			self.send(message)
			data = self.receivesocket.recv(25)
			if(data[1] == 33):
				data2 = self.receivesocket.recv(25)
				data = data[7:24]
				data2 = data2[7:15]
				data = data + data2
				i = 0
				for k in range(0,len(data),2):
					self.calibration.append((data[k] << 8) + data[k+1])
					i+=1
				done = True
			

	def receivethread(self):
		self.calibrate()
		while self.status == "Connected":
			try : 
				message = ["00", COMMAND_READ_REGISTER, "04", "A4", "00", "00", "00", "08"]
				self.send(message)
				data = self.receivesocket.recv(25)
				if(data[1]==33):
					self.lastEvent = self.createBoardEvent(data[2:15])
					pygame.event.post(pygame.event.Event(WIIBOARD_MASS, mass=self.lastEvent))
			except : 
				pass
		
	def createBoardEvent(self, bytes):
		buttonBytes = bytes[0:2]
		bytes = bytes[5:13]
		buttonPressed = False
		buttonReleased = False
		state = (buttonBytes[0] << 8) | buttonBytes[1]

		if state == BUTTON_DOWN_MASK:
			buttonPressed = True
			if not self.buttonDown:
				pygame.event.post(pygame.event.Event(WIIBOARD_BUTTON_PRESS))
				self.buttonDown = True

		if buttonPressed == False:
			if self.lastEvent.buttonPressed == True:
				buttonReleased = True
				self.buttonDown = False
				pygame.event.post(pygame.event.Event(WIIBOARD_BUTTON_RELEASE))

		rawTR = (bytes[0] << 8) + bytes[1]
		rawBR = (bytes[2] << 8) + bytes[3]
		rawTL = (bytes[4] << 8) + bytes[5]
		rawBL = (bytes[6] << 8) + bytes[7]

		topRight = self.calcMass(rawTR,0)
		bottomRight = self.calcMass(rawBR,1)
		topLeft = self.calcMass(rawTL,2)
		bottomLeft = self.calcMass(rawBL,3)

		boardEvent = BoardEvent(topLeft,topRight,bottomLeft,bottomRight,buttonPressed,buttonReleased)
		return boardEvent

	def calcMass(self, raw, pos):
		val = 0.0
		
		if raw < self.calibration[pos]:
			return val
		elif raw < self.calibration[pos+4]:
			val = 17 * ((raw - self.calibration[pos]) / float((self.calibration[pos+4] - self.calibration[pos])))
		elif raw > self.calibration[pos+4]:
			val = 17 + 17 * ((raw - self.calibration[pos+4]) / float((self.calibration[pos+8] - self.calibration[pos+4])))

		return val


		


				
		
'''image = pygame.image.load("Menu.jpg")
		image = pygame.transform.scale(image, (w,h))
		self.screen.blit(image,(0,0))
		pygame.display.flip()'''
	


			
				
			
			
				

	