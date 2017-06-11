"""
Contains all the game characters.
"""

import random

import pygame as pg

from xcape.common.loader import characterResources
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent
from xcape.components.physics import PhysicsComponent


class Player(GameObject, pg.sprite.Sprite):
    """
    The controllable character to be played.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, 50, 48)

        self.state = "idle"
        self.orientation = "right"
        self.lives = 3
        self.canJump = True
        self.jumpSpeed = -15
        self.moveSpeed = 10

        self.physics = PhysicsComponent(self)

        cat = characterResources["cat"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", [cat["idle.png"]], float('inf'))
        self.animation.add("running", cat["running"], 400)
        self.animation.scaleAll(self.rect.size)

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
        Draws the character on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)

    def jump(self):
        """
        Makes the character jump.
        """
        if self.canJump:
            self.physics.velocity.y = self.jumpSpeed
            self.physics.addVelocityY("jump", self.jumpSpeed)
            self.canJump = False

    def moveLeft(self):
        """
        Moves the character left.
        """
        if self.state == "running" and self.orientation == "right":
            self.physics.addVelocityX("move", -self.moveSpeed * 2)
        else:
            self.physics.addVelocityX("move", -self.moveSpeed)

        self.state = "running"
        self.orientation = "left"

    def moveRight(self):
        """
        Moves the character right.
        """
        if self.state == "running" and self.orientation == "left":
            self.physics.addVelocityX("move", self.moveSpeed * 2)
        else:
            self.physics.addVelocityX("move", self.moveSpeed)

        self.state = "running"
        self.orientation = "right"

    def stopLeft(self):
        """
        Stops the character if the character is moving left.
        """
        if self.state == "running" and self.orientation == "left":
            self.physics.velocity.x = 0
            self.state = "idle"

    def stopRight(self):
        """
        Stops the character if the character is moving right.
        """
        if self.state == "running" and self.orientation == "right":
            self.physics.velocity.x = 0
            self.state = "idle"


class PigBoss(GameObject, pg.sprite.Sprite):
    """
    The controllable character to be played.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        super().__init__()
        self.screen = screen
        self.rect = pg.Rect(0, 0, 100, 66)

        self.state = "idle"
        self.orientation = "right"
        self.jumpSpeed = -15
        self.moveSpeed = 1
        self.following = None

        self.physics = PhysicsComponent(self)
        # self.physics.PHYSICS_TICK = 70
        self.physics.isGravity = False

        pig = characterResources["pig"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", [pig["running"][0]], float('inf'))
        self.animation.add("running", pig["running"], 400)
        self.animation.scaleAll(self.rect.size)

    def update(self):
        r = random.randint(1, 100)

        x, y = self.following.rect.center
        u, v = self.rect.center

        dx = x - u
        dy = y - v

        move = pg.math.Vector2(dx, dy)
        move = move.normalize()

        # self.physics.velocity.x = move.x
        # self.physics.velocity.y = move.y
        self.physics.addVelocityX("move", move.x)
        self.physics.addVelocityY("move", move.y)
        print(dx, dy)

        # self.rect.x += dx * 0.001
        # self.rect.y += dy * 0.001

        # if r == 3:
        #     self.moveLeft()

        # if r == 4:
        #     self.moveRight()

        self.animation.update()
        self.physics.update()

    def handleEvent(self, event):
        pass

    def drawWithCamera(self, camera):
        """
        Draws the character on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)

    def follow(self, gameobject):
        """
        Sets the target that the boss is chasing.

        :param gameobject: GameObject Class, the game object to follow.
        """
        self.following = gameobject

    def moveLeft(self):
        """
        Moves the character left.
        """
        self.rect.x -= 3
        self.state = "running"
        self.orientation = "left"

    def moveRight(self):
        """
        Moves the character right.
        """
        self.rect.x += 3
        self.state = "running"
        self.orientation = "right"
