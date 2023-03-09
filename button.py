'''
button.py
Contains button class
Memory
Szymon Sudak
'''
import pygame

WHITE = (255, 255, 255)
FONT_FILE = "assets/mago3.ttf"


class Button:
    '''
    Button class.
    '''
    def __init__(self, args: dict):
        self.width = args["width"]
        self.height = args["height"]
        self.text = args["text"]
        self.size = args["size"]
        self.pos = args["pos"]
        self.is_pressed = False

        my_font = pygame.font.Font(FONT_FILE, self.size)
        text_surface = my_font.render(self.text, False, WHITE)
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, WHITE, (0, 0, self.width, self.height),
                         2, 2)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.image.blit(text_surface,
                        ((self.width-text_surface.get_rect().width)/2,
                         (self.height-text_surface.get_rect().height)/2))

        self.image.set_alpha(115)

        self.light = pygame.Surface((self.width, self.height))
        self.light.fill(WHITE)
        self.alpha = 10
        self.light.set_alpha(self.alpha)

    def process(self, mouse_pos, is_pressed):
        '''
        Process the button data.
        '''
        
        hover = self.rect.collidepoint(mouse_pos)
        if not hover:
            if self.alpha > 10:
                self.alpha -= 1
            self.is_pressed = False
        else:
            if is_pressed:
                self.alpha = 100
                self.is_pressed = True
            else:
                self.alpha = 30
                self.is_pressed = False

        self.light.set_alpha(self.alpha)

    def draw(self, surf):
        surf.blit(self.light, self.rect)
        surf.blit(self.image, self.rect)
