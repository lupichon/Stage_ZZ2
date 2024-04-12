import pygame
import wiiboard

# L=43
# W=24.5

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FACTOR = 20

font = None

size_buttonW = 100
size_buttonL = 50

add_text = []


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class graph:

    screen = None
    center_x = 0
    center_y = 0
    rect_x = 0
    rect_y = 0
    rect_height = 0
    rect_width = 0

    button1 = None
    button2 = None

    window_size = None

    input_rect1 = None
    input_text1 = ""
    input_rect2 = None
    input_text2 = ""

    def __init__(self, w, h, title):
        self.window_size = (w, h)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(title)

    def getDimensions(self):
        self.rect_width = FACTOR * 40  # L
        self.rect_height = FACTOR * 20  # W

        self.center_x = self.window_size[0] // 2
        self.center_y = self.window_size[1] // 2
        self.rect_x = self.center_x - self.rect_width // 2
        self.rect_y = self.center_y - self.rect_height // 2

    def texteField(self, x, y, screen, input_text):
        input_rect = pygame.Rect(x, y, size_buttonW, size_buttonL)
        input_color = (155, 155, 155)
        pygame.draw.rect(screen, input_color, input_rect)
        text_surface = font.render(input_text, True, BLACK)
        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        return input_rect

    # (255, 127, 80)
    def button(self, x, y, txt):
        button = pygame.Rect(x, y, size_buttonW, size_buttonL)
        button_color = RED
        hover_color = BLUE
        text = font.render(txt, True, BLACK)

        if button.collidepoint(pygame.mouse.get_pos()) and wiiboard.board.status == "Disconnected":
            button_color = hover_color

        pygame.draw.rect(self.screen, button_color, button)
        self.screen.blit(text, (button.centerx - text.get_width() // 2, button.centery - text.get_height() // 2))
        return button

    def display_menu_screen(self):
        self.screen.fill((52, 78, 91))

        self.button1 = self.button((self.window_size[0] - size_buttonW) // 2, 100, "Start")
        self.button2 = self.button(800, 800, "Validate")

        for t in add_text:
            self.displayText(t[0], BLACK, t[1], t[2])

        self.input_rect1 = self.texteField(200, 200, self.screen, self.input_text1)
        self.input_rect2 = self.texteField(200, 400, self.screen, self.input_text2)

        pygame.display.flip()

    def display_main_screen(self, mass):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, BLUE, (self.rect_x, self.rect_y, self.rect_width, self.rect_height), 1)

        text_surface = font.render("weight = " + str(round(mass.totalWeight, 2)), True, BLACK)
        self.screen.blit(text_surface, (100, 100))
        try:
            text_surface = font.render("x = " + str(round(mass.CoMx, 2)) + " y = " + str(round(mass.CoMy, 2)), True, BLACK)
            self.screen.blit(text_surface, (100, 200))
        except:
            pass

        try:
            pygame.draw.circle(self.screen, RED, (self.center_x + FACTOR * mass.CoMx, self.center_y - FACTOR * mass.CoMy), 8)
        except:
            pygame.draw.circle(self.screen, RED, (self.center_x, self.center_y), 8)

    def displayText(self, txt, Color, x, y):
        text_surface = font.render(txt, True, Color)
        self.screen.blit(text_surface, (x, y))


graph = graph(1000, 1000, "Center of Gravity")
