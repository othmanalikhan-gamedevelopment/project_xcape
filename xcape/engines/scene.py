"""
The scene engine of the game.
"""
import pygame as pg

import xcape.common.events as events
import xcape.common.loader as loader
import xcape.common.settings as settings
import xcape.components.scenes as scenes
from xcape.common.object import GameObject
from xcape.components.camera import SimpleCamera
from xcape.engines.collision import CollisionEngine
from xcape.entities.characters import Player


class SceneEngine(GameObject):
    """
    Responsibilities:
        - Displaying and updating the current scene.
        - Transitioning between menus.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.mode = SinglePlayer(screen)

    def handleEvent(self, event):
        if self.mode:
            self.mode.handleEvent(event)

        if event.type == events.SCENE_EVENT:
            if event.category == "start_game":
                if event.data == "solo":
                    self.mode = SinglePlayer(self.screen)
                    self.mode.startGame()
                if event.data == "coop":
                    self.mode = None
                    self.mode.startGame()

    def update(self):
        if self.mode:
            self.mode.update()

    def draw(self):
        if self.mode:
            self.mode.draw()


class SinglePlayer(GameObject):

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.resourcesScene = loader.loadContent(loader.SCENES_PATH)
        self.resourcesChar = loader.loadContent(loader.CHARACTERS_PATH)
        self.pause = False

        self.levelNum = 0
        self.camera = None
        self.collisionEngine = None

        self.player = Player(self.screen, self.resourcesChar)
        self.scene = self.loadScene(scenes.SoloScene02)
        self.nameToScene = \
            {
                "blank_scene": scenes.BlankScene,
                "scene_01": scenes.SoloScene01,
                "scene_02": scenes.SoloScene02,
            }
        self.numToScene = \
            {
                1: scenes.SoloScene01,
                2: scenes.SoloScene02,
            }

    def handleEvent(self, event):
        self.collisionEngine.eventHandler(event)
        self.player.handleEvent(event)
        self.scene.handleEvent(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.pause = not self.pause
                if self.pause:
                    events.messageMenu("single_player",
                                       "transition",
                                       "pause_menu")
                else:
                    events.messageMenu("single_player",
                                       "transition",
                                       "blank_menu")

        if event.type == events.SCENE_EVENT:
            if event.category == "transition":
                self.scene = self.loadScene(self.numToScene[event.data])

            # # Restart level
            # if self.player.isHit:
            #     self.scene.restart()

            # # Game over
            # if self.player.lives == 0:
            #     self.pause = True
            #     events.messageMenu("single_player", "transition", "game_over")

    def update(self):
        if not self.pause:
            self.scene.update()
            self.player.update()
            self.collisionEngine.update()
            self.camera.update()

    def draw(self):
        self.scene.drawWithCamera(self.camera)
        self.player.drawWithCamera(self.camera)

    def startGame(self):
        """
        Starts a new game.
        """
        self.loadScene(self.numToScene[1])

    def loadScene(self, scene):
        """
        Loads the given scene.
        """
        scene = scene(self.screen, self.resourcesScene)
        self.player.rect.center = scene.spawn
        self.camera = SimpleCamera(settings.WIDTH, settings.HEIGHT)
        self.camera.follow(self.player)
        # self.camera.follow(scene.walls[2])
        self.collisionEngine = CollisionEngine(self.player, scene)
        events.messageMenu("single_player", "transition", "ui_menu")
        events.messageMenu("single_player", "health", 3)
        return scene
