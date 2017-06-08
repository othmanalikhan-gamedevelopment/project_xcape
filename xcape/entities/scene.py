"""
Contains all the entities in a scene (excluding the players and bosses).
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.settings as settings
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent
from xcape.components.physics import PhysicsComponent


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


class BasePlatform(SceneEntity):
    """
    A base platform that is to be inherited by other platforms.
    """

    def __init__(self, x, y, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(screen)
        self.rect = pg.Rect(x, y, 0, 0)
        self.resources = resources
        self.image = None

    def resize(self, blocks, leftImage, midImage, rightImage):
        """
        Resizes the platform horizontally by some number of blocks specified.

        :param blocks: Integer, the number of times to replicate the platform.
        :param leftImage: pygame.Surface, the image of the left corner.
        :param midImage: pygame.Surface, the image of the mid.
        :param rightImage: pygame.Surface, the image of the right corner.
        :return: pygame.Surface, the resized image of the platform
        """
        lw, lh = leftImage.get_size()
        mw, mh = midImage.get_size()
        rw, rh = rightImage.get_size()

        # Creating platform image
        platform = pg.Surface((lw + blocks*mw + rw, mh))
        platform.blit(leftImage, (0, 0))
        for i in range(blocks):
            platform.blit(midImage, (lw + i*mw, 0))
        platform.blit(rightImage, (lw + blocks*mw, 0))

        # Newly created surface has a black background, so need to remove
        # black pixels
        platform.set_colorkey(settings.COLOURS["black"])
        platform = platform.convert_alpha()
        return platform

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class SPlatform(BasePlatform):
    """
    A static platform entity that the player can stand on.
    """

    def __init__(self, x, y, blocks, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(x, y, screen, resources)

        left = self.resources["platforms"]["platform_1.png"]
        mid = self.resources["platforms"]["platform_2.png"]
        right = self.resources["platforms"]["platform_3.png"]
        self.image = self.resize(blocks, left, mid, right)
        self.rect.size = self.image.get_size()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class DPlatform(BasePlatform):
    """
    A directional platform entity that requires the player to jump from below
    to pass through.
    """

    def __init__(self, x, y, blocks, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(x, y, screen, resources)

        left = self.resources["platforms"]["platform_1.png"]
        mid = self.resources["platforms"]["platform_2.png"]
        right = self.resources["platforms"]["platform_3.png"]
        self.image = self.resize(blocks, left, mid, right)
        self.rect.size = self.image.get_size()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class MPlatform(BasePlatform):
    """
    A moving platform entity that constantly moves between two points.
    """

    def __init__(self, A, B, dx, dy, screen, image):
        """
        :param A: 2-Tuple, containing coordinates of a point A.
        :param B: 2-Tuple, containing coordinates of a point B.
        :param dx: Number, pixels moved in the x-axis every physics tick.
        :param dy: Number, pixels moved in the y-axis every physics tick.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param image: pygame.Surface, the image of the platform.
        """
        super().__init__(A[0], A[1], screen, image)
        self.image = image
        self.rect.size = self.image.get_size()

        self.state = "forward"
        self.physics = PhysicsComponent(self)
        self.physics.isGravity = False
        self.A = A
        self.B = B
        self.dx = dx
        self.dy = dy

    def update(self):
        xBoundB, yBoundB = self.B
        xBoundA, yBoundA = self.A

        if self.rect.x > xBoundB:
            self.rect.x = xBoundB
            self.dx = -self.dx
        if self.rect.y > yBoundB:
            self.dy = -self.dy

        if self.rect.x < xBoundA:
            self.rect.x = xBoundA
            self.dx = -self.dx
        if self.rect.y < yBoundA:
            self.dy = -self.dy

        self.physics.velocity.x = self.dx
        self.physics.velocity.y = self.dy
        self.physics.update()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class Switch(SceneEntity):
    """
    A switch entity that the player can turn on and off.
    """

    def __init__(self, x, y, switchNum, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param switchNum: Integer, identifying the number of the button.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(screen)
        self.resources = resources
        self.rect = pg.Rect(x, y, 0, 0)
        self.buttonNum = switchNum
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


class Door(SceneEntity):
    """
    A door entity that the player can enter.
    """

    def __init__(self, x, y, doorNum, screen, resources):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param doorNum: Integer, identifying the number of the button.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__(screen)
        self.resources = resources
        self.rect = pg.Rect(x, y, 0, 0)
        self.doorNum = doorNum
        self.switchesWaiting = None
        self.isClosed = True

        button = resources["doors"]
        self.state = "closed"
        self.animation = AnimationComponent(self, enableRepeat=False)
        self.animation.add("open", [button["open.png"]], float('inf'))
        self.animation.add("closed", [button["closed.png"]], float('inf'))

    def handleEvent(self, event):
        if event.type == events.SCENE_EVENT:
            if event.category == "switch":

                try:
                    switchNum, isOn = event.data
                    self.switchesWaiting.remove(switchNum)
                    if not self.switchesWaiting:
                        self.openDoor()
                except ValueError:
                    pass

    def update(self):
        self.animation.update()

    def drawWithCamera(self, camera):
        self.animation.drawWithCamera(camera)

    def waitForSwitches(self, switches):
        """
        Links the door to the given switch numbers; the door opens only when
        those switches have been activated.

        :param switches: List, containing Integers for switch numbers.
        """
        self.switchesWaiting = switches

    def openDoor(self):
        """
        Changes the state of the door to open and sends out an event.
        """
        self.isClosed = False
        self.state = "open"
        events.messageScene("Door", "door", (self.doorNum, self.isClosed))



