'''
tile.py
Tile class
Memory
Szymon Sudak
'''
import pygame
import math

FLIP_SPEED = 1/6
TILE_SIZE = (40, 60)
PADDING = (24, 4)
SHIFT = (12, 2)
SYMBOLS_FORMAT = (13, 4)


def sigmoid(x):
    '''
    Sigmoid function.
    '''
    return 1/(1+math.exp(-15*(x-0.5)))


def get_symbol_region(id):
    '''
    Get right symbol texture.
    '''
    sizex = TILE_SIZE[0] + PADDING[0]
    sizey = TILE_SIZE[1] + PADDING[1]
    start = (SHIFT[0] + id % SYMBOLS_FORMAT[0] * sizex,
             SHIFT[1] + id // SYMBOLS_FORMAT[0] * sizey)
    return (start[0], start[1], TILE_SIZE[0], TILE_SIZE[1])


class Tile:
    '''
    Tile class.
    Handles the apperence and behavior
    of the memory tiles.
    '''
    def __init__(self, x, y, symbol, scale: list, symbols):
        '''
        Initializer.
        '''
        self.is_flipped = False
        self.is_removed = False
        self.is_flipping = False
        self.symbol = symbol
        self.scale = scale
        self.pos = (x, y)
        self.symbols = symbols
        self.load(symbol, scale)

    def load(self, symbol, scale: list):
        '''
        Load images.
        '''
        self.orginal_reverse = pygame.Surface(TILE_SIZE)
        self.orginal_reverse.blit(self.symbols, (0, 0),
                                  (844, 194, TILE_SIZE[0], TILE_SIZE[1]))
        self.orginal_obverse = pygame.Surface(TILE_SIZE)
        self.orginal_obverse.blit(self.symbols, (0, 0),
                                  get_symbol_region(symbol))

        self.reload(scale)

    def reload(self, scale):
        self.reverse = pygame.transform.scale(self.orginal_reverse, scale)
        self.obverse = pygame.transform.scale(self.orginal_obverse, scale)
        self.obverse.set_alpha(255)
        self.rect = self.reverse.get_rect()
        self.rect.center = self.pos

    def set_alpha(self, alpha):
        '''
        Set tiles alpha value
        '''
        self.obverse.set_alpha(alpha)
        self.reverse.set_alpha(alpha)

    def flip_animation(self):
        '''
        Flipping animation
        '''
        if self.angle < 2*math.pi:
            self.reload((self.scale[0]*(math.cos(self.angle)+1)/2,
                         self.scale[1]))
            if self.angle < math.pi:
                self.angle += FLIP_SPEED
                if self.angle >= math.pi:
                    self.is_flipped = not self.is_flipped
            else:
                self.angle += FLIP_SPEED

        else:
            self.is_flipping = False

    def draw(self, window: pygame.Surface):
        '''
        Draw the object.
        '''

        if self.is_removed:
            alpha = self.obverse.get_alpha()
            if alpha > 50:
                self.set_alpha(alpha-10)

        if self.is_flipping:
            self.flip_animation()
        if self.is_flipped:
            window.blit(self.obverse, self.rect)
        else:
            window.blit(self.reverse, self.rect)

    def flip(self):
        '''
        Flip the tile.
        '''
        if self.is_flipping:
            return
        self.angle = 0.0
        self.is_flipping = True

    def try_flip(self, mouse_pos):
        '''
        Try to flip the tile.
        '''
        if self.is_flipping or self.is_flipped:
            return False
        if not self.is_removed and self.rect.collidepoint(mouse_pos):
            self.flip()
            return True
        return False

    def remove(self):
        '''
        Remove tile.
        '''
        self.is_removed = True
