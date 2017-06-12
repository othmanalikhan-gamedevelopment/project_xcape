"""
The menu engine of the game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.components.menus as menus
from xcape.common.object import GameObject


class MenuEngine(GameObject):
    """
    Responsibilities:
        - Displaying and updating the current menu.
        - Transitioning between menus.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        super().__init__()
        self.screen = screen

        self.menu = None
        self.nameToMenu = \
            {
                "blank_menu": None,
                "splash_menu": menus.SplashMenu,
                "main_menu": menus.MainMenu,
                "options_menu": menus.OptionsMenu,
                "game_over_menu": menus.GameOverMenu,
                "pause_menu": menus.PauseMenu,
                "solo_ui_menu": menus.SoloUIMenu
            }

    def handleEvent(self, event):
        if self.menu:
            self.menu.handleEvent(event)

        if event.type == events.MENU_EVENT:
            if event.category == "transition":
                try:
                    menu = self.nameToMenu[event.data]
                    self.menu = menu(self.screen)
                except TypeError:
                    self.menu = menu

            if event.category == "screen":
                self.screen = pg.display.get_surface()

    def update(self):
        if self.menu:
            self.menu.update()

    def draw(self):
        if self.menu:
            self.menu.draw()
