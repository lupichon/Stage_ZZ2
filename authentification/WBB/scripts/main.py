import WBB.scripts.wiiboard as wiiboard
import pygame
import time

board = wiiboard.Wiiboard()

x = 0
y = 0

find = True

def main():
	global x, y, find
	pygame.init()

	address = board.discover()
	if address is not None : 
		board.connect(address) 
		board.setLight(True)
		running = True
	else : 
		running = False
		find = False
	
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

			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				board.disconnect()
				break
	pygame.quit()
	
if __name__ == "__main__":
	main()