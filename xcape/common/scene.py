"""
Contains the base class for a scene for both single and multiplayer levels.
"""

import pygame as pg

from xcape.common.object import GameObject


class BaseScene(GameObject):
    """
    The base scene for any scene.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.rect = pg.Rect(0, 0, 0, 0)
        self.levelNum = 0
        self.spawn = None

        self.players = []
        self.bosses = []
        self.walls = []
        self.sPlatforms = []
        self.mPlatforms = []
        self.dPlatforms = []
        self.switches = []
        self.doors = []
        self.spikes = []
        self.spears = []
        self.decorations = []

    def handleEvent(self, event):
        pass

    def update(self):
        raise NotImplementedError

    def draw(self, camera=None):
        raise NotImplementedError

    def addPlayers(self):
        """
        Adds players to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError

    def addBosses(self):
        """
        Adds players to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError

    def addWalls(self):
        """
        Adds walls to the scene.

        :return: List, containing wall entities.
        """
        raise NotImplementedError

    def addSPlatforms(self):
        """
        Adds static platforms to the scene.

        :return: List, containing platform entities.
        """
        raise NotImplementedError

    def addMPlatforms(self):
        """
        Adds moving platforms to the scene.

        :return: List, containing platform entities.
        """
        raise NotImplementedError

    def addDPlatforms(self):
        """
        Adds directional platforms to the scene.

        :return: List, containing platform entities.
        """
        raise NotImplementedError

    def addDoors(self):
        """
        Adds doors to the scene.

        :return: List, containing door entities.
        """
        raise NotImplementedError

    def addSwitches(self):
        """
        Adds buttons to the scene.

        :return: List, containing button entities.
        """
        raise NotImplementedError

    def addSpikes(self):
        """
        Adds spikes to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError

    def addDecorations(self):
        """
        Adds decorations to the scene.

        :return: List, containing decoration entities.
        """
        raise NotImplementedError

    def addSpears(self):
        """
        Adds spears to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError
