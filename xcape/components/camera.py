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
        self.physics.maxSpeed = 20

        self.origin = 0
        self.elapsed = 0
        self.duration = 0
        self.delay = 0

        self.brief = None
        self.following = None
        self.rect = pg.Rect(0, 0, self.WIDTH, self.HEIGHT)

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin
        start = self.delay
        end = self.duration + self.delay

        if self.brief and end > self.elapsed > start:
            dx, dy = self.computeShift(self.brief)
        else:
            dx, dy = self.computeShift(self.following)

        self.physics.fixVelocityX(dx)
        self.physics.fixVelocityY(dy)
        self.physics.update()

    def computeShift(self, gameobject):
        """
        Calculates how much the camera needs to be shifted by from it's
        current position to the position of the following target.

        :param gameobject: GameObject instance, the game object to follow.
        :return: 2-Tuple, the (dx, dy) amount of pixels to shift.
        """
        # The initial position of the camera.
        xFollow, yFollow, _, _ = gameobject.rect
        xStart, yStart, w, h = self.rect

        # The final expected position of the camera.
        xFinal = -xFollow + self.HALF_WIDTH
        yFinal = -yFollow + self.HALF_HEIGHT

        # The camera speed is proportional to the difference.
        dx = xFinal - xStart
        dy = yFinal - yStart
        return dx, dy

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

    def followBriefly(self, gameobject, delay=1000, duration=2000):
        """
        Briefly focuses the given game object the returns to the original
        following target of the camera.

        :param gameobject: GameObject instance, the game object to follow.
        :param delay: Integer, the milliseconds to wait before following.
        :param duration: Integer, the milliseconds to follow the given target.
        """
        self.brief = gameobject
        self.duration = duration
        self.delay = delay
        self.origin = pg.time.get_ticks()
        self.elapsed = 0
