import WBB.scripts.wiiboard as wiiboard
import pygame
import time

board = wiiboard.Wiiboard()

FACTOR = 20
x = 0
y = 0


def main():
	global x, y, topRight, bottomRight, topLeft, bottomLeft
	pygame.init()

	address = board.discover()
	board.connect(address) 
	board.setLight(True)
	running = True
	
	while(running and board.status == "Connected"):
		for event in pygame.event.get():
			if event.type == wiiboard.WIIBOARD_MASS:
				if event.type == wiiboard.WIIBOARD_MASS:
					x = event.mass.CoMx
					y = event.mass.CoMy
			elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
				print("Button pressed!")

			elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
				print("Button released")

			elif event.type == pygame.QUIT:
				running = False
			
	board.disconnect()
	pygame.quit()
	print("end")
if __name__ == "__main__":
	main()