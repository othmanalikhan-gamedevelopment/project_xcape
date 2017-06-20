"""
Contains all playable characters.
"""

import pygame as pg

import xcape.common.settings as settings
from xcape.common.loader import CHARACTER_RESOURCES
from xcape.common.object import GameObject
from xcape.components.physics import PhysicsComponent
from xcape.components.render import RenderComponent


class PlayerBase(GameObject, pg.sprite.Sprite):
    """
    The controllable character to be played.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, 0, 0)
        self.num = 0

        self.animationState = "idle"
        self.orientation = "right"
        self.lives = 5

        self.isOnGround = False
        self.jumpSpeed = -12
        self.moveSpeed = 9

        self.physics = PhysicsComponent(self)
        self.animation = RenderComponent(self, enableOrientation=True)

        self.keybinds = None

    def update(self):
        self.animation.update()
        self.physics.update()

        # Hacky solution to fix hit box sizes without tampering with the
        # animation images directly (too much effort at this point)
        w, h = self.rect.size
        self.rect.size = (w-10, h)

        pressed = pg.key.get_pressed()
        left = self.keybinds["move_left"]
        right = self.keybinds["move_right"]

        if pressed[left] and not pressed[right]:
            self.moveLeft()
        if pressed[right] and not pressed[left]:
            self.moveRight()

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.keybinds["jump"]:
                self.jump()

        if event.type == pg.KEYUP:
            if event.key == self.keybinds["move_left"]:
                self.stop()
            if event.key == self.keybinds["move_right"]:
                self.stop()

    def drawWithCamera(self, camera):
        """
        Draws the character on the screen, shifted by the camera.

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)

    def jump(self):
        """
        Makes the character jump.
        """
        if self.isOnGround:
            self.physics.velocity.y = self.jumpSpeed
            self.physics.addVelocityY("jump", self.jumpSpeed)
            self.isOnGround = False

    def moveLeft(self):
        """
        Moves the character left.
        """
        self.animationState = "running"
        self.orientation = "left"
        self.physics.addDisplacementX("move", -self.moveSpeed)

    def moveRight(self):
        """
        Moves the character right.
        """
        self.animationState = "running"
        self.orientation = "right"
        self.physics.addDisplacementX("move", self.moveSpeed)

    def stop(self):
        """
        Stops the character.
        """
        self.animationState = "idle"
        self.physics.velocity.x = 0


class PlayerOne(PlayerBase):
    """
    The controllable player one.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 50, 48)
        self.num = 1

        cat = CHARACTER_RESOURCES["cat_orange"]
        self.animation.add("idle", cat["idle"], float('inf'))
        self.animation.add("running", cat["running"], 400)
        self.animation.scaleAll(self.rect.size)

        self.keybinds = settings.KEYBINDS_P1


class PlayerTwo(PlayerBase):
    """
    The controllable player two.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 50, 48)
        self.num = 2

        cat = CHARACTER_RESOURCES["cat_blue"]
        self.animation.add("idle", cat["idle"], float('inf'))
        self.animation.add("running", cat["running"], 400)
        self.animation.scaleAll(self.rect.size)

        self.keybinds = settings.KEYBINDS_P2
