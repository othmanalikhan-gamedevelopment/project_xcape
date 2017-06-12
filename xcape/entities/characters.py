"""
Contains all the game characters.
"""

import random

import pygame as pg

from xcape.common.loader import characterResources
from xcape.common.loader import cutsceneResources
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent
from xcape.components.cutscenes import Dialogue
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

        self.isOnGround = False
        self.jumpSpeed = -12
        self.moveSpeed = 9

        self.physics = PhysicsComponent(self)

        cat = characterResources["cat"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", cat["idle"], float('inf'))
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

        pressed = pg.key.get_pressed()

        if pressed[pg.K_LEFT] and not pressed[pg.K_RIGHT]:
            self.moveLeft()
        if pressed[pg.K_RIGHT] and not pressed[pg.K_LEFT]:
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

        :param camera: Camera class, shifts the position of the drawn animation.
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
        self.state = "running"
        self.orientation = "left"
        self.physics.addDisplacementX("move", -self.moveSpeed)

    def moveRight(self):
        """
        Moves the character right.
        """
        self.state = "running"
        self.orientation = "right"
        self.physics.addDisplacementX("move", self.moveSpeed)

    def stop(self):
        """
        Stops the character.
        """
        self.state = "idle"
        self.physics.velocity.x = 0


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
        self.physics.isGravity = False


        pig = characterResources["pig"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", [pig["running"][0]], float('inf'))
        self.animation.add("running", pig["running"], 400)
        self.animation.scaleAll(self.rect.size)

        assets = cutsceneResources["assets"]
        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(assets["office_1.png"], 300, 300)


    # TODO:
    # 1. Add dialogues for the boss
    # 2. Make the boss do a long dash sweeping attack
    # 3. Make the boss do fake attacks from time to time
    # 4. Make the boss do a dunk attack from above
    def update(self):


        if abs(self.rect.x - self.following.rect.x) > 0:
            self.moveRight()
        else:
            self.stop()


        self.moveVertical()

        self.animation.update()
        self.physics.update()
        # print(self.physics.velocity)

    def handleEvent(self, event):
        pass

    def drawWithCamera(self, camera):
        """
        Draws the character on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)
        self.dialogue.draw()

    def follow(self, gameobject):
        """
        Sets the target that the boss is chasing.

        :param gameobject: GameObject instance, the game object to follow.
        """
        self.following = gameobject

    def moveVertical(self):
        """
        Moves the character vertically.
        """
        r = random.randint(1, 10)

        y1 = self.rect.top
        y2 = self.following.rect.top

        dy = y2 - y1

        # if r > 5:
        #     self.rect.y = self.following.rect.top + r
        # else:
        #     self.rect.y = self.following.rect.bottom + r

        self.rect.y = self.following.rect.top

    def moveRight(self):
        """
        Moves the character right.
        """
        self.physics.fixVelocityX(1)
        self.state = "running"
        self.orientation = "right"

    def stop(self):
        """
        Stops the character.
        """
        self.physics.fixVelocityX(0)

