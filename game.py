'''
game.py
Contains game logic and gameplay features.
Memory
Szymon Sudak
'''
import pygame
import random
from tile import Tile, sigmoid
from button import Button
from timer import Timer
from screens import WinScreen

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
    symbol_list = [*range(52)]
    random.shuffle(symbol_list)
    symbol_list = symbol_list[:width*height//2]
    symbol_list += symbol_list
    random.shuffle(symbol_list)
    random.shuffle(symbol_list)

    for y in range(height):
        for x in range(width):
            symbol = symbol_list[len(tile_list)]
            pos_x = playfield.left + x * spacing_x + spacing_x / 2
            pos_y = playfield.top + y * spacing_y + spacing_y / 2
            tile_list.append(Tile(pos_x, pos_y, symbol, tile_scale, cards))

    return tile_list


class Game:
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
        self.flipped_list = []
        self.is_win = False
        self.removed = 0

    def spread_tiles(self, t, delay):
        shift = 0
        for tile in self.tile_list:
            tile.rect.center = smooth_pos(self.playfield.topleft,
                                          tile.pos, t+shift)
            shift += delay

    def set_alpha(self, alpha):
            '''
            Set alpha value of tiles
            '''
            for tile in self.tile_list:
                tile.set_alpha(alpha)

    def process(self, mouse_pos, mouse_pressed):
        if self.is_win:
            return

        for tile in self.tile_list:
            if mouse_pressed and len(self.flipped_list) < 2:
                if tile.try_flip(mouse_pos):
                    self.flipped_list.append(tile)

        if (
            len(self.flipped_list) == 2
            and not self.flipped_list[0].is_flipping
            and not self.flipped_list[1].is_flipping
           ):
            if self.flipped_list[0].symbol == self.flipped_list[1].symbol:
                for tile in self.flipped_list:
                    tile.remove()
                    self.removed += 1
            else:
                for tile in self.flipped_list:
                    tile.flip()
            self.flipped_list.clear()

        if self.removed >= self.width * self.height:
            self.is_win = True

    def blit(self, window: pygame.Surface):
        for tile in self.tile_list:
            tile.draw(window)


def run_game(window, game, bg_col, framerate):
    BUTTON_SIZE = window.get_width() * 0.05
    button_args = {
        "width": 2*BUTTON_SIZE,
        "height": BUTTON_SIZE,
        "text": "Menu",
        "size": int(BUTTON_SIZE * 0.6),
        "pos": (0, 0)
    }
    menu_button = Button(button_args)
    menu_button.rect.topright = window.get_rect().topright
    fpsClock = pygame.time.Clock()
    center = window.get_rect().center
    timer = Timer(int(BUTTON_SIZE*2), (center[0], center[1]/7))

    STEPS = 100
    for i in range(STEPS):
        game.spread_tiles(i/STEPS, 1/STEPS)
        window.fill(bg_col)
        game.blit(window)

        pygame.display.flip()
        fpsClock.tick(framerate)

    held = False
    run = True
    # Main loop
    while run:
        mouse_pressed = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if pygame.mouse.get_pressed()[0] and not held:
            mouse_pressed = True
            held = True

        if not pygame.mouse.get_pressed()[0]:
            held = False

        if game.is_win:
            run = False

        if menu_button.is_pressed:
            run = False

        game.process(mouse_pos, mouse_pressed)
        window.fill(bg_col)
        game.blit(window)
        menu_button.draw(window)
        timer.blit(window)
        menu_button.process(mouse_pos, mouse_pressed)

        pygame.display.flip()
        fpsClock.tick(framerate)
        timer.add(1/framerate)

    if not game.is_win:
        return

    win_screen = WinScreen(window, timer.time)
    pos1 = (0, win_screen.rect.height)
    pos2 = (0, 0)

    STEPS = 100
    for i in range(STEPS):
        game.spread_tiles((STEPS - i)/STEPS, 1/STEPS)
        win_screen.rect.topleft = smooth_pos(pos1, pos2, i/STEPS)
        game.set_alpha((1-sigmoid(i/STEPS))*50)

        window.fill(bg_col)
        game.blit(window)
        win_screen.blit(window)
        pygame.display.flip()
        fpsClock.tick(framerate)

    window.fill(bg_col)
    win_screen.blit(window)
    pygame.display.flip()

    fpsClock.tick(framerate/200)
