"""
The menu engine of the game.
"""

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
                "ui_menu": menus.UIMenu
            }

    def handleEvent(self, event):
        if self.menu:
            self.menu.handleEvent(event)

        if event.type == events.MENU_EVENT:
            if event.category == "transition":
                menu = self.nameToMenu[event.data]
                if menu:
                    self.menu = menu(self.screen)

    def update(self):
        if self.menu:
            self.menu.update()

    def draw(self):
        if self.menu:
            self.menu.draw()
