"""
The collision engine of the game.
"""
import pygame as pg
from pygame.math import Vector2

import xcape.common.events as events
from xcape.common.object import GameObject


class CollisionEngine(GameObject):
    """
    A specialised (non-scalable) collision engine that handles collisions
    between all entities in a scene.
    """

    def __init__(self, scene):
        """
        :param scene: Scene Class, representing a level.
        """
        self.scene = scene

    def eventHandler(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.resolveDoorCollisions()

    def update(self):
        self.resolveWallCollisions()
        self.resolveSwitchCollisions()

        self.resolveSPlatformCollisions()
        self.resolveDPlatformCollisions()
        self.resolveMPlatformCollisions()

        self.resolveSpikeCollisions()
        # self.resolveBossCollisions()
        self.resolveBoundaryCollision()

    def resolveWallCollisions(self):
        """
        Resolves any wall collisions.
        """
        for player in self.scene.players:
            self._resolveBasicCollision(player, self.scene.walls)

    def resolveSPlatformCollisions(self):
        """
        Resolves any static platform collisions.
        """
        for player in self.scene.players:
            self._resolveBasicCollision(player, self.scene.sPlatforms)

    def resolveDPlatformCollisions(self):
        """
        Resolves any directional platform collisions.
        """
        for player in self.scene.players:

            hits = pg.sprite.spritecollide(player, self.scene.dPlatforms, False)
            for platform in hits:
                direction = self._checkCollisionDirection(player, platform)

                if direction == "bottom":
                    tol = abs(player.rect.bottom - platform.rect.top)
                    if tol < 30:
                        player.rect.bottom = platform.rect.top
                        player.canJump = True

                        # Allows conversation of velocity if the player jumps through
                        if player.physics.velocity.y > 0:
                            player.physics.velocity.y = 0

    def resolveMPlatformCollisions(self):
        """
        Resolves any moving platform collisions.
        """
        for player in self.scene.players:

            hits = pg.sprite.spritecollide(player, self.scene.mPlatforms, False)
            for platform in hits:
                direction = self._checkCollisionDirection(player, platform)

                if direction == "bottom":
                    player.rect.bottom = platform.rect.top
                    player.canJump = True
                    player.physics.velocity.y = 0

                elif direction == "left":
                    player.rect.left = platform.rect.right

                elif direction == "top":
                    player.rect.top = platform.rect.bottom

                elif direction == "right":
                    player.rect.right = platform.rect.left

                # TODO: Update to use physics displacement functions instead
                player.rect.x += platform.dx
                player.rect.y += platform.dy

    def resolveSwitchCollisions(self):
        """
        Resolves any switch collisions.
        """
        switchesOn = [s for s in self.scene.switches if s.isOn]
        for s in switchesOn:

            for player in self.scene.players:
                if pg.sprite.collide_rect(player, s):
                    if (player.physics.velocity.x != 0 or
                            player.physics.velocity.y != 0):
                        s.turnOff()

    def resolveDoorCollisions(self):
        """
        Resolves any door collisions.
        """
        for player in self.scene.players:

            hits = pg.sprite.spritecollide(player, self.scene.doors, False)
            doorsClosed = [d for d in self.scene.doors if d.isClosed]
            if hits and not doorsClosed:
                events.messageScene("collision_engine",
                                    "transition",
                                    self.scene.levelNum + 1)

    def resolveSpikeCollisions(self):
        """
        Resolves any spike collisions.
        """
        for player in self.scene.players:

            hits = pg.sprite.spritecollide(player, self.scene.spikes, False)
            if hits:
                events.messageScene("collision_engine", "death")

    def resolveBossCollisions(self):
        """
        Resolves any boss collisions.
        """
        for player in self.scene.players:

            hits = pg.sprite.spritecollide(player, self.scene.bosses, False)
            if hits:
                events.messageScene("collision_engine", "death")

    def resolveBoundaryCollision(self):
        """
        Checks if the players have 'fallen' out of the level.
        """
        boundary = pg.Rect(-1000, -1000, 3000, 3000)

        for player in self.scene.players:
            if not pg.Rect.contains(boundary, player):
                events.messageScene("collision_engine", "death")

    def _checkCollisionDirection(self, moving, static):
        """
        Checks if the moving game object has collided with the static game
        object, and determines the direciton of collision.

        :param moving: GameObject instance, representing a moving game object.
        :param static: GameObject instance, representing a static game object.
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

    def _resolveBasicCollision(self, moving, group):
        """
        Resolves any collisions between a moving object and a group of
        objects such that the moving object cannot pass through such objects.

        :param moving: GameObject instance, representing a moving scene entity.
        :param group: List, containing GameObject instance in a scene.
        :return:
        """
        hits = pg.sprite.spritecollide(moving, group, False)

        for wall in hits:
            direction = self._checkCollisionDirection(moving, wall)

            if direction == "bottom":
                moving.rect.bottom = wall.rect.top
                moving.physics.velocity.y = 0
                moving.isOnGround = True

            elif direction == "left":
                moving.rect.left = wall.rect.right
                moving.physics.velocity.x = 0

            elif direction == "top":
                moving.rect.top = wall.rect.bottom
                moving.physics.velocity.y = 0

            elif direction == "right":
                moving.rect.right = wall.rect.left
                moving.physics.velocity.x = 0
