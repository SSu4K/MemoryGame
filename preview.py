'''
game.py
Contains game logic and gameplay features
Memory
Szymon Sudak
'''
import pygame
import random
from tile import Tile, sigmoid

TILE_PADDING = 0.9

THEMES = (
    "assets/deck_classic_light_2color_0.png",
    "assets/deck_classic_light_4color_1.png",
    "assets/deck_classic_dark_2color_0.png",
    "assets/deck_classic_sepia_2color_0.png"
)


def smooth_pos(pos1, pos2, t):
    '''
    Returns smooth position between points
    for a parameter t, using sigmoid fuction
    '''
    x1, y1 = pos1
    x2, y2 = pos2
    new_x = x1 + sigmoid(t) * (x2-x1)
    new_y = y1 + sigmoid(t) * (y2-y1)
    return (new_x, new_y)


def tiles_init(width, height, playfield: pygame.Rect, cards):
    '''
    Initialize tiles.
    '''
    tile_list = []
    spacing_x = playfield.width / width
    spacing_y = playfield.height / height
    tile_scale = (spacing_x*TILE_PADDING, spacing_y*TILE_PADDING)

    for y in range(height):
        for x in range(width):
            pos_x = playfield.left + x * spacing_x + spacing_x / 2
            pos_y = playfield.top + y * spacing_y + spacing_y / 2
            tile_list.append(Tile(pos_x, pos_y, random.randrange(52),
                                  tile_scale, cards))
            tile_list[len(tile_list)-1].flip()

    return tile_list


class Preview:
    '''
    Game class.
    Handles all of the gameplay features.
    '''
    def __init__(self, args: dict):
        self.playfield = args["playfield"]
        self.width = args["width"]
        self.height = args["height"]
        self.cards = pygame.image.load(THEMES[args["theme"]])
        self.tile_list = tiles_init(self.width, self.height,
                                    self.playfield, self.cards)

    def blit(self, window: pygame.Surface):
        for tile in self.tile_list:
            if random.randrange(100) == 0:
                if not tile.is_flipped:
                    tile.load(random.randrange(52), tile.scale)
                tile.flip()

            tile.draw(window)
