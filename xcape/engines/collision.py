"""
The collision engine of the game.
"""
import pygame as pg
from pygame.math import Vector2

import xcape.common.events as events
from xcape.common.object import GameObject


class CollisionEngine(GameObject):
    """
    A specialised collision engine that handles collisions between all
    entities in a scene, including the player collisions.
    """

    def __init__(self, player, scene):
        """
        :param player: Player Class, representing the player.
        :param scene: Scene Class, representing a level.
        """
        self.player = player
        self.scene = scene

    def eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.resolveDoorCollisions()

    def update(self):
        self.resolveWallCollisions()
        self.resolveSPlatformCollisions()
        self.resolveDPlatformCollisions()
        self.resolveMPlatformCollisions()
        self.resolveSwitchCollisions()
        self.resolveSpikeCollisions()
        # self.checkScenarioBoundaryCollision()

    def resolveWallCollisions(self):
        """
        Resolves any wall collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.walls, False)
        for wall in hits:
            direction = self._checkCollisionDirection(self.player, wall)

            if direction == "bottom":
                self.player.rect.bottom = wall.rect.top
                self.player.physics.velocity.y = 0
                self.player.canJump = True

            elif direction == "left":
                self.player.rect.left = wall.rect.right

            elif direction == "top":
                self.player.rect.top = wall.rect.bottom

            elif direction == "right":
                self.player.rect.right = wall.rect.left

    def resolveSPlatformCollisions(self):
        """
        Resolves any static platform collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.sPlatforms, False)

        for platform in hits:
            direction = self._checkCollisionDirection(self.player, platform)

            if direction == "bottom":
                self.player.rect.bottom = platform.rect.top
                self.player.canJump = True
                self.player.physics.velocity.y = 0

            elif direction == "left":
                self.player.rect.left = platform.rect.right

            elif direction == "top":
                self.player.rect.top = platform.rect.bottom

            elif direction == "right":
                self.player.rect.right = platform.rect.left

    def resolveDPlatformCollisions(self):
        """
        Resolves any directional platform collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.dPlatforms, False)

        for platform in hits:
            direction = self._checkCollisionDirection(self.player, platform)

            if direction == "bottom":
                tol = abs(self.player.rect.bottom - platform.rect.top)
                if tol < 30:
                    self.player.rect.bottom = platform.rect.top
                    self.player.canJump = True

                    # Allows conversation of velocity if the player jumps through
                    if self.player.physics.velocity.y > 0:
                        self.player.physics.velocity.y = 0

    def resolveMPlatformCollisions(self):
        """
        Resolves any moving platform collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.mPlatforms, False)

        for platform in hits:
            direction = self._checkCollisionDirection(self.player, platform)

            if direction == "bottom":
                self.player.rect.bottom = platform.rect.top
                self.player.canJump = True
                self.player.physics.velocity.y = 0

            elif direction == "left":
                self.player.rect.left = platform.rect.right

            elif direction == "top":
                self.player.rect.top = platform.rect.bottom

            elif direction == "right":
                self.player.rect.right = platform.rect.left

            self.player.rect.x += platform.dx
            self.player.rect.y += platform.dy

    def resolveSwitchCollisions(self):
        """
        Resolves any switch collisions.
        """
        switchesOn = [s for s in self.scene.switches if s.isOn]
        for s in switchesOn:
            if pg.sprite.collide_rect(self.player, s):
                if (self.player.physics.velocity.x != 0 or
                        self.player.physics.velocity.y != 0):
                    s.turnOff()

    def resolveDoorCollisions(self):
        """
        Resolves any door collisions.
        """
        doorsClosed = [d for d in self.scene.doors if d.isClosed]
        hits = pg.sprite.spritecollide(self.player, self.scene.doors, False)

        if hits and not doorsClosed:
            events.messageScene("collision_engine",
                                "transition",
                                self.scene.levelNum + 1)

    def resolveSpikeCollisions(self):
        """
        Resolves any spike collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.spikes, False)

        if hits:
            events.messageScene("collision_engine", "death")

    def _checkCollisionDirection(self, moving, static):
        """
        Checks if the moving game object has collided with the static game
        object, and determines the direciton of collision.

        :param moving: GameObject class, representing a moving game object.
        :param static: GameObject class, representing a static game object.
        :return: String, whether 'bottom', 'left', 'top', or 'right'.
        """
        if pg.sprite.collide_rect(moving, static):
            # Defining points on the static game object
            x, y = static.rect.center
            S00 = static.rect.topleft
            S10 = static.rect.topright
            S11 = static.rect.bottomright
            S01 = static.rect.bottomleft

            # Defining points on the moving game object
            u, v = moving.rect.center
            M00 = moving.rect.topleft
            M10 = moving.rect.topright
            M11 = moving.rect.bottomright
            M01 = moving.rect.bottomleft

            # Defining vectors on the static game object which will be used in
            # accurate collision handling. The vectors are from the center of
            # the game object to its corners.
            vec_M00 = Vector2(x - S00[0], y - S00[1])
            vec_M10 = Vector2(x - S10[0], y - S10[1])
            vec_M11 = Vector2(x - S11[0], y - S11[1])
            vec_M01 = Vector2(x - S01[0], y - S01[1])

            # Defining variables for our new coordinate system based on angles
            # (which is mathematically equivalent to bearings)
            FULL_ROTATION = 360
            origin = vec_M00

            # Calculating angles of the static game object vectors
            angle_00 = origin.angle_to(vec_M00) % FULL_ROTATION
            angle_10 = origin.angle_to(vec_M10) % FULL_ROTATION
            angle_11 = origin.angle_to(vec_M11) % FULL_ROTATION
            angle_01 = origin.angle_to(vec_M01) % FULL_ROTATION

            # Calculating the displacement angle between the moving and
            # static game objects
            displacement = Vector2(x - u, y - v)
            angle = origin.angle_to(displacement) % FULL_ROTATION

            # Calculating direction of the collision
            isCollideBottom = angle_00 < angle < angle_10
            isCollideLeft = angle_10 < angle < angle_11
            isCollideTop = angle_11 < angle < angle_01
            isCollideRight = angle_01 < angle

            if isCollideBottom:
                return "bottom"
            elif isCollideLeft:
                return "left"
            elif isCollideTop:
                return "top"
            elif isCollideRight:
                return "right"

    def checkScenarioBoundaryCollision(self):
        """
        Checks if the playerOne has 'fallen' out of the level.
        """
        background = self.scene.background.get_rect()
        boundary = pg.Rect(self.scene.worldShiftX,
                           self.scene.worldShiftY,
                           background.width,
                           background.height + 100)

        if not pg.Rect.contains(boundary, self.player):
            self.player.isHit = True
            self.player.lives -= 1
