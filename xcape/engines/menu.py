"""
The menu engine of the game.
"""

import pygame as pg

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
                "intro_menu": menus.IntroMenu,
                "main_menu": menus.MainMenu,
                "options_menu": menus.OptionsMenu,
                "lose_menu": menus.LoseMenu,
                "pause_menu": menus.PauseMenu,
                "solo_ui_menu": menus.SoloUIMenu,
                "coop_ui_menu": menus.CoopUIMenu,
                "win_menu": menus.WinMenu,
                "death_menu": menus.DeathMenu,
            }

    def handleEvent(self, event):
        if self.menu:
            self.menu.handleEvent(event)

        if event.type == self.MENU_EVENT:
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

    def draw(self, camera=None):
        if self.menu:
            self.menu.draw()
