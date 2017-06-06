"""
The collision engine of the game.
"""
import pygame as pg
from pygame.math import Vector2

# from sprites import MovingPlatform, TransparentPlatform
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
            if event.key == pg.K_SPACE or event.key == pg.K_UP:
                self.checkDoorCollision()

    def update(self):
        self.ResolveWallCollisions()
        self.ResolvePlatformCollisions()
        # self.checkPlatformCollision()
        # self.checkButtonCollision()
        # self.checkEnemyCollision()
        # self.checkScenarioBoundaryCollision()

    def ResolveWallCollisions(self):
        """
        Resolves any wall collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.walls, False)
        for wall in hits:
            direction = self.CheckCollisionDirection(self.player, wall)

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

    def ResolvePlatformCollisions(self):
        """
        Resolves any platform collisions.
        """
        hits = pg.sprite.spritecollide(self.player, self.scene.platforms, False)
        for platform in hits:
            direction = self.CheckCollisionDirection(self.player, platform)

            if direction == "bottom":
                self.player.rect.bottom = platform.rect.top
                self.player.physics.velocity.y = 0
                self.player.canJump = True

            elif direction == "left":
                self.player.rect.left = platform.rect.right

            elif direction == "top":
                self.player.rect.top = platform.rect.bottom

            elif direction == "right":
                self.player.rect.right = platform.rect.left

    def checkPlatformCollision(self):
        """
        Checks if the playerOne has collided with any platform in the scenario and
        updates accordingly.
        """
        hitStatic = pg.sprite.spritecollide(self.player,
                                            self.scene.platStatic,
                                            False)
        hitMoving = pg.sprite.spritecollide(self.player,
                                            self.scene.platMoving,
                                            False)
        hitTransparent = pg.sprite.spritecollide(self.player,
                                                 self.scene.platTransparent,
                                                 False)
        hits = hitStatic + hitMoving + hitTransparent

        for plat in hits:

            if isinstance(plat, TransparentPlatform):
                tol = abs(self.player.rect.bottom - plat.rect.top)

                if isCollideBottom:
                    self.player.rect.bottom = plat.rect.top
                    self.player.canJump = True

                    if self.player.physics.velocity.y > 0:
                        self.player.physics.velocity.y = 0

                elif isCollideTop and tol < 10:
                    self.player.rect.bottom = plat.rect.top

            else:
                # Moves the playerOne if the playerOne is on a moving platform
                if isinstance(plat, MovingPlatform):
                    self.player.rect.x += plat.moveX * 2
                    self.player.rect.y += plat.moveY

    def CheckCollisionDirection(self, moving, static):
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

    def checkButtonCollision(self):
        """
        Checks if the playerOne has collided with any button in the scenario and
        updates accordingly.
        """
        hits = pg.sprite.spritecollide(self.player,
                                       self.scene.buttonsOff,
                                       True)
        if hits:
            if self.player.physics.velocity.x != 0 or \
                            self.player.physics.velocity.y != 0:
                print("abrir")
                self.scene.isButtonOn = True

    def checkDoorCollision(self):
        """
        Checks if the playerOne has collided with any door in the scenario and
        updates accordingly.
        """
        hits = pg.sprite.spritecollide(self.player,
                                       self.scene.doorsOpen,
                                       False)
        if hits and self.scene.isDoorOpen:
            print("entrar")
            self.scene.isEnd = True

    def checkEnemyCollision(self):
        """
        Checks if the playerOne has collided with any enemy or harmful object
        in the scenario and updates accordingly.
        """
        enemy_hit = pg.sprite.spritecollide(self.player,
                                            self.scene.enemies,
                                            False)

        if enemy_hit:
            print("choque")
            self.player.lives -= 1
            self.player.isHit = True

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
