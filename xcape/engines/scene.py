"""
The scene engine of the game.
"""
import pygame as pg

import xcape.common.events as events
import xcape.common.loader as loader
import xcape.components.scenes as scenes
from xcape.common.object import GameObject
from xcape.common.render import ImageLabel
# from xcape.entities.characters import PlayerOne


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
        self.resources = loader.loadContent(loader.SCENES_PATH)
        self.mode = SinglePlayer(self.screen, self.resources)

    def handleEvent(self, event):
        self.mode.handleEvent(event)

        if event.type == events.SCENE_EVENT:
            if event.category == "start_game":
                if event.data == "solo":
                    self.mode = SinglePlayer(self.screen, self.resources)
                    self.mode.startGame()
                if event.data == "coop":
                    self.mode = None
                    self.mode.startGame()

    def update(self):
        self.mode.update()

    def draw(self):
        self.mode.draw()


class SinglePlayer(GameObject):

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, containing the images for the scenes.
        """
        self.screen = screen
        self.resources = resources
        self.pause = True

        self.camera = None
        self.collisionEngine = None
        # self.player = PlayerOne(self.screen)
        self.scene = scenes.SoloScene01(self.screen, self.resources)
        self.nameToscene = \
            {
                "blank_scene": scenes.BlankScene,
                "scene_01": scenes.SoloScene01,
            }


    def handleEvent(self, event):
        # self.collisionEngine.eventHandler(event)
        # self.player.eventHandler(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("single_player",
                                   "health",
                                   2)

            if event.key == pg.K_ESCAPE:
                self.pause = not self.pause
                if self.pause:
                    events.messageMenu("single_player",
                                       "transition",
                                       "pause_screen")
                else:
                    events.messageMenu("single_player",
                                       "transition",
                                       "blank_screen")

        if event.type == events.SCENE_EVENT:
            if event.category == "transition":
                scene = self.nameToscene[event.data]
                self.scene = scene(self.screen, self.resources)

    def update(self):
        """
        Updates the game every frame.
        """
        if not self.pause:

            self.player.update()
            self.scene.update()
            self.collisionEngine.update()
            self.camera.update()

            # Change level
            if self.scene.isEnd:
                pass

            if self.player.isHit:
                self.scene.restart()

            # Ends game if player loses
            if self.player.lives == 0:
                events.messageScene("", "transition", "game_over")

    def draw(self):
        """
        Draws all game objects on the screen.
        """
        # self.scene.draw()
        # self.player.draw()

    def startGame(self):
        """
        Starts a new game.
        """
        self.loadScenario01()

    def loadScenario01(self):
        """
        Loads the first level of the game.
        """
        spawn = (70, 70)
        self.player.rect.center = spawn
        self.scene = Scenario01(self.screen, spawn)
        self.collisionEngine = CollisionEngine(self.scene, self.player)
        events.messageMenu("single_player", "transition", "ui")


