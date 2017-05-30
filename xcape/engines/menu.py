import pygame as pg
import xcape.components.menus as menus
import xcape.common.events as events


class MenuEngine:

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.nameToMenu = \
            {
                "blank": menus.BlankMenu,
                "splash": None
            }

        self.menu = menus.BlankMenu(self.screen)

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


