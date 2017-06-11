"""
The core engine of the game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.settings as settings
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
        # Loads all images into memory

        pg.init()
        self.screen = pg.display.get_surface()

        self.clock = pg.time.Clock()
        self.clock.tick(settings.FPS)
        self.running = True

        self.sceneEngine = SceneEngine(self.screen)
        self.menuEngine = MenuEngine(self.screen)
        self.cutsceneEngine = CutSceneEngine(self.screen)

        # events.messageScene("core_engine", "start_game", "solo")
        # events.messageScene("core_engine", "transition", "scene_04")
        # events.messageScene("core_engine", "transition", "blank_scene")

        # events.messageMenu("core_engine", "transition", "blank_menu")
        events.messageMenu("core_engine", "transition", "splash_menu")

        events.messageCutScene("core_engine", "transition", "blank_cutscene")

    def handleEvent(self, _):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    quit()

            if (event.type == events.MENU_EVENT
                    or event.type == pg.KEYDOWN):
                self.menuEngine.handleEvent(event)

            if (event.type == events.SCENE_EVENT
                    or event.type == pg.KEYDOWN
                    or event.type == pg.KEYUP):
                self.sceneEngine.handleEvent(event)

            if (event.type == events.CUTSCENE_EVENT
                    or event.type == pg.KEYDOWN):
                self.cutsceneEngine.handleEvent(event)

    def update(self):
        self.sceneEngine.update()
        self.menuEngine.update()
        self.cutsceneEngine.update()

    def draw(self):
        self.sceneEngine.draw()
        self.menuEngine.draw()
        self.cutsceneEngine.draw()
        pg.display.update()

    def run(self):
        while self.running:
            self.handleEvent(None)
            self.update()
            self.draw()
