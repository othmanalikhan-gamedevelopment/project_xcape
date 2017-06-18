"""
Responsible for applying physics on a game object.
"""
from collections import OrderedDict

from pygame.math import Vector2

from xcape.common.object import GameObject


class PhysicsComponent(GameObject):
    """
    Represents the physics component that can apply physics to a game object.

    The units for the physics variables are listed below.

    Displacement:       Pixels.
    Velocity:           Pixels per physics tick.
    Time:               Physics tick.
    """

    def __init__(self, gameObject):
        """
        :param gameObject: GameObject instance, representing any object within
        the game.
        """
        self.gameObject = gameObject
        self.displacement = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.maxSpeed = 20

        self.gravity = Vector2(0, 2)
        self.isGravity = True
        self.travelled = 0

        self._nameToDisX = OrderedDict()
        self._nameToDisY = OrderedDict()
        self._nameToVelX = OrderedDict()
        self._nameToVelY = OrderedDict()

        # Increasing the tick rate too much can cause choppiness!
        # This variable needs to be tweaked until it feels smooth enough.
        self.PHYSICS_TICK = 2
        self.tick = 0

    def update(self):
        self.tick += 1
        if self.tick % self.PHYSICS_TICK == 0:
            self.immediateUpdate()
            self.tick = 0

    def immediateUpdate(self):
        """
        Updates the physics immediately, ignoring the physics tick rate.
        """
        self.applyGravity()
        self.limitSpeed()

        self.applyNetVelocity()
        self.applyNetDisplacement()

    def applyNetDisplacement(self):
        """
        Applies the resultant displacement vector.
        """
        self.displacement.x += sum(self._nameToDisX.values())
        self.displacement.y += sum(self._nameToDisY.values())
        self.gameObject.rect.x += self.displacement.x
        self.gameObject.rect.y += self.displacement.y
        self.travelled += self.displacement.length()

        # Displacement applied is NOT conserved
        self._nameToDisX.clear()
        self._nameToDisY.clear()
        self.displacement.x = 0
        self.displacement.y = 0

    def addDisplacementX(self, name, amount):
        """
        Adds a new displacement component along the x-axis.

        :param name: String, the name of the displacement being applied.
        :param amount: Number, the amount of displacement to add.
        """
        self._nameToDisX[name] = amount

    def addDisplacementY(self, name, amount):
        """
        Adds a new displacement component along the y-axis.

        :param name: String, the name of the displacement being applied.
        :param amount: Number, the amount of displacement to add.
        """
        self._nameToDisY[name] = amount

    def applyNetVelocity(self):
        """
        Applies the resultant velocity vector.
        """
        self.velocity.x += sum(self._nameToVelX.values())
        self.velocity.y += sum(self._nameToVelY.values())
        self.gameObject.rect.x += self.velocity.x
        self.gameObject.rect.y += self.velocity.y
        self.travelled += self.velocity.length()

        self._nameToVelX.clear()
        self._nameToVelY.clear()

    def addVelocityX(self, name, amount):
        """
        Adds a new velocity component along the x-axis.

        :param name: String, the name of the velocity being applied.
        :param amount: Number, the amount of velocity to add.
        """
        self._nameToVelX[name] = amount

    def addVelocityY(self, name, amount):
        """
        Adds a new velocity component along the y-axis.

        :param name: String, the name of the velocity being applied.
        :param amount: Number, the amount of velocity to add.
        """
        self._nameToVelY[name] = amount

    def fixVelocityX(self, amount):
        """
        Fixes the velocity component along the x-axis to be constant.

        :param amount: Number, the amount of velocity to add.
        """
        self._nameToVelX.clear()
        self.velocity.x = amount

    def fixVelocityY(self, amount):
        """
        Fixes the velocity component along the y-axis to be constant.

        :param amount: Number, the amount of velocity to add.
        """
        self._nameToVelX.clear()
        self.velocity.y = amount

    def applyGravity(self):
        """
        Applies gravity on the game object.
        """
        if self.isGravity:
            self.addVelocityY("gravity", self.gravity.y)

    def limitSpeed(self):
        """
        Sets a maximum velocity on the game object.

        This is important otherwise very fast velocities can cause game
        objects to pass through blocks, bypassing the collision checker.
        """
        if abs(self.velocity.x) > self.maxSpeed:
            if self.velocity.x > 0:
                self.velocity.x = self.maxSpeed
            else:
                self.velocity.x = -self.maxSpeed

        if abs(self.velocity.y) > self.maxSpeed:
            if self.velocity.y > 0:
                self.velocity.y = self.maxSpeed
            else:
                self.velocity.y = -self.maxSpeed
