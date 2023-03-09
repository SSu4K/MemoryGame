'''
main.py
Main game file
Memory
Szymon Sudak
'''

import pygame
from game import Game, run_game
from menu import Menu

BACKGROUND_COLOR = (25, 25, 25)
RED = (200, 50, 100)
FRAMERATE = 60

WINDOW = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
COEF = WINDOW.get_height() // 60 * 0.6
PLAYFIELD = pygame.Rect(0, 0, 40*2*COEF, 60*COEF)
PLAYFIELD.center = WINDOW.get_rect().center


def main():
    '''
    Contains main game loop
    '''
    pygame.init()
    menu = Menu(WINDOW, FRAMERATE)

    while True:
        args = menu.run()
        args["playfield"] = PLAYFIELD
        game = Game(args)
        run_game(WINDOW, game, args["color"], FRAMERATE)


if __name__ == "__main__":
    main()
