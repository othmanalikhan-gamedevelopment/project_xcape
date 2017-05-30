import configparser

import pygame as pg

import xcape.common.events as events
from xcape.engine.menu import MenuEngine
from xcape.engine.scene import SceneEngine


class CoreEngine:

    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.settings = configparser.ConfigParser()
        self.settings.read("settings.ini")
        FPS = int(self.settings["GENERAL"]["fps"])
        TITLE = self.settings["GENERAL"]["title"]
        WIDTH = int(self.settings["GENERAL"]["width"])
        HEIGHT = int(self.settings["GENERAL"]["height"])

        pg.display.set_caption(TITLE)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.clock.tick(FPS)
        self.running = True

        self.sceneEngine = SceneEngine()
        self.menuEngine = MenuEngine()

    def update(self):
        self.sceneEngine.update()
        self.menuEngine.update()

    def handleEvent(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_F4:
                    quit()

            if event.type == events.MENU_EVENT:
                self.menuEngine.handleEvent(event)
            if event.type == events.SCENE_EVENT:
                self.sceneEngine.handleEvent(event)

    def draw(self):
        self.sceneEngine.draw()
        self.menuEngine.draw()
        pg.display.update()

    def run(self):
        while self.running:
            self.handleEvent()
            self.update()
            self.draw()
