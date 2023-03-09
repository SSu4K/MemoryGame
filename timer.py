'''
timer.py
Contains timer class
Memory
Szymon Sudak
'''
import pygame

WHITE = (255, 255, 255)
FONT_FILE = "assets/mago3.ttf"


class Timer:
    '''
    Timer class.
    '''
    def __init__(self, font_size, pos):
        self.clock = pygame.time.Clock()
        self.size = font_size
        self.my_font = pygame.font.Font(FONT_FILE, self.size)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.time = 0
        self.text = "00:00:00"
        self.pos = pos
        self.update()
        self.rect.center = self.pos

    def reset(self):
        self.time = 0

    def add(self, miliseconds):
        self.time += miliseconds
        self.update()

    def update(self):
        minutes = int(self.time // 60)
        seconds = int(self.time) % 60
        decyseconds = (int(self.time*100)) % 100
        self.text = (f'{minutes:02d}' + ':' +
                     f'{seconds:02d}' + ':' + f'{decyseconds:02d}')
        self.text_surface = self.my_font.render(self.text, False, WHITE)
        self.rect.size = self.text_surface.get_rect().size

    def blit(self, surf):
        surf.blit(self.text_surface, self.rect)
