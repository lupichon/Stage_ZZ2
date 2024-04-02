import my_wiiboard
import pygame
import time
import matplotlib

FACTOR = 20

def main():
	board = my_wiiboard.Wiiboard()
	pygame.init()
	
	address = board.discover()
	board.connect(address) 

	board.setLight(True)
	running = True

	window_size = (1000, 1000)
	screen = pygame.display.set_mode(window_size)
	pygame.display.set_caption("Center of Mass")
	RED = (255, 0, 0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)

	rect_width = FACTOR * my_wiiboard.L 
	rect_height = FACTOR * my_wiiboard.W

	center_x = window_size[0] // 2
	center_y = window_size[1] // 2
	rect_x = center_x - rect_width // 2
	rect_y = center_y - rect_height // 2

	#image = pygame.image.load('image_219.jpg') 
	#image = pygame.transform.scale(image, (rect_width, rect_height))

	while(running and board.status == "Connected"):
		for event in pygame.event.get():
			if event.type == my_wiiboard.WIIBOARD_MASS:
				#print ("Total weight: " + str(event.mass.totalWeight) + ". Top left: " + str(event.mass.topLeft) + ". Bottom left: " + str(event.mass.bottomLeft) + ". Top right: " + str(event.mass.topRight) + ". Bottom right: " + str(event.mass.bottomRight))
				#print("x : " + str(event.mass.CoMx) + " y : " + str(event.mass.CoMy))
				screen.fill((255, 255, 255))
				#screen.blit(image, (rect_x, rect_y))  
				pygame.draw.rect(screen, BLUE, (rect_x, rect_y, rect_width, rect_height),1)
				pygame.draw.circle(screen, GREEN, (center_x - rect_width // 4,center_y),8)
				if(event.mass.totalWeight > 5):
					pygame.draw.circle(screen, RED, (center_x + FACTOR * event.mass.CoMx,center_y - FACTOR * event.mass.CoMy),8)
				else:
					pygame.draw.circle(screen, RED, (center_x,center_y),8)
				pygame.display.flip()
					

			elif event.type == my_wiiboard.WIIBOARD_BUTTON_PRESS:
				print("Button pressed!")

			elif event.type == my_wiiboard.WIIBOARD_BUTTON_RELEASE:
				print("Button released")
			
			elif event.type == pygame.QUIT:
				running = False
			
	board.disconnect()
	pygame.quit()
	print("end")

if __name__ == "__main__":
	main()

