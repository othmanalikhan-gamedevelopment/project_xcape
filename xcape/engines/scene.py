"""
The scene engine of the game.
"""
import pygame as pg

import xcape.common.settings as settings
import xcape.components.coop as coop
import xcape.components.solo as solo
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
        self.lives = 5
        self._loadUI(self.maxLives, self.lives)

        self.nameToScene = \
            {
                "scene_01": solo.JailScene01,
                "scene_02": solo.JailScene02,
                "scene_03": solo.JailScene03,
                "scene_04": solo.JailScene04,
            }
        self.numToScene = \
            {
                1: solo.JailScene01,
                2: solo.JailScene02,
                3: solo.JailScene03,
                4: solo.JailScene04,
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
                self._handleTransition(event)
            if event.category == "death":
                self._handleDeath()
            if event.category == "revive":
                self._handleRevive()

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

    def _restartScene(self):
        """
        Restarts the current scene.
        """
        levelNum = self.scene.levelNum
        self._loadScene(self.numToScene[levelNum])

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

    def _handleTransition(self, event):
        """
        Transitions to the specified level given by the event, or to the win
        menu if no level can be found.

        :param event: pygame.Event object, containing the level to transition.
        """
        try:
            self._loadScene(self.nameToScene[event.data])
        except KeyError:
            try:
                self._loadScene(self.numToScene[event.data])
            except KeyError:
                self.messageMenu("transition", "win_menu")

    def _handleDeath(self):
        """
        Pauses the level and transitions to either the death or game over menu.
        """
        self.lives -= 1
        if self.lives == 0:
            self._showLoseMenu()
        else:
            pg.mixer.stop()
            self.pause = True
            self.messageMenu("transition", "death_menu")

    def _handleRevive(self):
        """
        Restarts the level and unpauses it.
        """
        self._loadUI(self.maxLives, self.lives)
        self._restartScene()
        self.pause = False


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
                "scene_01": coop.JailScene01,
                "scene_02": coop.JailScene02,
                "scene_03": coop.JailScene03,
            }
        self.numToScene = \
            {
                1: coop.JailScene01,
                2: coop.JailScene02,
                3: coop.JailScene03,
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
                self._swapCameraFollow()

        if event.type == self.SCENE_EVENT:
            if event.category == "transition":
                self._handleTransition(event)
            if event.category == "death":
                self._handleDeath(event)
            if event.category == "revive":
                self._handleRevive()

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

    def _restartScene(self):
        """
        Restarts the current scene.
        """
        levelNum = self.scene.levelNum
        self._loadScene(self.numToScene[levelNum])

    def _loadScene(self, Scene):
        """
        Loads the given scene.

        :param Scene: BaseScene inheritor, representing a scene class.
        """
        self.scene = Scene(self.screen)
        self.collisionEngine = CollisionEngine(self.scene)

        self.camera = SimpleCamera(settings.WIDTH, settings.HEIGHT)
        self.camera.physics.maxSpeed = 30
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

    def _handleTransition(self, event):
        """
        Transitions to the specified level given by the event, or to the win
        menu if no level can be found.

        :param event: pygame.Event object, containing the level to transition.
        """
        try:
            self._loadScene(self.nameToScene[event.data])
        except KeyError:
            try:
                self._loadScene(self.numToScene[event.data])
            except KeyError:
                self.messageMenu("transition", "win_menu")

    def _handleDeath(self, event):
        """
        Pauses the level and transitions to either the death or game over menu.

        :param event: pygame.Event object, representing a death event.
        """
        playerNum = event.data
        self.lives[playerNum-1] -= 1
        isAlive = all([live != 0 for live in self.lives])
        if not isAlive:
            self._showLoseMenu()
        else:
            pg.mixer.stop()
            self.pause = True
            self.messageMenu("transition", "death_menu")

    def _handleRevive(self):
        """
        Restarts the level and unpauses it.
        """
        self._loadUI(self.maxLives, self.lives)
        self._restartScene()
        self.pause = False

    def _swapCameraFollow(self):
        """
        Toggles the camera to follow between the two players.
        """
        p1, p2 = self.scene.players
        if self.camera.following == p1:
            self.camera.follow(p2)
        else:
            self.camera.follow(p1)
