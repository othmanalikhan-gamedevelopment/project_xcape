"""
The core engine of the game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.settings as settings
from xcape.common.gameobject import GameObject
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
        pg.init()
        pg.display.set_caption(settings.TITLE)
        self.screen = pg.display.set_mode((settings.WIDTH, settings.HEIGHT))

        self.clock = pg.time.Clock()
        self.clock.tick(settings.FPS)
        self.running = True

        self.sceneEngine = SceneEngine(self.screen)
        self.menuEngine = MenuEngine(self.screen)

    def update(self):
        self.sceneEngine.update()
        self.menuEngine.update()

    def handleEvent(self, _):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    quit()

            if event.type == events.MENU_EVENT or event.type == pg.KEYDOWN:
                self.menuEngine.handleEvent(event)
            if event.type == events.SCENE_EVENT:
                self.sceneEngine.handleEvent(event)

    def draw(self):
        self.sceneEngine.draw()
        self.menuEngine.draw()
        pg.display.update()

    def run(self):
        while self.running:
            self.handleEvent(None)
            self.update()
            self.draw()

