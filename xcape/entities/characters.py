"""
Contains all the game characters.
"""

import pygame as pg

from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent
from xcape.components.physics import PhysicsComponent


class Player(GameObject, pg.sprite.Sprite):
    """
    The controllable character to be played.
    """

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        super().__init__()
        self.screen = screen
        self.resources = resources
        self.rect = pg.Rect(0, 0, 50, 48)

        self.state = "idle"
        self.orientation = "right"
        self.lives = 3
        self.canJump = True
        self.jumpSpeed = -15
        self.moveSpeed = 10

        cat = self.resources["cat"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", [cat["idle.png"]], float('inf'))
        self.animation.add("running", cat["running"], 400)
        self.animation.scaleAll(self.rect.size)

        self.physics = PhysicsComponent(self)

        self.keybinds = \
            {
                "jump": pg.K_UP,
                "move_left": pg.K_LEFT,
                "move_right": pg.K_RIGHT,
            }

    def update(self):
        self.animation.update()
        self.physics.update()

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == self.keybinds["jump"]:
                self.jump()
            if event.key == self.keybinds["move_left"]:
                self.moveLeft()
            if event.key == self.keybinds["move_right"]:
                self.moveRight()

        if event.type == pg.KEYUP:
            if event.key == self.keybinds["move_left"]:
                self.stopLeft()
            if event.key == self.keybinds["move_right"]:
                self.stopRight()

    def drawWithCamera(self, camera):
        """
        Draws the player on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)

    def jump(self):
        """
        Makes the player jump.
        """
        if self.canJump:
            self.physics.velocity.y = self.jumpSpeed
            self.physics.addVelocityY("jump", self.jumpSpeed)
            self.canJump = False

    def moveLeft(self):
        """
        Moves the player left.
        """
        if self.state == "running" and self.orientation == "right":
            self.physics.addVelocityX("move", -self.moveSpeed * 2)
        else:
            self.physics.addVelocityX("move", -self.moveSpeed)

        self.state = "running"
        self.orientation = "left"

    def moveRight(self):
        """
        Moves the player right.
        """
        if self.state == "running" and self.orientation == "left":
            self.physics.addVelocityX("move", self.moveSpeed * 2)
        else:
            self.physics.addVelocityX("move", self.moveSpeed)

        self.state = "running"
        self.orientation = "right"

    def stopLeft(self):
        """
        Stops the player if the player is moving left.
        """
        if self.state == "running" and self.orientation == "left":
            self.physics.velocity.x = 0
            self.state = "idle"

    def stopRight(self):
        """
        Stops the player if the player is moving right.
        """
        if self.state == "running" and self.orientation == "right":
            self.physics.velocity.x = 0
            self.state = "idle"
