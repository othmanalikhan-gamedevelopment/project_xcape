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

        self.scene = None
        self.camera = None
        self.collisionEngine = None
        self.pause = False

        self.nameToScene = \
            {
                "blank_scene": None,
                "scene_01": scenes.SoloScene01,
                "scene_02": scenes.SoloScene02,
                "scene_03": scenes.SoloScene03,
                "scene_04": scenes.SoloScene04,
            }
        self.numToScene = \
            {
                0: None,
                1: scenes.SoloScene01,
                2: scenes.SoloScene02,
                3: scenes.SoloScene03,
                4: scenes.SoloScene04,
            }

    def handleEvent(self, event):
        self.collisionEngine.eventHandler(event)
        self.scene.handleEvent(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self._togglePause()

        if event.type == events.SCENE_EVENT:
            if event.category == "transition":
                try:
                    self._loadScene(self.nameToScene[event.data])
                except KeyError:
                    self._loadScene(self.numToScene[event.data])

            if event.category == "death":
                self.scene.player.lives -= 1
                events.messageMenu("single_player", "health", self.scene.player.lives)
                if self.scene.player.lives == 0:
                    self._showGameOver()
                else:
                    self._restartScene()

    def update(self):
        if not self.pause and self.scene:
            self.scene.update()
            self.collisionEngine.update()
            self.camera.update()

    def draw(self):
        if self.scene:
            self.scene.drawWithCamera(self.camera)

    def startGame(self):
        """
        Starts a new game.
        """
        self._loadScene(self.nameToScene["scene_04"])

    def _loadScene(self, Scene):
        """
        Loads the given scene.

        :param Scene: BaseScene inheritor, representing a scene class.
        """
        if Scene:
            self.scene = Scene(self.screen)
            self.collisionEngine = CollisionEngine(self.scene)
            self._loadUI(self.scene.player.lives)

            self.camera = SimpleCamera(settings.WIDTH, settings.HEIGHT)
            self.camera.follow(self.scene.player)
            # self.camera.follow(self.scene.walls[0])

    def _loadUI(self, health):
        """
        Triggers an event to display the UI menu.

        :param health: Integer, the number of hearts to display on the UI.
        """
        events.messageMenu("single_player", "transition", "ui_menu")
        events.messageMenu("single_player", "health", health)

    def _restartScene(self):
        """
        Restarts the current scene.
        """
        levelNum = self.scene.levelNum
        self._loadScene(self.numToScene[levelNum])

    def _showGameOver(self):
        """
        Pauses the game and triggers the game over screen.
        """
        self.pause = True
        self._loadScene(self.nameToScene["blank_scene"])
        events.messageMenu("single_player", "transition", "game_over_menu")

    def _togglePause(self):
        """
        Pauses the game and triggers the pause menu and vice-versa.
        """
        self.pause = not self.pause
        if self.pause:
            events.messageMenu("single_player", "transition", "pause_menu")
        else:
            events.messageMenu("single_player", "transition", "blank_menu")
