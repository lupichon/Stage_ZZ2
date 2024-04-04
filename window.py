import pygame

#L=43
#W=24.5

RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
FACTOR = 20
font = None

class graph:
	
	screen = None
	center_x = 0
	center_y = 0
	rect_x = 0
	rect_y = 0
	rect_height = 0
	rect_width = 0
	button_rect = None

	window_size = None

	input_rect1 = None
	input_text1 = ''
	input_rect2 = None
	input_text2 = ''

	def __init__(self,w,h,title):
		self.window_size = (w,h)
		self.screen = pygame.display.set_mode(self.window_size)
		pygame.display.set_caption(title)


	def getDimensions(self):
		print(self.input_text1)
		self.rect_width = FACTOR * float(self.input_text1) #L
		self.rect_height = FACTOR * float(self.input_text2)#W

		self.center_x = self.window_size[0] // 2
		self.center_y = self.window_size[1] // 2
		self.rect_x = self.center_x - self.rect_width // 2
		self.rect_y = self.center_y - self.rect_height // 2
		

	def texteField(self,x,y,screen,input_text):
		input_rect = pygame.Rect(x,y , 100, 50)
		input_color = (155,155,155)
		text_color = (0,0,0)
		pygame.draw.rect(screen, input_color, input_rect)
		text_surface = font.render(input_text, True, text_color)
		self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
		return input_rect

	def button(self):
		self.button_rect = pygame.Rect(150, 100, 100, 50)
		button_color = (150,150,150)
		hover_color = (255,255,255)
		text_color = (0,0,0)
		text = font.render("Validate", True, text_color)

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
		self.screen.fill((255, 255, 255))
		self.button()
		self.input_rect1 = self.texteField(200,200,self.screen,self.input_text1)
		self.input_rect2 = self.texteField(200,400,self.screen,self.input_text2)

	def display_main_screen(self,mass):
		self.screen.fill((255, 255, 255))
		pygame.draw.rect(self.screen, BLUE, (self.rect_x, self.rect_y, self.rect_width, self.rect_height),1)
		pygame.draw.circle(self.screen,GREEN, (self.center_x - self.rect_width // 4,self.center_y),8)

		text_surface = font.render("weight = " + str(round(mass.totalWeight,2)), True, BLACK)
		self.screen.blit(text_surface, (100,100))
		try : 
			text_surface = font.render("x = " + str(round(mass.CoMx,2)) + " y = " + str(round(mass.CoMy,2)), True, BLACK)
			self.screen.blit(text_surface, (100,200))
		except : 
			pass

		try : 
			pygame.draw.circle(self.screen, RED, (self.center_x + FACTOR * mass.CoMx,self.center_y - FACTOR * mass.CoMy),8)
		except:
			pygame.draw.circle(self.screen, RED, (self.center_x,self.center_y),8)
			
    

graph = graph(1000,1000,"Center of Gravity")