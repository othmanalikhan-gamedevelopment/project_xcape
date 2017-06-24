"""
The scene engine of the game.
"""
import pygame as pg

import xcape.common.settings as settings
import xcape.components.scenes as scenes
from xcape.common.object import GameObject
from xcape.components.camera import SimpleCamera
from xcape.engines.collision import CollisionEngine


class SceneEngine(GameObject):
    """
    Responsibilities:
        - Displaying and updating the current scene.
        - Transitioning between scenes.
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

        if event.type == self.SCENE_EVENT:
            if event.category == "start_game":
                if event.data == "solo":
                    self.mode = SinglePlayer(self.screen)
                    self.mode.startGame()
                if event.data == "coop":
                    self.mode = MultiPlayer(self.screen)
                    self.mode.startGame()

            if event.category == "no_mode":
                self.mode = None

            if event.category == "screen":
                self.screen = pg.display.get_surface()

    def update(self):
        if self.mode:
            self.mode.update()

    def draw(self, camera=None):
        if self.mode:
            self.mode.draw()


# TODO: Refactor
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

        self.maxLives = 5
        self.lives = 1
        self._loadUI(self.maxLives, self.lives)

        self.nameToScene = \
            {
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

    def __str__(self):
        return "single_player"

    def handleEvent(self, event):
        self.collisionEngine.eventHandler(event)
        self.scene.handleEvent(event)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE and self.lives != 0:
                self._togglePauseMenu()
            if event.key == pg.K_RETURN:
                self.camera.duration = 0

        if event.type == self.SCENE_EVENT:
            if event.category == "transition":
                try:
                    self._loadScene(self.nameToScene[event.data])
                except KeyError:
                    try:
                        self._loadScene(self.numToScene[event.data])
                    except KeyError:
                        self.messageMenu("transition", "win_menu")

            if event.category == "complete":
                if event.sender == "death_menu":
                    self._loadUI(self.maxLives, self.lives)
                    self._restartScene()
                    self.pause = False

            if event.category == "death":
                self.lives -= 1
                if self.lives == 0:
                    self._showLoseMenu()
                else:
                    pg.mixer.stop()
                    self.pause = True
                    self.messageMenu("transition", "death_menu")

    def update(self):
        if not self.pause and self.scene:
            self.scene.update()
            self.collisionEngine.update()
            self.camera.update()

    def draw(self, camera=None):
        if self.scene:
            self.scene.draw(self.camera)

    def startGame(self):
        """
        Starts a new game.
        """
        self._loadScene(self.nameToScene["scene_01"])

    def _loadScene(self, Scene):
        """
        Loads the given scene.

        :param Scene: BaseScene inheritor, representing a scene class.
        """
        self.scene = Scene(self.screen)
        self.collisionEngine = CollisionEngine(self.scene)

        self.camera = SimpleCamera(settings.WIDTH, settings.HEIGHT)
        self.camera.follow(self.scene.players[0])
        self.camera.followBriefly(self.scene.doors[-1])

    def _loadUI(self, maxHealth, currentHealth):
        """
        Triggers an event to display the UI menu.

        :param currentHealth: Integer, the number of full hearts to display.
        :param maxHealth: Integer, the number of empty hearts to display.
        """
        self.messageMenu("transition", "solo_ui_menu")
        self.messageMenu("max_health", maxHealth)
        self.messageMenu("health", currentHealth)

    def _restartScene(self):
        """
        Restarts the current scene.
        """
        levelNum = self.scene.levelNum
        self._loadScene(self.numToScene[levelNum])

    def _showLoseMenu(self):
        """
        Pauses the game and triggers the game over screen.
        """
        self.pause = True
        self.messageMenu("transition", "lose_menu")

    def _togglePauseMenu(self):
        """
        Pauses the game and triggers the pause menu and vice-versa.
        """
        self.pause = not self.pause
        if self.pause:
            self.messageMenu("transition", "pause_menu")
        else:
            self.messageMenu("transition", "blank_menu")
            self._loadUI(self.maxLives, self.lives)


# TODO: Refactor
class MultiPlayer(GameObject):

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen

        self.scene = None
        self.camera = None
        self.collisionEngine = None
        self.pause = False

        self.maxLives = [5, 5]
        self.lives = [5, 5]
        self._loadUI(self.maxLives, self.lives)

        self.nameToScene = \
            {
                "scene_01": scenes.CoopScene01,
                "scene_02": scenes.CoopScene02,
                "scene_03": scenes.CoopScene03,
            }
        self.numToScene = \
            {
                1: scenes.CoopScene01,
                2: scenes.CoopScene02,
                3: scenes.CoopScene03,
            }

    def handleEvent(self, event):
        self.collisionEngine.eventHandler(event)
        self.scene.handleEvent(event)

        if event.type == pg.KEYDOWN:
            isAlive = all([live != 0 for live in self.lives])
            if event.key == pg.K_ESCAPE and isAlive:
                self._togglePauseMenu()
            if event.key == pg.K_RETURN:
                self.camera.duration = 0
            if event.key == pg.K_SPACE:
                p1, p2 = self.scene.players
                if self.camera.following == p1:
                    self.camera.follow(p2)
                else:
                    self.camera.follow(p1)

        if event.type == self.SCENE_EVENT:
            if event.category == "transition":
                try:
                    self._loadScene(self.nameToScene[event.data])
                except KeyError:
                    try:
                        self._loadScene(self.numToScene[event.data])
                    except KeyError:
                        self.messageMenu("transition", "win_menu")

            if event.category == "complete":
                if event.sender == "death_menu":
                    self._loadUI(self.maxLives, self.lives)
                    self._restartScene()
                    self.pause = False

            if event.category == "death":
                playerNum = event.data
                self.lives[playerNum-1] -= 1
                isAlive = all([live != 0 for live in self.lives])
                if not isAlive:
                    self._showGameOver()
                else:
                    self.pause = True
                    self.messageMenu("transition", "death_menu")

    def update(self):
        if not self.pause and self.scene:
            self.scene.update()
            self.collisionEngine.update()
            self.camera.update()

    def draw(self, camera=None):
        if self.scene:
            self.scene.draw(self.camera)

    def startGame(self):
        """
        Starts a new game.
        """
        self._loadScene(self.nameToScene["scene_01"])

    def _loadScene(self, Scene):
        """
        Loads the given scene.

        :param Scene: BaseScene inheritor, representing a scene class.
        """
        self.scene = Scene(self.screen)
        self.collisionEngine = CollisionEngine(self.scene)

        self.camera = SimpleCamera(settings.WIDTH, settings.HEIGHT)
        self.camera.follow(self.scene.players[0])
        self.camera.followBriefly(self.scene.doors[-1])

    def _loadUI(self, maxHealth, health):
        """
        Triggers an event to display the UI menu.

        :param health: List, containing current healths for both players.
        :param maxHealth: List, containing max healths for both players.
        """
        self.messageMenu("transition", "coop_ui_menu")
        self.messageMenu("max_health", maxHealth)
        self.messageMenu("health", health)

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
        self.messageMenu("transition", "lose_menu")

    def _togglePauseMenu(self):
        """
        Pauses the game and triggers the pause menu and vice-versa.
        """
        self.pause = not self.pause
        if self.pause:
            self.messageMenu("transition", "pause_menu")
        else:
            self.messageMenu("transition", "blank_menu")
            self._loadUI(self.maxLives, self.lives)
