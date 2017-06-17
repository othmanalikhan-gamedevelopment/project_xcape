"""
Responsible for the camera in a scene.
"""

import pygame as pg

from xcape.common.object import GameObject
from xcape.components.physics import PhysicsComponent


class SimpleCamera(GameObject):
    """
    A camera that follows around an entity in a scene.

    A special thanks to Sloth from StackOverflow:
        https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame
    """

    def __init__(self, WIDTH, HEIGHT):
        """
        :param WIDTH: Integer, number of pixels the camera covers horizontally.
        :param HEIGHT: Integer, number of pixels the camera covers vertically.
        """
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.HALF_WIDTH = WIDTH/2
        self.HALF_HEIGHT = HEIGHT/2

        self.physics = PhysicsComponent(self)
        self.physics.maxSpeed = 30

        self.following = None
        self.rect = pg.Rect(0, 0, self.WIDTH, self.HEIGHT)

    def update(self):
        # The initial position of the camera.
        xFollow, yFollow, _, _ = self.following.rect
        xStart, yStart, w, h = self.rect

        # The final expected position of the camera.
        xFinal = -xFollow + self.HALF_WIDTH
        yFinal = -yFollow + self.HALF_HEIGHT

        # The camera speed is proportional to the difference.
        dx = xFinal - xStart
        dy = yFinal - yStart

        self.physics.fixVelocityX(dx)
        self.physics.fixVelocityY(dy)
        self.physics.update()

    def follow(self, gameobject):
        """
        Sets the camera to follow a game object.

        :param gameobject: GameObject instance, the game object to follow.
        """
        self.following = gameobject

    def apply(self, gameobject):
        """
        Returns a shifted rectangle of the given object so such that it
        is within the bounds of the camera view.

        :param gameobject: GameObject instance, the game object to follow.
        :return: pg.Rect, the shifted rectangle into the camera's view.
        """
        return gameobject.rect.move(self.rect.topleft)
