"""
Contains all the entities in a scene (excluding the players and bosses).
"""

import pygame as pg

from xcape.common.loader import SCENE_RESOURCES, SFX_RESOURCES
from xcape.common.object import GameObject
from xcape.components.audio import AudioComponent
from xcape.components.physics import PhysicsComponent
from xcape.components.render import RenderComponent, buildParts, replicate


class Decoration(GameObject):
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
        self.screen = screen
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"
        self.rect = pg.Rect(x, y, 0, 0)

    def __str__(self):
        return "decoration"

    def update(self):
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)


class Wall(GameObject):
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
        self.screen = screen

        if len(images) == 3:
            image = buildParts(blocks, orientation, images)
        elif len(images) == 1:
            image = replicate(blocks, orientation, images[0])
        else:
            raise ValueError("A wall must have one or three images only!")

        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"
        self.rect = pg.Rect(x, y, 0, 0)

    def __str__(self):
        return "wall"

    def update(self):
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)


class SPlatform(GameObject):
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
        self.screen = screen

        left = SCENE_RESOURCES["platforms"]["platform_1"][0]
        mid = SCENE_RESOURCES["platforms"]["platform_2"][0]
        right = SCENE_RESOURCES["platforms"]["platform_3"][0]
        image = buildParts(blocks, "h", [left, mid, right])

        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"
        self.rect = pg.Rect(x, y, 0, 0)

    def __str__(self):
        return "static_platform"

    def update(self):
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)


class DPlatform(GameObject):
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
        self.screen = screen

        left = SCENE_RESOURCES["platforms"]["platform_1"][0]
        mid = SCENE_RESOURCES["platforms"]["platform_2"][0]
        right = SCENE_RESOURCES["platforms"]["platform_3"][0]
        image = buildParts(blocks, "h", [left, mid, right])

        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"
        self.rect = pg.Rect(x, y, 0, 0)

    def __str__(self):
        return "directional_platform"

    def update(self):
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)


class MPlatform(GameObject):
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
        self.screen = screen
        self.A = A
        self.B = B
        self.dx = dx
        self.dy = dy
        self.isDirectionX = True
        self.isDirectionY = True

        self.physics = PhysicsComponent(self)
        self.physics.isGravity = False

        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"
        self.rect = pg.Rect(A[0], A[1], 0, 0)

    def __str__(self):
        return "moving_platform"

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

        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)


class Switch(GameObject):
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
        self.screen = screen
        self.num = switchNum
        self.isOn = True

        button = SCENE_RESOURCES["buttons"]
        self.render = RenderComponent(self, enableRepeat=False)
        self.render.add("on", [button["switch"][0]])
        self.render.add("off", button["switch"], 500)
        self.render.state = "on"
        self.rect = pg.Rect(x, y, 0, 0)

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("click", SFX_RESOURCES["scene_switch"])

    def __str__(self):
        return "switch " + str(self.num)

    def update(self):
        self.render.update()
        self.audio.update()

    def draw(self, camera=None):
        self.render.draw(camera)

    def turnOff(self):
        """
        Changes the state of the button to off and sends out an event.
        """
        self.isOn = False
        self.render.state = "off"
        self.audio.state = "click"
        self.messageScene("switch", (self.num, self.isOn))


class Door(GameObject):
    """
    A door entity that the player can enter.
    """

    def __init__(self, x, y, num, screen):
        """
        :param x: Integer, the x-position of the wall.
        :param y: Integer, the y-position of the wall.
        :param num: Integer, identifying the number of the button.
        :param screen: pygame.Surface, the screen to draw the wall onto.
        """
        self.screen = screen
        self.num = num
        self.switchesWaiting = []
        self.isClosed = True

        door = SCENE_RESOURCES["doors"]
        self.render = RenderComponent(self, enableRepeat=False)
        self.render.add("open", door["open"])
        self.render.add("closed", door["close"])
        self.render.state = "closed"
        self.rect = pg.Rect(x, y, 0, 0)

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("open", SFX_RESOURCES["scene_door"])

    def __str__(self):
        return "door_{}".format(self.num)

    def handleEvent(self, event):
        if event.type == self.SCENE_EVENT:
            if event.category == "switch":

                try:
                    switchNum, isOn = event.data
                    self.switchesWaiting.remove(switchNum)
                    if not self.switchesWaiting:
                        self.openDoor()
                except ValueError:
                    print("'{}' is safely ignoring switch number {}"
                          .format(self.__str__(), switchNum))
                except AttributeError:
                    print("'{}' is not a valid switch number!".format(switchNum))

    def update(self):
        self.render.update()
        self.audio.update()

    def draw(self, camera=None):
        self.render.draw(camera)

    def openDoor(self):
        """
        Changes the state of the door to open and sends out an event.
        """
        self.isClosed = False
        self.render.state = "open"
        self.audio.state = "open"
        self.messageScene("door", (self.num, self.isClosed))


class Spike(GameObject):
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
        self.screen = screen

        image = replicate(blocks, orientation, image)
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"
        self.rect = pg.Rect(x, y, 0, 0)

    def update(self):
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)
