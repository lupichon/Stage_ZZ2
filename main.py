import wiiboard
import window
import pygame
import time

resume_img = pygame.image.load("images/button_resume.png").convert_alpha()
options_img = pygame.image.load("images/button_options.png").convert_alpha()
quit_img = pygame.image.load("images/button_quit.png").convert_alpha()
video_img = pygame.image.load('images/button_video.png').convert_alpha()
audio_img = pygame.image.load('images/button_audio.png').convert_alpha()
keys_img = pygame.image.load('images/button_keys.png').convert_alpha()
back_img = pygame.image.load('images/button_back.png').convert_alpha()

#create button instances
resume_button = window.Button(304, 125, resume_img, 1)
options_button = window.Button(297, 250, options_img, 1)
quit_button = window.Button(336, 375, quit_img, 1)
video_button = window.Button(226, 75, video_img, 1)
audio_button = window.Button(225, 200, audio_img, 1)
keys_button = window.Button(246, 325, keys_img, 1)
back_button = window.Button(332, 450, back_img, 1)

def main():
	
	pygame.init()
	window.font = pygame.font.SysFont("arialblack", 36)

	running = True
	menu = True
	select = 1
	while (running and menu):
		window.graph.display_menu_screen()
		for event in pygame.event.get() : 
			if event.type == pygame.MOUSEBUTTONDOWN:
				if window.graph.button1.collidepoint(pygame.mouse.get_pos()):
					address = wiiboard.board.discover()
					wiiboard.board.connect(address) 
				elif window.graph.button2.collidepoint(pygame.mouse.get_pos()):
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
				wiiboard.board.setLight(True)

			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				wiiboard.board.setLight(False)
		# Rafraîchir l'affichage
		pygame.display.flip()
		
	if(running):
		window.graph.getDimensions()
	while(running and wiiboard.board.status == "Connected"):
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
				wiiboard.board.setLight(True)

			elif event.type == wiiboard.WIIBOARD_DISCONNECTED:
				wiiboard.board.setLight(False)
			
		pygame.display.flip()

	wiiboard.board.disconnect()
	pygame.quit()
	print("end")

if __name__ == "__main__":
	main()

