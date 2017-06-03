"""
The menu engine of the game.
"""

import xcape.common.events as events
import xcape.common.loader as loader
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
        self.resources = loader.loadContent(loader.MENUS_PATH)

        self.menu = menus.UIMenu(self.screen, self.resources)
        self.menu.setLives(3)
        self.nameToMenu = \
            {
                "blank_menu": menus.BlankMenu,
                "splash_menu": menus.SplashMenu,
                "main_menu": menus.MainMenu,
                "options_menu": menus.OptionsMenu,
                "game_over_menu": menus.GameOverMenu,
                "pause_menu": menus.PauseMenu,
                "ui_menu": menus.UIMenu
            }

    def handleEvent(self, event):
        self.menu.handleEvent(event)

        if event.type == events.MENU_EVENT:
            if event.category == "transition":
                menu = self.nameToMenu[event.data]
                self.menu = menu(self.screen, self.resources)

    def update(self):
        self.menu.update()

    def draw(self):
        self.menu.draw()
