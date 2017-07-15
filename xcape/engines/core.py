"""
The core engine of the game.
"""

import sys

import pygame as pg

import xcape.common.settings as settings

# PyGame needs to be initialised immediately.
# loader.py module depends on a pygame function that needs to be initialised
# and this module runs immediately upon importing to allow one time loading
# of all game assets.
pg.init()
pg.mixer.pre_init(44100, 16, 2, 64)
pg.display.set_caption(settings.TITLE)
pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
from xcape.common.loader import ICON_RESOURCES
pg.display.set_icon(ICON_RESOURCES["assets"]["red"][0])

from xcape.common.object import GameObject
from xcape.engines.cutscene import CutSceneEngine
from xcape.engines.menu import MenuEngine
from xcape.engines.scene import SceneEngine


class CoreEngine(GameObject):
    """
    Responsibilities:
        - Displaying and updating the scene engine.
        - Displaying and updating the menu engine.
        - Pulling out events from the event queue and passing them down.
    """

    def __init__(self):
        self.screen = pg.display.get_surface()

        self.clock = pg.time.Clock()
        self.running = True

        self.sceneEngine = SceneEngine(self.screen)
        self.menuEngine = MenuEngine(self.screen)
        self.cutsceneEngine = CutSceneEngine(self.screen)

        self.messageMenu("transition", "splash_menu")
        # self.messageScene("start_game", "solo")
        # self.messageScene("transition", 5)
        # self.messageCutScene("transition", "office_cutscene")

    def __str__(self):
        return "core_engine"

    def handleEvent(self, _):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    sys.exit()

            if (event.type == self.MENU_EVENT
                    or event.type == pg.KEYDOWN):
                self.menuEngine.handleEvent(event)

            if (event.type == self.SCENE_EVENT
                    or event.type == pg.KEYDOWN
                    or event.type == pg.KEYUP):
                self.sceneEngine.handleEvent(event)

            if (event.type == self.CUTSCENE_EVENT
                    or event.type == pg.KEYDOWN):
                self.cutsceneEngine.handleEvent(event)

    def update(self):
        self.sceneEngine.update()
        self.menuEngine.update()
        self.cutsceneEngine.update()

    def draw(self, camera=None):
        self.sceneEngine.draw()
        self.menuEngine.draw()
        self.cutsceneEngine.draw()
        pg.display.update()

    def run(self):
        while self.running:
            self.handleEvent(None)
            self.update()
            self.draw()
            self.clock.tick(settings.FPS)
