'''
menu.py
Menu class
Memory
Szymon Sudak
'''
import pygame
import sys
from preview import Preview
from button import Button

THEME_COLOURS = (
    (25, 25, 30),
    (25, 25, 30),
    (25, 25, 40),
    (40, 30, 25),
)

class Menu:
    '''
    Menu class, handles all menu operations and rendering.
    '''
    def __init__(self, window, framerate):

        BUTTON_PADDING = window.get_height() / 8
        BUTTON_HEIGHT = BUTTON_PADDING * 0.8
        BUTTON_WIDTH = window.get_width() / 3
        FONT_SIZE = (BUTTON_HEIGHT * 3) // 4

        start_args = {
            "width": BUTTON_WIDTH,
            "height": BUTTON_HEIGHT,
            "text": "Start",
            "size": int(FONT_SIZE),
            "pos": window.get_rect().center
        }
        self.start_button = Button(start_args)

        difficulty_args = start_args
        difficulty_args["text"] = "Difficulty"
        difficulty_args["pos"] = (window.get_rect().centerx,
                                  window.get_rect().centery+BUTTON_PADDING)
        self.difficulty_button = Button(difficulty_args)

        theme_args = start_args
        theme_args["text"] = "Theme"
        theme_args["pos"] = (window.get_rect().centerx,
                             window.get_rect().centery+2*BUTTON_PADDING)
        self.theme_button = Button(theme_args)

        exit_args = start_args
        exit_args["text"] = "Exit"
        exit_args["pos"] = (window.get_rect().centerx,
                            window.get_rect().centery+3*BUTTON_PADDING)
        self.exit_button = Button(exit_args)

        self.difficulty = 0
        self.theme = 0
        self.window = window
        self.framerate = framerate

    def blit(self, window):
        window.fill(THEME_COLOURS[self.theme])
        self.start_button.draw(window)
        self.difficulty_button.draw(window)
        self.theme_button.draw(window)
        self.exit_button.draw(window)

    def process(self, mouse_pos, mouse_pressed):
        '''
        Process the menu data.
        '''
        self.start_button.process(mouse_pos, mouse_pressed)
        self.difficulty_button.process(mouse_pos, mouse_pressed)
        self.exit_button.process(mouse_pos, mouse_pressed)
        self.theme_button.process(mouse_pos, mouse_pressed)

    def run(self):
        self.process((0, 0), False)

        COEF = self.window.get_height() // 60 * 0.3
        PLAYFIELD = pygame.Rect(0, 0, self.window.get_width() / 4, 0)
        PLAYFIELD.height = PLAYFIELD.width * 3 / 4
        PLAYFIELD.centerx = self.window.get_rect().centerx
        PLAYFIELD.centery = self.window.get_rect().centery/2
        args = {
            "playfield": PLAYFIELD,
            "width": (self.difficulty+2) * 2,
            "height": (self.difficulty+2),
            "theme": self.theme
        }

        preview = Preview(args)

        fpsClock = pygame.time.Clock()
        held = False

        while not self.start_button.is_pressed:
            mouse_pressed = False
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if pygame.mouse.get_pressed()[0] and not held:
                mouse_pressed = True
                held = True

            if not pygame.mouse.get_pressed()[0]:
                held = False

            if self.exit_button.is_pressed:
                pygame.quit()
                sys.exit()

            if self.difficulty_button.is_pressed:
                self.difficulty += 1
                self.difficulty %= 3
                args["width"] = (self.difficulty+2) * 2
                args["height"] = (self.difficulty+2)
                preview = Preview(args)

            if self.theme_button.is_pressed:
                self.theme += 1
                self.theme %= 4
                args["theme"] = self.theme
                preview = Preview(args)

            self.process(mouse_pos, mouse_pressed)
            self.blit(self.window)
            preview.blit(self.window)

            pygame.display.flip()
            fpsClock.tick(self.framerate)

        args["color"] = THEME_COLOURS[self.theme]
        return args
