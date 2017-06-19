"""
Contains all the entities in a scene (excluding the players and bosses).
"""

import pygame as pg

import xcape.common.events as events
from xcape.common.loader import sceneResources
from xcape.common.object import GameObject
from xcape.common.render import buildParts, replicate
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

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        pass


class Decoration(SceneEntity):
    """
    An entity that does nothing other than act as a background decoration.
    """

    def __init__(self, x, y, image, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param image: pygame.Surface, the image of the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        self.image = image
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class Wall(SceneEntity):
    """
    A wall entity that obstructs the player.
    """

    def __init__(self, x, y, blocks, orientation, images, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param orientation: String, either 'v' or 'h' for vertical or horizontal.
        :param images: Tuple, containing either a single or three
        pygame.Surfaces to build the platform.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        if len(images) == 3:
            self.image = buildParts(blocks, orientation, images)
        elif len(images) == 1:
            self.image = replicate(blocks, orientation, images[0])

        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class BasePlatform(SceneEntity):
    """
    A base platform that is to be inherited by other platforms.
    """

    def __init__(self, x, y, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        self.rect = pg.Rect(x, y, 0, 0)
        self.image = None

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class SPlatform(BasePlatform):
    """
    A static platform entity that the player can stand on.
    """

    def __init__(self, x, y, blocks, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(x, y, screen)

        left = sceneResources["platforms"]["platform_1.png"]
        mid = sceneResources["platforms"]["platform_2.png"]
        right = sceneResources["platforms"]["platform_3.png"]
        images = [left, mid, right]
        self.image = buildParts(blocks, "h", images)
        self.rect.size = self.image.get_size()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class DPlatform(BasePlatform):
    """
    A directional platform entity that requires the player to jump from below
    to pass through.
    """

    def __init__(self, x, y, blocks, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param blocks: Integer, the number of times to replicate the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(x, y, screen)

        left = sceneResources["platforms"]["platform_1.png"]
        mid = sceneResources["platforms"]["platform_2.png"]
        right = sceneResources["platforms"]["platform_3.png"]
        images = [left, mid, right]
        self.image = buildParts(blocks, "h", images)
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
        super().__init__(A[0], A[1], screen)
        self.image = image
        self.rect.size = self.image.get_size()

        self.state = "forward"
        self.physics = PhysicsComponent(self)
        self.physics.isGravity = False
        self.A = A
        self.B = B
        self.dx = dx
        self.dy = dy
        self.isDirectionX = True
        self.isDirectionY = True

    def update(self):
        # Physics update at start because it seems there is a mismatch of clock
        # between moving platform and the player; the proper solution involves
        # coding a physics engine that synchronises all physics updates.
        # Try moving the physics update post the change in self.dx variables
        # and the bug of the player standing on the moving platform appears.
        self.physics.update()

        xBoundA, yBoundA = self.A
        xBoundB, yBoundB = self.B

        if self.rect.x > xBoundB and self.isDirectionX:
            self.dx *= -1
            self.isDirectionX = False
        if self.rect.x < xBoundA and not self.isDirectionX:
            self.dx *= -1
            self.isDirectionX = True

        if self.rect.y > yBoundB and self.isDirectionY:
            self.dy *= -1
            self.isDirectionY = False
        if self.rect.y < yBoundA and not self.isDirectionY:
            self.dy *= -1
            self.isDirectionY = True

        self.physics.addDisplacementX("move", self.dx)
        self.physics.addDisplacementY("move", self.dy)

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))


class Switch(SceneEntity):
    """
    A switch entity that the player can turn on and off.
    """

    def __init__(self, x, y, switchNum, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param switchNum: Integer, identifying the number of the button.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        self.rect = pg.Rect(x, y, 0, 0)
        self.buttonNum = switchNum
        self.isOn = True

        button = sceneResources["buttons"]
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

    def __init__(self, x, y, doorNum, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param doorNum: Integer, identifying the number of the button.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        self.rect = pg.Rect(x, y, 0, 0)
        self.doorNum = doorNum
        self.switchesWaiting = None
        self.isClosed = True

        button = sceneResources["doors"]
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
                except AttributeError:
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


class Spike(SceneEntity):
    """
    A spike entity that kills the player.
    """

    def __init__(self, x, y, blocks, orientation, image, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param image: pygame.Surface, the image of the wall.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        super().__init__(screen)
        self.image = replicate(blocks, orientation, image)
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def drawWithCamera(self, camera):
        self.screen.blit(self.image, camera.apply(self))
