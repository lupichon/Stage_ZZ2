import pygame

#dimensions of the WBB
L = 43			
W = 24.5

class graph:
	
	RED = (255, 0, 0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)
	BLACK = (0,0,0)
	FACTOR = 20
	screen = None
	center_x = 0
	center_y = 0
	rect_x = 0
	rect_y = 0
	rect_height = 0
	rect_width = 0
	font = None
	button_rect = None
	input_rect = None
	input_text = ''


	def __init__(self,w,h,title):
		window_size = (w,h)
		self.screen = pygame.display.set_mode(window_size)
		pygame.display.set_caption(title)

		self.rect_width = self.FACTOR * L 
		self.rect_height = self.FACTOR * W

		self.center_x = window_size[0] // 2
		self.center_y = window_size[1] // 2
		self.rect_x = self.center_x - self.rect_width // 2
		self.rect_y = self.center_y - self.rect_height // 2

		self.font = pygame.font.Font(None, 36)

	def texteField(self,x,y):
		self.input_rect = pygame.Rect(x,y , 100, 50)
		input_color = (155,155,155)
		text_color = (0,0,0)

		pygame.draw.rect(self.screen, input_color, self.input_rect)
		text_surface = self.font.render(self.input_text, True, text_color)
		self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

	def button(self):
		self.screen.fill((255, 255, 255))
		self.button_rect = pygame.Rect(150, 100, 100, 50)
		button_color = (150,150,150)
		hover_color = (255,255,255)
		text_color = (0,0,0)
		text = self.font.render("Validate", True, text_color)

		if self.button_rect.collidepoint(pygame.mouse.get_pos()):
			button_color = hover_color
		else:
			button_color = (155,155,155)
		pygame.draw.rect(self.screen, button_color, self.button_rect)
		self.screen.blit(text, (self.button_rect.centerx - text.get_width() // 2, self.button_rect.centery - text.get_height() // 2))
	
	def getLength():
		a=1
	
	def getWidth():
		a=1

	def display_menu_screen(self):
		self.button()
		self.texteField(200,200)

	def display_main_screen(self,mass):
		self.screen.fill((255, 255, 255))
		pygame.draw.rect(self.screen, self.BLUE, (self.rect_x, self.rect_y, self.rect_width, self.rect_height),1)
		pygame.draw.circle(self.screen,self.GREEN, (self.center_x - self.rect_width // 4,self.center_y),8)

		text_surface = self.font.render("weight = " + str(round(mass.totalWeight,2)), True, self.BLACK)
		self.screen.blit(text_surface, (100,100))
		try : 
			text_surface = self.font.render("x = " + str(round(mass.CoMx,2)) + " y = " + str(round(mass.CoMy,2)), True, self.BLACK)
			self.screen.blit(text_surface, (100,200))
		except : 
			pass

		try : 
			pygame.draw.circle(self.screen, self.RED, (self.center_x + self.FACTOR * mass.CoMx,self.center_y - self.FACTOR * mass.CoMy),8)
		except:
			pygame.draw.circle(self.screen, self.RED, (self.center_x,self.center_y),8)
			
    
			