"""
The menu engine of the game.
"""

import pygame as pg
from xcape.common.gameobject import GameObject
import xcape.components.menus as menus
import xcape.common.events as events
import xcape.common.renderer as renderer


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
        self.screen = screen
        self.resources = renderer.loadMenus()

        self.menu = menus.SplashMenu(self.screen, self.resources)
        self.nameToMenu = \
            {
                "blank_menu": menus.BlankMenu,
                "splash_menu": menus.SplashMenu,
                "main_menu": None
            }

    def handleEvent(self, event):
        """
        :param event: pygame.Event, allowing event-driven programming.
        """
        if event.type == events.MENU_EVENT:
            if event.category == "transition":
                self.menu = self.nameToMenu[event.data](self.screen, self.resources)

    def update(self):
        self.menu.update()

    def draw(self):
        self.menu.draw()
