"""
The menu engine of the game.
"""

import pygame as pg
from xcape.common.gameobject import GameObject
import xcape.components.menus as menus
import xcape.common.events as events


class MenuEngine(GameObject):
    """
    Responsibilities:
        - Displaying and updating the current menu.
        - Transitioning between menus.
    """

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: Renderer object, containing loaded images.
        """
        self.screen = screen
        self.resources = resources

        self.menu = menus.SplashMenu(self.screen)
        self.nameToMenu = \
            {
                "blank": menus.BlankMenu,
                "splash": None
            }


    def handleEvent(self, event):
        """
        :param event: pygame.Event, allowing event-driven programming.
        """
        if event.type == events.MENU_EVENT:
            if event.category == "transition":
                self.menu = self.nameToMenu[event.data](self.screen)

    def update(self):
        self.menu.update()

    def draw(self):
        self.menu.draw()
