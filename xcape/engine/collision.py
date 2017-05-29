"""
Responsible for handling the collisions in the game.
"""
import pygame as pg
from pygame.math import Vector2

from sprites import MovingPlatform, TransparentPlatform


class CollisionEngine:
    """
    Represents the collision engine that handles collisions between a
    player and the scenario.
    """

    def __init__(self, player, scenario):
        """
        A simple constructor.

        :param player: Player Class, representing the playerOne game object.
        :param scenario: Scenario Class, representing a level game object.
        """
        self.player = player
        self.scenario = scenario

    def update(self):
        """
        Checks for collisions and handles appropriately.
        """
        self.checkPlatformCollision()
        self.checkButtonCollision()
        self.checkEnemyCollision()
        self.checkScenarioBoundaryCollision()

    def eventHandler(self, event):
        """
        Handles the supplied event.

        :param event: pygame.event, representing an triggered event.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_UP:
                self.checkDoorCollision()

    def checkPlatformCollision(self):
        """
        Checks if the playerOne has collided with any platform in the scenario and
        updates accordingly.
        """
        hitStatic = pg.sprite.spritecollide(self.player,
                                            self.scenario.platStatic,
                                            False)
        hitMoving = pg.sprite.spritecollide(self.player,
                                            self.scenario.platMoving,
                                            False)
        hitTransparent = pg.sprite.spritecollide(self.player,
                                                 self.scenario.platTransparent,
                                                 False)
        hits = hitStatic + hitMoving + hitTransparent

        for plat in hits:
            x, y = plat.rect.center
            P_00 = plat.rect.topleft
            P_10 = plat.rect.topright
            P_11 = plat.rect.bottomright
            P_01 = plat.rect.bottomleft

            # Defining points on the playerOne
            u, v = self.player.rect.center
            C_00 = self.player.rect.topleft
            C_10 = self.player.rect.topright
            C_11 = self.player.rect.bottomright
            C_01 = self.player.rect.bottomleft

            # Defining vectors on the platform which will be used in accurate
            # collision handling. The vectors are from the center of the
            # platform to the corners of the platform.
            vec_P00 = Vector2(x - P_00[0], y - P_00[1])
            vec_P10 = Vector2(x - P_10[0], y - P_10[1])
            vec_P11 = Vector2(x - P_11[0], y - P_11[1])
            vec_P01 = Vector2(x - P_01[0], y - P_01[1])

            # Defining variables for our angle coordinate system (which are
            # mathematically equivalent to bearings)
            FULL_ROTATION = 360
            origin = vec_P00

            # Calculating angles of the platform vectors
            angle_00 = origin.angle_to(vec_P00) % FULL_ROTATION
            angle_10 = origin.angle_to(vec_P10) % FULL_ROTATION
            angle_11 = origin.angle_to(vec_P11) % FULL_ROTATION
            angle_01 = origin.angle_to(vec_P01) % FULL_ROTATION

            # Calculating the displacement angle between the playerOne and platform
            displacement = Vector2(x - u, y - v)
            angle = origin.angle_to(displacement) % FULL_ROTATION

            # Calculating direction of the collision
            isCollideBottom = angle_00 < angle < angle_10
            isCollideLeft = angle_10 < angle < angle_11
            isCollideTop = angle_11 < angle < angle_01
            isCollideRight = angle_01 < angle

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
                if isCollideBottom:
                    self.player.rect.bottom = plat.rect.top
                    self.player.physics.velocity.y = 0
                    self.player.canJump = True

                elif isCollideLeft:
                    self.player.rect.left = plat.rect.right

                elif isCollideTop:
                    self.player.rect.top = plat.rect.bottom

                elif isCollideRight:
                    self.player.rect.right = plat.rect.left

                # Moves the playerOne if the playerOne is on a moving platform
                if isinstance(plat, MovingPlatform):
                    self.player.rect.x += plat.moveX * 2
                    self.player.rect.y += plat.moveY

    def checkButtonCollision(self):
        """
        Checks if the playerOne has collided with any button in the scenario and
        updates accordingly.
        """
        hits = pg.sprite.spritecollide(self.player,
                                       self.scenario.buttonsOff,
                                       True)
        if hits:
            if self.player.physics.velocity.x != 0 or \
                            self.player.physics.velocity.y != 0:
                print("abrir")
                self.scenario.isButtonOn = True

    def checkDoorCollision(self):
        """
        Checks if the playerOne has collided with any door in the scenario and
        updates accordingly.
        """
        hits = pg.sprite.spritecollide(self.player,
                                       self.scenario.doorsOpen,
                                       False)
        if hits and self.scenario.isDoorOpen:
            print("entrar")
            self.scenario.isEnd = True

    def checkEnemyCollision(self):
        """
        Checks if the playerOne has collided with any enemy or harmful object
        in the scenario and updates accordingly.
        """
        enemy_hit = pg.sprite.spritecollide(self.player,
                                            self.scenario.enemies,
                                            False)

        if enemy_hit:
            print("choque")
            self.player.lives -= 1
            self.player.isHit = True

    def checkScenarioBoundaryCollision(self):
        """
        Checks if the playerOne has 'fallen' out of the level.
        """
        background = self.scenario.background.get_rect()
        boundary = pg.Rect(self.scenario.worldShiftX,
                           self.scenario.worldShiftY,
                           background.width,
                           background.height + 100)

        if not pg.Rect.contains(boundary, self.player):
            self.player.isHit = True
            self.player.lives -= 1
