"""
Contains all the entities in a scene (excluding the players and bosses).
"""

import pygame as pg


from xcape.components.animation import AnimationComponent
from xcape.common.object import GameObject


class SceneEntity(GameObject):
    """
    Represents an the base of an entity in a scene.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.rect = pg.Rect(0, 0, 0, 0)
        self.screen = screen
        self.state = "idle"

    def drawWithCamera(self, camera):
        """
        Draws the player on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        pass


class Wall(SceneEntity):
    """
    A wall entity that obstructs the player.
    """

    def __init__(self, x, y, blocks, orientation, image, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param orientation: String, either 'v' or 'h' for vertical or horizontal.
        :param image: pygame.Surface, the image of the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        self.image = image
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = image.get_size()
        self.extend(blocks, orientation)

    def extend(self, blocks, orientation):
        """
        Extends the wall either vertically or horizontally by some number of
        blocks specified.

        :param blocks: Integer, the number of times to replicate the wall.
        :param orientation: String, either 'v' or 'h' for vertical or horizontal.
        """
        w, h = self.image.get_size()

        if orientation == "h":
            wall = pg.Surface((blocks*w, h))
            for i in range(blocks):
                wall.blit(self.image, (i*w, 0))
            self.rect.width += (blocks-1)*w

        if orientation == "v":
            wall = pg.Surface((w, blocks*h))
            for i in range(blocks):
                wall.blit(self.image, (0, i*h))
            self.rect.height += (blocks-1)*h

        self.image = wall

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class StaticPlatform(SceneEntity):
    """
    A static platform that the player can collide with.
    """

    def __init__(self, x, y, blocks, screen, resources):
        super().__init__(screen, resources)


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

