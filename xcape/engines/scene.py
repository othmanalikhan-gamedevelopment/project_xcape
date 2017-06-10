"""
The scene engine of the game.
"""
import pygame as pg

import xcape.common.events as events
import xcape.common.settings as settings
import xcape.components.scenes as scenes
from xcape.common.object import GameObject
from xcape.components.camera import SimpleCamera
from xcape.engines.collision import CollisionEngine


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
        self.mode = None

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

        self.pause = False
        self.camera = None
        self.collisionEngine = None

        self.scene = self.loadScene(scenes.BlankScene)
        self.nameToScene = \
            {
                "blank_scene": scenes.BlankScene,
                "scene_01": scenes.SoloScene01,
                "scene_02": scenes.SoloScene02,
                "scene_03": scenes.SoloScene03,
                "scene_04": scenes.SoloScene04,
            }
        self.numToScene = \
            {
                1: scenes.SoloScene01,
                2: scenes.SoloScene02,
                3: scenes.SoloScene03,
                4: scenes.SoloScene04,
            }
        self.loadUI()

    def handleEvent(self, event):
        self.collisionEngine.eventHandler(event)
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
                try:
                    self.scene = self.loadScene(self.nameToScene[event.data])
                except KeyError:
                    self.scene = self.loadScene(self.numToScene[event.data])

            if event.category == "death":
                self.scene.player.lives -= 1
                events.messageMenu("single_player",
                                   "health",
                                   self.scene.player.lives)

                if self.scene.player.lives == 0:
                    self.pause = True
                    self.scene = self.loadScene(self.nameToScene["blank_scene"])
                    events.messageMenu("single_player", "transition", "game_over_menu")
                else:
                    levelNum = self.scene.levelNum
                    self.scene = self.loadScene(self.numToScene[levelNum])

    def update(self):
        if not self.pause:
            self.scene.update()
            self.collisionEngine.update()
            self.camera.update()

    def draw(self):
        self.scene.drawWithCamera(self.camera)

    def startGame(self):
        """
        Starts a new game.
        """
        self.scene = self.loadScene(self.numToScene[4])

    def loadScene(self, scene):
        """
        Loads the given scene.
        """
        scene = scene(self.screen)
        scene.player.rect.center = scene.spawn
        self.camera = SimpleCamera(settings.WIDTH, settings.HEIGHT)
        self.camera.follow(scene.player)
        # self.camera.follow(scene.spikes[1])
        self.collisionEngine = CollisionEngine(scene)
        return scene

    def loadUI(self):
        """
        Triggers an event to display the UI menu.
        """
        events.messageMenu("single_player", "transition", "ui_menu")
        events.messageMenu("single_player", "health", self.scene.player.lives)
