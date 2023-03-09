'''
screens.py
Win screen class
Memory
Szymon Sudak
'''
import pygame

GREEN = (50, 200, 10)
WHITE = (255, 255, 255)
BACKGROUND = (0, 0, 0, 150)
FONT_FILE = "assets/mago3.ttf"


class WinScreen:
    '''
    Win screen class.
    '''

    def __init__(self, window, time):
        '''
        Initializer.
        '''
        self.surf = pygame.Surface(window.get_rect().size, pygame.SRCALPHA)
        self.rect = window.get_rect()
        self.surf.fill(BACKGROUND)

        SIZE = window.get_rect().height

        self.font1 = pygame.font.Font(FONT_FILE, int(SIZE/5))
        self.font2 = pygame.font.Font(FONT_FILE, int(SIZE/10))

        self.text1 = self.font1.render("Well done!", False, GREEN)
        self.text2 = self.font2.render("your time was:", False, WHITE)

        minutes = int(time // 60)
        seconds = int(time) % 60
        decyseconds = (int(time*100)) % 100
        time_text = (f'{minutes:02d}' + ':' +
                     f'{seconds:02d}' + ':' + f'{decyseconds:02d}')
        self.text3 = self.font2.render(time_text, False, WHITE)

        centerx = self.surf.get_rect().centerx
        centery = self.surf.get_rect().centery

        rect1 = self.text1.get_rect()
        rect1.centerx = centerx
        rect1.centery = centery/2
        rect2 = self.text2.get_rect()
        rect2.centerx = centerx
        rect2.centery = centery
        rect3 = self.text3.get_rect()
        rect3.centerx = centerx
        rect3.centery = centery*1.2

        self.surf.blit(self.text1, rect1)
        self.surf.blit(self.text2, rect2)
        self.surf.blit(self.text3, rect3)

    def blit(self, surf):
        '''
        Blit method.
        '''
        surf.blit(self.surf, self.rect)
