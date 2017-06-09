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

        Distance:   pixels.
        Velocity:   pixels per game tick.
        Time:       game tick.
    """

    def __init__(self, gameObject):
        """
        :param gameObject: GameObject Class, representing any object within the
        game.
        """
        self.gameObject = gameObject
        self.velocity = Vector2(0, 0)
        self.gravity = Vector2(0, 2)
        self.maxSpeed = 20
        self.isGravity = True
        self._nameToVelX = OrderedDict()
        self._nameToVelY = OrderedDict()

        # Increasing this variable too much can cause choppiness!
        # This variable needs to be tweaked until it feels smooth enough
        self.PHYSICS_TICK = 20
        self.tick = 0

    def update(self):
        self.tick += 1

        if self.tick % self.PHYSICS_TICK == 0:
            self.immediateUpdate()
            self.tick = 0

    def immediateUpdate(self):
        """
        Updates the physics immediately, ignoring the physics time step ticker.
        """
        self.applyGravity()
        self.limitSpeed()

        # Computing velocity
        self.velocity.x += sum(self._nameToVelX.values())
        self.velocity.y += sum(self._nameToVelY.values())

        # Computing displacement
        self.gameObject.rect.x += self.velocity.x
        self.gameObject.rect.y += self.velocity.y

        # Removing all velocity components applied (but the main velocity
        # vector variable is conserved)
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
