"""
Responsible for containing all the game characters.
"""
import pygame as pg

import xcape.common.events as events
import xcape.common.render as render
import xcape.common.settings as settings
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
        self.canJump = True
        self.lives = 3

        cat = self.resources["cat"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.addStatic("idle", cat["idle.png"])
        self.animation.addStatic("jumping", cat["idle.png"])
        self.animation.addDynamic("running", cat["running"], 1000)
        self.animation.scaleAll(self.rect.size)

        self.physics = PhysicsComponent(self)
        self.jumpSpeed = -1
        self.moveSpeed = 1

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
            if (event.key == self.keybinds["move_left"] and
                    self.physics.velocity.x < 0):
                self.stop()
            if (event.key == self.keybinds["move_right"]
                    and self.physics.velocity.x > 0):
                self.stop()

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
            self.canJump = False
            self.state = "jumping"

    def moveLeft(self):
        """
        Moves the player left.
        """
        self.physics.velocity.x = -self.moveSpeed
        self.state = "running"
        self.orientation = "left"

    def moveRight(self):
        """
        Moves the player right.
        """
        self.physics.velocity.x = self.moveSpeed
        self.state = "running"
        self.orientation = "right"

    def stop(self):
        """
        Stops the player.
        """
        self.physics.velocity.x = 0
        self.state = "idle"
