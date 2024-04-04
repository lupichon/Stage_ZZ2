import wiiboard
import window
import pygame
import time

def main():
	board = wiiboard.Wiiboard()
	pygame.init()

	graph = window.graph(1000,1000,"Center of Gravity")
	
	address = board.discover()
	board.connect(address) 

	running = True
	while (running):
		graph.display_menu_screen()
		for event in pygame.event.get() : 
			if event.type == pygame.MOUSEBUTTONDOWN:
				if graph.button_rect.collidepoint(pygame.mouse.get_pos()):
					running = False

			elif event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:  
					try:
						number = int(graph.input_text)  
						print("Nombre entré :", number)
					except ValueError:
						print("Erreur : entrée invalide")
				elif event.key == pygame.K_BACKSPACE:  
					graph.input_text = graph.input_text[:-1] 
				else:
					graph.input_text += event.unicode

			elif event.type == wiiboard.WIIBOARD_CONNECTED:
				board.setLight(True)

			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				board.setLight(False)


		# Rafraîchir l'affichage
		pygame.display.flip()

	
	running = True

	while(running and board.status == "Connected"):
		for event in pygame.event.get():
			if event.type == wiiboard.WIIBOARD_MASS:
				graph.display_main_screen(event.mass)
			
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

