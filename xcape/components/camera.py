"""
Responsible for the camera in a scene.
"""

import pygame as pg

from xcape.common.object import GameObject


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

        self.following = None
        self.view = pg.Rect(0, 0, self.WIDTH, self.HEIGHT)

    def update(self):
        x, y, _, _ = self.following.rect
        _, _, w, h = self.view

        self.view = pg.Rect(-x + self.HALF_WIDTH, -y + self.HALF_HEIGHT, w, h)

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
        return gameobject.rect.move(self.view.topleft)
