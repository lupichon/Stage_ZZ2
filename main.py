import modules
import pygame
import time
import matplotlib

def main():
	board = modules.Wiiboard()
	pygame.init()

	graph = modules.graph(1000,1000,"Center of Gravity")
	
	address = board.discover()
	board.connect(address) 

	running = True

	while(running and board.status == "Connected"):
		for event in pygame.event.get():
			if event.type == modules.WIIBOARD_MASS:
				#print ("Total weight: " + str(event.mass.totalWeight) + ". Top left: " + str(event.mass.topLeft) + ". Bottom left: " + str(event.mass.bottomLeft) + ". Top right: " + str(event.mass.topRight) + ". Bottom right: " + str(event.mass.bottomRight))
				#print("x : " + str(event.mass.CoMx) + " y : " + str(event.mass.CoMy))
				graph.display(event)
			
			elif event.type == modules.WIIBOARD_BUTTON_PRESS:
				print("Button pressed!")

			elif event.type == modules.WIIBOARD_BUTTON_RELEASE:
				print("Button released")
			
			elif event.type == pygame.QUIT:
				running = False

			elif event.type == modules.WIIBOARD_CONNECTED:
				board.setLight(True)

			elif event.type == modules.WIIBOARD_DISCONNECTED:
				board.setLight(False)
			
	board.disconnect()
	pygame.quit()
	print("end")

if __name__ == "__main__":
	main()

