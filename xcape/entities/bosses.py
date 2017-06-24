"""
Contains the pig boss character.
"""

import random

import pygame as pg
from pygame.math import Vector2

import xcape.components.dialogue as dialogue
from xcape.common.loader import CHARACTER_RESOURCES, SFX_RESOURCES
from xcape.common.object import GameObject
from xcape.components.audio import AudioComponent
from xcape.components.physics import PhysicsComponent
from xcape.components.render import RenderComponent, Dialogue


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

        self._initialiseRenderer()
        self._initialiseAudio()
        self._initialisePhysics()
        self._initialiseDialogues()
        self._initialiseAI()

    def __str__(self):
        return "pig_boss"

    def handleEvent(self, event):
        print("{} is safely ignored event {}".format(self.__str__(), event))

    def update(self):
        self.updateRenderState()
        self.updateAudioState()
        self.updateDialogueState()
        self.updateAIState()
        self.physics.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.dialogue.draw(camera)

    def updateAudioState(self):
        """
        Adjusts the volume based on proximity to targets.
        """
        maxDistance = 500
        minVolume = 0.1
        scaleVolume = 0.5

        p1, p2 = self.targets
        x, y = self.rect.center
        x1, y1 = p1.rect.center
        x2, y2 = p2.rect.center

        d1 = Vector2(x - x1, y - y1)
        d2 = Vector2(x - x2, y - y2)
        distance = min(d1.length(), d2.length(), maxDistance)

        vol = max((minVolume, (1-(distance/maxDistance))*scaleVolume))
        self.audio.sound.set_volume(vol)
        self.audio.update()

    def updateRenderState(self):
        """
        Updates the rendering state based on physics.
        """
        if self.physics.velocity.x > 0:
            self.render.state = "running"
            self.render.orientation = "right"

        if self.physics.velocity.x < 0:
            self.render.state = "running"
            self.render.orientation = "left"

        if self.physics.velocity.y > 0:
            self.render.state = "running"

        if self.physics.velocity.x > 0:
            self.render.state = "running"

        self.render.update()

    def updateDialogueState(self):
        """
        Updates the state of dialogue based on random procs.
        """
        elapsed = pg.time.get_ticks()

        # Changes the dialogue line every three seconds
        if abs(elapsed - self.dialogueOrigin) > self.dialogueDuration:
            self.dialogueOrigin = pg.time.get_ticks()
            r = random.randint(0, len(self.dialogue.allBubbles) - 1)
            # Hacky solution to increase chances of proccing
            if r == 0 or random.randint(0, 1) == 0:
                self.dialogue.index = None
            else:
                self.dialogue.index = r

        # Forces the dialogue bubble to follow the boss
        if self.dialogue.index:
            x, y = self.rect.center
            currentBubble = self.dialogue.allBubbles[self.dialogue.index]
            if self.render.orientation == "right":
                currentBubble.rect.center = (x+10, y-55)
            if self.render.orientation == "left":
                currentBubble.rect.center = (x-80, y-55)

    def updateAIState(self):
        """
        Updates the state of AI.
        """
        if self.AIState == "no_aggro":
            isAggro = self.isInRange(self.following.rect.center, self.aggroRadius)
            if isAggro:
                self.AIState = "thinking"

        if self.AIState == "thinking":
            isNear = self.isInRange(self.following.rect.center, self.chaseRadius)
            isAttacking = self.attackLoci

            if not isNear and not isAttacking:
                self.AIState = "chase"
            else:
                self.initiateAttack()

        if self.AIState == "chase":
            self.chase(self.chaseRadius, self.chaseSpeed)

        if self.AIState == "retreat":
            self.retreat(self.retreatRadius, self.retreatSpeed)

        if self.AIState == "attack":
            self.attack(self.attackPoint,
                        self.attackSpeed,
                        self.physics.travelled - self.travelOffset)

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

    def isInRange(self, point, distance):
        """
        Checks whether the given point is within the specified distance.

        :param point: 2-Tuple, containing the x and y coordinates.
        :param distance: Number, the minimum distance to the point.
        :return: Boolean, true if within range otherwise false.
        """
        x, y = self.rect.center
        xp, yp = point

        d = Vector2(x - xp, y  - yp)

        if distance >= d.length():
            return True
        else:
            return False

    def initiateAttack(self):
        """
        Initialises the attacking state of the character.
        """
        self.AIState = "attack"
        self.travelOffset = self.physics.travelled

        if not self.attackPatterns:
            self.attackPatterns = self.generatePatterns(self.isSquarePattern,
                                                        self.isTrianglePattern,
                                                        self.isSpiralPattern,
                                                        self.isSweepPattern,
                                                        self.isStompPattern)
            p1, p2 = self.targets
            if self.following == p1:
                self.following = p2
            elif self.following == p2:
                self.following = p1

        if not self.attackLoci:
            nameToSpeed = \
                {
                    "sweep_right": 30,
                    "sweep_left": 30,
                    "stomp_bot": 30,
                    "stomp_top": 30,
                }
            try:
                name, self.attackLoci = self.attackPatterns.popitem()
                self.attackSpeed = nameToSpeed[name]
            except KeyError:
                self.attackSpeed = 15

        self.attackPoint = self.attackLoci.pop()
        self.audio.state = "attack"

    def generatePatterns(self,
                         isSquare=True,
                         isTriangle=True,
                         isSpiral=True,
                         isSweep=True,
                         isStomp=True):
        """
        Generates the attack patterns.

        :param isSquare: Boolean, whether to include the pattern.
        :param isTriangle: Boolean, whether to include the pattern.
        :param isSpiral: Boolean, whether to include the pattern.
        :param isSweep: Boolean, whether to include the pattern.
        :param isStomp: Boolean, whether to include the pattern.
        :return: Dictionary, mapping attack name to a list of points.
        """
        square = \
        {
            "square_right": [(0, 200), (200, 0), (0, -200), (-200, 0)],
            "square_left": [(0, -200), (-200, 0), (0, 200), (200, 0)],
        }
        triangle = \
        {
            "triangle_wave_right": 3*[(100, 100), (100, -100)],
            "triangle_wave_left": 3*[(-100, -100), (-100, 100)],
        }
        spiral = \
        {
            "spiral_top": [(150, 0), (0, 150), (-225, 0), (0, -225),
                           (68, 0), (0, 68), (-101, 0), (0, -101),
                           (30, 0), (0, 30), (-45, 0), (0, -45),
                           (10, 0), (0, 10), (-15, 0), (0, -15)],
            "spiral_bot": [(-150, 0), (0, -150), (225, 0), (0, 225),
                           (-68, 0), (0, -68), (101, 0), (0, 101),
                           (-30, 0), (0, -30), (45, 0), (0, 45),
                           (-10, 0), (0, -10), (15, 0), (0, 15)],
        }
        sweep = \
        {
            "sweep_left": 5*[(500, 0), (0, 50), (-500, 0), (0, 50)],
            "sweep_right": 5*[(-500, 0), (0, -50), (500, 0), (0, -50)],
        }
        stomp = \
        {
            "stomp_bot": 5*[(0, 300), (50, 0), (0, -300), (50, 0)],
            "stomp_top": 5*[(0, -300), (-50, 0), (0, 300), (-50, 0)],
        }

        patterns = {}
        if isSquare:
            patterns.update(square)
        if isTriangle:
            patterns.update(triangle)
        if isSpiral:
            patterns.update(spiral)
        if isSweep:
            patterns.update(sweep)
        if isStomp:
            patterns.update(stomp)
        return patterns

    def _initialiseRenderer(self):
        pig = CHARACTER_RESOURCES["pig"]
        self.render = RenderComponent(self, enableOrientation=True)
        self.render.add("idle", pig["running"][0])
        self.render.add("running", pig["running"], 400)
        self.render.scaleAll(self.rect.size)
        self.render.state = "running"
        self.render.orientation = "left"

    def _initialiseAudio(self):
        self.audio = AudioComponent(self,
                                    enableAutoPlay=False,
                                    enableRepeat=False)
        self.audio.add("machine", SFX_RESOURCES["pig_machine"])
        self.audio.add("attack", SFX_RESOURCES["pig_attack"])

        # Plays machine sonud endlessly
        self.audio.state = "machine"
        self.audio.sound.play(loops=-1)

    def _initialisePhysics(self):
        self.physics = PhysicsComponent(self)
        self.physics.isGravity = False
        self.physics.maxSpeed = 100
        self.jumpSpeed = -15
        self.moveSpeed = 1

    def _initialiseDialogues(self):
        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.BOSS_0, 0, 0)
        self.dialogue.add(dialogue.BOSS_1, 0, 0)
        self.dialogue.add(dialogue.BOSS_2, 0, 0)
        self.dialogue.add(dialogue.BOSS_3, 0, 0)
        self.dialogue.add(dialogue.BOSS_4, 0, 0)
        self.dialogue.index = None
        self.dialogueOrigin = pg.time.get_ticks()
        self.dialogueDuration = 5000

    def _initialiseAI(self):
        self.AIState = "no_aggro"
        self.following = None
        self.targets = []

        self.attackPatterns = None
        self.attackLoci = None
        self.attackPoint = None
        self.attackSpeed = 0
        self.attackTravelled = 0

        self.isSquarePattern = True
        self.isTrianglePattern = True
        self.isSpiralPattern = True
        self.isSweepPattern = True
        self.isStompPattern = True

        self.chaseSpeed = 7
        self.chaseRadius = 150
        self.retreatSpeed = 10
        self.retreatRadius = 200
        self.aggroRadius = 300

