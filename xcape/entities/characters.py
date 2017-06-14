"""
Contains all the game characters.
"""

import random

import pygame as pg

import xcape.components.dialogue as dialogue
from xcape.common.loader import characterResources
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

        self.AIState = "chase"
        self.attackDirectionX = "right"
        self.attackDirectionY = "down"

        self.timer = 0
        self.attackDelay = 700

        self.isSweepAttack = False
        self.sweepDirection = "right"
        self.sweepOrigin = 0
        self.sweepsDone = 3

        self.physics = PhysicsComponent(self)
        self.physics.isGravity = False

        pig = characterResources["pig"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", [pig["running"][0]], float('inf'))
        self.animation.add("running", pig["running"], 400)
        self.animation.scaleAll(self.rect.size)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.BOSS_1, 0, 0)
        self.dialogue.add(dialogue.BOSS_2, 0, 0)
        self.dialogue.add(dialogue.BOSS_3, 0, 0)
        self.dialogue.add(dialogue.BOSS_4, 0, 0)
        self.dialogue.index = 1
        self.dialogueOrigin = pg.time.get_ticks()

    # TODO:
    # 4. Make the boss do a dunk attack from above
    def update(self):
        self.updateAttackDirectionX()
        self.updateAttackDirectionY()

        if self.AIState == "chase":
            if not self.inRangeX(200):
                self.chaseHorizontally(5)
            else:
                self.physics.fixVelocityX(0)

            if not self.inRangeY(10):
                self.chaseVertically(5)
            else:
                self.physics.fixVelocityY(0)

            if self.inRangeX(200) and self.inRangeY(10):
                self.AIState = "attack"
                self.timer = pg.time.get_ticks()

        if self.AIState == "attack":
            if pg.time.get_ticks() - self.timer > self.attackDelay:
                self.sweepAttack(10, 400)

        self.updateDialogue()
        self.animation.update()
        self.physics.update()

    def handleEvent(self, event):
        pass

    def drawWithCamera(self, camera):
        """
        Draws the character on the screen, shifted by the camera.

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)
        self.dialogue.drawWithCamera(camera)

    def updateDialogue(self):
        """
        Updates the dialogue of the boss.
        """
        elapsed = pg.time.get_ticks()

        # Changes the dialogue line every three seconds
        if abs(elapsed - self.dialogueOrigin) > 3000:
            self.dialogueOrigin = pg.time.get_ticks()
            r = random.randint(0, len(self.dialogue.bubbles)-1)
            self.dialogue.index = r

        # Forces the dialogue bubble to follow the boss
        x, y = self.rect.center
        currentBubble = self.dialogue.bubbles[self.dialogue.index]
        if self.orientation == "right":
            currentBubble.rect.center = (x+80, y-55)
        if self.orientation == "left":
            currentBubble.rect.center = (x-15, y-55)

    def updateAttackDirectionX(self):
        """
        Determines whether the target to attack is on the right or left.
        """
        isRight = self.rect.x - self.following.rect.x < 0
        isLeft = self.rect.x - self.following.rect.x > 0
        if isRight:
            self.attackDirectionX = "right"
        if isLeft:
            self.attackDirectionX = "left"

    def updateAttackDirectionY(self):
        """
        Determines whether the target to attack is up or down.
        """
        isUp = self.rect.y - self.following.rect.y < 0
        isDown = self.rect.y - self.following.rect.y > 0
        if isUp:
            self.attackDirectionY = "up"
        elif isDown:
            self.attackDirectionY = "down"

    def follow(self, gameobject):
        """
        Sets the target that the boss is chasing.

        :param gameobject: GameObject instance, the game object to follow.
        """
        self.following = gameobject

    def sweepAttack(self, speed, distance):
        """
        Attacks the target by moving horizontally towards the target at the
        given speed and over the specified distance.

        :param speed: Integer, the speed the character moves left.
        :param distance: Integer, the distance the attack lasts in pixels.
        """
        if not self.isSweepAttack:
            self.isSweepAttack = True
            self.sweepOrigin = self.rect.x
            self.sweepDirection = self.attackDirectionX

        if distance > abs(self.sweepOrigin - self.rect.x):
            if self.sweepDirection == "right":
                self.moveRight(speed)
            elif self.sweepDirection == "left":
                self.moveLeft(speed)

            # Proc to stop the sweep attack abruptly to confuse the player
            if random.randint(1, 200) == 1:
                self.AIState = "chase"
                self.isSweepAttack = False

        else:
            self.AIState = "chase"
            self.isSweepAttack = False

    def chaseVertically(self, speed):
        """
        Chases the target vertically.

        :param speed: Integer, the speed the character moves up.
        """
        if self.attackDirectionY == "up":
            self.moveUp(speed)
        elif self.attackDirectionY == "down":
            self.moveDown(speed)
        else:
            self.physics.fixVelocityY(0)

    def chaseHorizontally(self, speed):
        """
        Chases the target horizontally.

        :param speed: Integer, the speed the character moves up.
        """
        if self.attackDirectionX == "right":
            self.moveRight(speed)
        elif self.attackDirectionX == "left":
            self.moveLeft(speed)
        else:
            self.physics.fixVelocityX(0)

    def inRangeY(self, range):
        """
        Checks if the target is within range vertically.

        :param range: Integer, the amount of pixels until the following target.
        :return: Boolean, whether the target is close within the tolerance.
        """
        distance = abs(self.rect.y - self.following.rect.y)
        if range > distance:
            return True
        else:
            return False

    def inRangeX(self, range):
        """
        Checks if the target is within range horizontally.

        :param range: Integer, the amount of pixels until the following target.
        :return: Boolean, whether the target is close within the tolerance.
        """
        distance = abs(self.rect.x - self.following.rect.x)
        if range > distance:
            return True
        else:
            return False

    def moveUp(self, speed):
        """
        Moves the character up.

        :param speed: Integer, the speed the character moves up.
        """
        self.physics.fixVelocityY(speed)
        self.state = "running"

    def moveDown(self, speed):
        """
        Moves the character down.

        :param speed: Integer, the speed the character moves down.
        """
        self.physics.fixVelocityY(-speed)
        self.state = "running"

    def moveRight(self, speed):
        """
        Moves the character right.

        :param speed: Integer, the speed the character moves right.
        """
        self.physics.fixVelocityX(speed)
        self.state = "running"
        self.orientation = "right"

    def moveLeft(self, speed):
        """
        Moves the character left.

        :param speed: Integer, the speed the character moves left.
        """
        self.physics.fixVelocityX(-speed)
        self.state = "running"
        self.orientation = "left"
