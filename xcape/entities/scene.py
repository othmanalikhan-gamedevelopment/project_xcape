"""
Contains all the entities in a scene (excluding the players and bosses).
"""

import pygame as pg


import xcape.common.settings as settings
import xcape.common.events as events

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
        self.image = self.resize(blocks, orientation, image)
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def resize(self, blocks, orientation, image):
        """
        Resizes the wall vertically or horizontally by a specified amount.

        :param blocks: Integer, the total number of blocks the final wall has.
        :param orientation: String, either 'v' or 'h' for vertical or horizontal.
        :param image: pygame.Surface, the image of the wall.
        :return: pygame.Surface, the resized image of the platform
        """
        w, h = image.get_size()

        if orientation == "h":
            wall = pg.Surface((blocks*w, h))
            for i in range(blocks):
                wall.blit(image, (i*w, 0))

        if orientation == "v":
            wall = pg.Surface((w, blocks*h))
            for i in range(blocks):
                wall.blit(image, (0, i*h))

        wall = wall.convert()
        return wall

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class StaticPlatform(SceneEntity):
    """
    A platform entity that the player can stand on.
    """

    def __init__(self, x, y, blocks, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(screen)
        self.resources = resources
        self.image = self.resize(blocks)
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def resize(self, blocks):
        """
        Resizes the platform horizontally by some number of blocks specified.

        :param blocks: Integer, the number of times to replicate the platform.
        :return: pygame.Surface, the resized image of the platform
        """
        left = self.resources["platforms"]["platform_1.png"]
        mid = self.resources["platforms"]["platform_2.png"]
        right = self.resources["platforms"]["platform_3.png"]

        lw, lh = left.get_size()
        mw, mh = mid.get_size()
        rw, rh = right.get_size()

        # Creating platform image
        platform = pg.Surface((lw + blocks*mw + rw, mh))
        platform.blit(left, (0, 0))
        for i in range(blocks):
            platform.blit(mid, (lw + i*mw, 0))
        platform.blit(right, (lw + blocks*mw, 0))

        # Newly created surface has a black background, so need to remove
        # black pixels
        platform.set_colorkey(settings.COLOURS["black"])
        platform = platform.convert_alpha()
        return platform

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class Switch(SceneEntity):
    """
    A switch entity that the player can turn on and off.
    """

    def __init__(self, x, y, buttonNum, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param buttonNum: Integer, identifying the number of the button.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(screen)
        self.resources = resources
        self.rect = pg.Rect(x, y, 0, 0)
        self.buttonNum = buttonNum
        self.isOn = True

        button = resources["buttons"]
        self.state = "on"
        self.animation = AnimationComponent(self, enableRepeat=False)
        self.animation.add("on", [button["switch"][0]], float('inf'))
        self.animation.add("off", button["switch"], 500)

    def update(self):
        self.animation.update()

    def drawWithCamera(self, camera):
        self.animation.drawWithCamera(camera)

    def turnOff(self):
        """
        Changes the state of the button to off and sends out an event.
        """
        self.isOn = False
        self.state = "off"
        events.messageScene("Switch", "switch", (self.buttonNum, self.isOn))







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


