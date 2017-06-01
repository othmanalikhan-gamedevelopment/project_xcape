"""
Contains all the entities in a scene (excluding the players and bosses).
"""

import pygame as pg


from xcape.common.object import GameObject


class SceneEntity(GameObject):
    """
    Represents an object in game.
    """

    def __init__(self, data):
        """
        A simple constructor.
        """
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)


class StaticPlatform(SceneEntity):
    """
    A static platform that the player can collide with.
    """

    def __init__(self, x, y, blocks):
        pass


class MovingPlatform(SceneEntity):
    """
    A moving platform that moves constantly between two points.
    """

    def __init__(self, x, y, dx, dy, boundVertical, boundHorizontal):
        """
        A simple constructor.
        """
        super().__init__()

        self.moveX = moveX
        self.moveY = moveY

        self.boundary_top = boundVertical[0]
        self.boundary_bottom = boundVertical[1]
        self.boundary_left = boundHorizontal[0]
        self.boundary_right = boundHorizontal[1]

    def update(self):
        """
        Updating the moving platform to move in game.
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        cur_pos_x = self.rect.x
        cur_pos_y = self.rect.y

        if cur_pos_x < self.boundary_left or cur_pos_x > self.boundary_right:
            self.moveX *= -1
            
        if cur_pos_y > self.boundary_bottom or cur_pos_y < self.boundary_top:
            self.moveY *= -1


class TransparentPlatform(SceneEntity):
    """
    A transparent platform that the player can pass through from beneath only.
    """

    def __init__(self, size):
        """
        A simple constructor.
        """
        super().__init__(size)

