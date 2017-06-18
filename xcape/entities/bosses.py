"""
Contains the pig boss character.
"""

import random

import pygame as pg
from pygame.math import Vector2

import xcape.components.dialogue as dialogue
from xcape.common.loader import characterResources
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent
from xcape.components.cutscenes import Dialogue
from xcape.components.physics import PhysicsComponent


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

        self._initialisePhysics()
        self._initialiseAnimations()
        self._initialiseDialogues()
        self._initialiseAI()

    def _initialisePhysics(self):
        self.physics = PhysicsComponent(self)
        self.physics.isGravity = False
        self.jumpSpeed = -15
        self.moveSpeed = 1

    def _initialiseAnimations(self):
        pig = characterResources["pig"]
        self.animation = AnimationComponent(self, enableOrientation=True)
        self.animation.add("idle", [pig["running"][0]], float('inf'))
        self.animation.add("running", pig["running"], 400)
        self.animation.scaleAll(self.rect.size)

    def _initialiseDialogues(self):
        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.BOSS_0, 0, 0)
        self.dialogue.add(dialogue.BOSS_1, 0, 0)
        self.dialogue.add(dialogue.BOSS_2, 0, 0)
        self.dialogue.add(dialogue.BOSS_3, 0, 0)
        self.dialogue.add(dialogue.BOSS_4, 0, 0)
        self.dialogue.index = 0
        self.dialogueOrigin = pg.time.get_ticks()
        self.dialogueDuration = 5000

    def _initialiseAI(self):
        self.AIState = "thinking"
        self.attackDirectionX = "right"
        self.attackDirectionY = "down"
        self.following = None
        self.targets = []

        self._attackTimer = 0
        self.attacksDone = 0
        self.attacksMax = 3

        self.attackPatterns = None
        self.attackLoci = None
        self.attackPoint = None
        self.attackSpeed = None
        self.attackSpeedMin = 10
        self.attackSpeedMax = 20
        self.attackTravelled = 0

        self.chaseSpeed = 10
        self.chaseRadius = 200
        self.retreatSpeed = 10
        self.retreatRadius = 200

    def generatePatterns(self):
        """
        Generates the attack patterns.

        :return: Dictionary, mapping attack name to a list of points.
        """
        patterns = \
        {
            "square": [(0, 100), (100, 0), (0, -100), (-100, 0)],
            "triangle": [(100, 100), (100, -100), (-200, 0)]
        }

        return patterns

    def update(self):
        self.updateAIState()
        self.updateDialogueState()
        self.updateAnimationState()
        self.physics.update()

    def updateAIState(self):
        """
        Updates the state of AI.
        """
        if self.AIState == "thinking":
            self.initiateAttack()

        if self.AIState == "chase":
            self.chase(self.chaseRadius, self.chaseSpeed)

        if self.AIState == "retreat":
            self.retreat(self.retreatRadius, self.retreatSpeed)

        if self.AIState == "attack":
            print(self.attackSpeed)
            self.attack(self.attackPoint,
                        self.attackSpeed,
                        self.physics.travelled - self.travelOffset)

    def updateDialogueState(self):
        """
        Updates the state of dialogue.
        """
        elapsed = pg.time.get_ticks()

        # Changes the dialogue line every three seconds
        if abs(elapsed - self.dialogueOrigin) > self.dialogueDuration:
            self.dialogueOrigin = pg.time.get_ticks()
            r = random.randint(0, len(self.dialogue.bubbles)-1)
            # Hacky method to increase the chance for the 0th dialogue to proc
            zero = random.randint(0, 1)

            if zero == 0 or r == 0:
                self.dialogue.index = 0
            else:
                self.dialogue.index = r

        # Forces the dialogue bubble to follow the boss
        x, y = self.rect.center
        currentBubble = self.dialogue.bubbles[self.dialogue.index]
        if self.orientation == "right":
            currentBubble.rect.center = (x+80, y-55)
        if self.orientation == "left":
            currentBubble.rect.center = (x-15, y-55)

    def updateAnimationState(self):
        """
        Updates the state of the animation.
        """
        if self.physics.velocity.x > 0:
            self.state = "running"
            self.orientation = "right"

        if self.physics.velocity.x < 0:
            self.state = "running"
            self.orientation = "left"

        if self.physics.velocity.y > 0:
            self.state = "running"

        if self.physics.velocity.x > 0:
            self.state = "running"

        self.animation.update()

    def handleEvent(self, event):
        pass

    def drawWithCamera(self, camera):
        """
        Draws the character on the screen, shifted by the camera.

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        self.animation.drawWithCamera(camera)
        self.dialogue.drawWithCamera(camera)

    def initiateAttack(self):
        """
        Initialises the attacking state of the character.
        """
        self.AIState = "attack"
        self.travelOffset = self.physics.travelled

        if not self.attackPatterns:
            self.attackPatterns = self.generatePatterns()

        if not self.attackLoci:
            _, self.attackLoci = self.attackPatterns.popitem()
            self.attackSpeed = random.randint(self.attackSpeedMin,
                                              self.attackSpeedMax)

        self.attackPoint = self.attackLoci.pop()

    def target(self, gameObjects):
        """
        Sets the target that the boss is hunting.

        :param gameObjects: List, containing gameObject instances.
        """
        self.targets = gameObjects
        self.following = gameObjects[0]

    def retreat(self, radius, speed):
        """
        Retreats from the target if the target approaches too close.

        :param radius: Integer, the distance around the target to keep out.
        :param speed: Integer, the speed to retreat at.
        """
        x, y = self.rect.center
        xf, yf = self.following.rect.center

        d = Vector2(x - xf, y - yf)
        v = d.normalize()
        v.scale_to_length(speed)

        if not d.length() > radius:
            self.physics.fixVelocityX(v.x)
            self.physics.fixVelocityY(v.y)
        else:
            self.physics.fixVelocityX(0)
            self.physics.fixVelocityY(0)
            self.AIState = "thinking"

    def chase(self, radius, speed):
        """
        Chases the target until the target is too close.

        :param radius: Integer, the distance around the target to keep within.
        :param speed: Integer, the speed to chase at.
        """
        x, y = self.rect.center
        xf, yf = self.following.rect.center

        d = Vector2(x - xf, y - yf)
        v = d.normalize()
        v.scale_to_length(speed)

        if d.length() > radius:
            self.physics.fixVelocityX(-v.x)
            self.physics.fixVelocityY(-v.y)
        else:
            self.physics.fixVelocityX(0)
            self.physics.fixVelocityY(0)
            self.AIState = "thinking"

    def attack(self, translate, speed, travelled):
        """
        Moves from the current location by the translation amount. The attack
        aspect is intended from the collision with any targets on the way.

        :param translate: 2-Tuple, the amount to translate by.
        :param speed: Integer, the speed to move while attacking.
        :param travelled: Integer, the distance travelled from origin of attack.
        """
        d = Vector2(translate)
        v = d.normalize()
        v.scale_to_length(speed)
        self.physics.fixVelocityX(v.x)
        self.physics.fixVelocityY(v.y)

        if travelled > d.length():
            self.physics.fixVelocityX(0)
            self.physics.fixVelocityY(0)
            self.AIState = "thinking"
