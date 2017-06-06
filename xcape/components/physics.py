"""
Responsible for applying physics on a game object.
"""
from pygame.math import Vector2


class PhysicsComponent:
    """
    Represents the physics component that can apply physics to a game object.

    The units for the physics variables are listed below.

        Distance:   pixels.
        Velocity:   pixels per game tick.
        Time:       game tick.
    """

    def __init__(self, gameObject):
        """
        A simple constructor.

        :param gameObject: GameObject Class, representing any object within the
        game.
        """
        self.gameObject = gameObject
        self.velocity = Vector2(0, 0)
        self.gravity = Vector2(0, 0.8)
        self.jumpSpeed = -15
        self.moveSpeed = 10
        self.maxSpeed = 20
        self.TIME_STEP = 60
        self.counter = 0

    def update(self):
        """
        Applies the physics on the game object.
        """
        self.counter += 1

        if self.counter % self.TIME_STEP == 0:
            # self.applyGravity()
            self.limitSpeed()

            self.gameObject.rect.x += self.velocity.x
            self.gameObject.rect.y += self.velocity.y

            self.counter = 0

    def applyGravity(self):
        """
        Applies gravity on the game object.
        """
        self.velocity.y += self.gravity.y

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
                self.gameObject.velocity.x = -self.maxSpeed

        if abs(self.velocity.y) > self.maxSpeed:
            if self.velocity.y > 0:
                self.velocity.y = self.maxSpeed
            else:
                self.velocity.y = -self.maxSpeed
