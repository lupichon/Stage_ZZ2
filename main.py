import wiiboard
import window
import pygame
import time

def main():
	board = wiiboard.Wiiboard()
	pygame.init()
	window.font = pygame.font.Font(None, 36)
	
	address = board.discover()
	board.connect(address) 

	running = True
	menu = True
	select = 1
	while (running and menu):
		window.graph.display_menu_screen()
		for event in pygame.event.get() : 
			if event.type == pygame.MOUSEBUTTONDOWN:
				if window.graph.button_rect.collidepoint(pygame.mouse.get_pos()):
					menu = False
				elif window.graph.input_rect1.collidepoint(pygame.mouse.get_pos()):
					select = 1
				elif window.graph.input_rect2.collidepoint(pygame.mouse.get_pos()):
					select = 2

			elif event.type == pygame.QUIT:
				running = False
 
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_BACKSPACE: 
					if(select == 1): 
						window.graph.input_text1 = window.graph.input_text1[:-1] 
					elif(select == 2):
						window.graph.input_text2 = window.graph.input_text2[:-1]
				else:
					if(select == 1 and len(window.graph.input_text1)<4):
						window.graph.input_text1 += event.unicode
					elif(select == 2 and len(window.graph.input_text2)<4):
						window.graph.input_text2 += event.unicode

			elif event.type == wiiboard.WIIBOARD_CONNECTED:
				board.setLight(True)

			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				board.setLight(False)
		# Rafraîchir l'affichage
		pygame.display.flip()

	window.graph.getDimensions()
	while(running and board.status == "Connected"):
		for event in pygame.event.get():
			if event.type == wiiboard.WIIBOARD_MASS:
				window.graph.display_main_screen(event.mass)
			
			elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
				print("Button pressed!")

			elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
				print("Button released")
			
			elif event.type == pygame.QUIT:
				running = False

			elif event.type == wiiboard.WIIBOARD_CONNECTED:
				board.setLight(True)

			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				board.setLight(False)
			
		pygame.display.flip()

	board.disconnect()
	pygame.quit()
	print("end")

if __name__ == "__main__":
	main()

