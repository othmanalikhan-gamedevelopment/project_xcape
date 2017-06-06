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

    def __init__(self, x, y, blocks, image, screen):
        super().__init__(screen)

        w, h = image.get_size()
        self.rect = pg.Rect(x, y, w, h)
        self.blocks = blocks
        self.state = "idle"

        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", image)

    def extend(self, blocks, isVertical=True):
        """
        Extends the wall either vertically or horizontally by some number of
        blocks specified.

        :param blocks: Integer, the number of times to replicate the wall.
        :param isVertical: Boolean, whether the extension is vertical or horizontal.
        """
        if isVertical:
            w, h = self.animation.image.get_size()
            wall = pg.Surface((blocks*w, h))
            for i in range(blocks):
                wall.blit(self.animation.image, (i*w, 0))

            self.animation.image = wall

    def addCorner(self, isLeft):
        pass

    def update(self):
        self.animation.update()

    def drawWithCamera(self, camera):
        self.animation.drawWithCamera(camera)


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

