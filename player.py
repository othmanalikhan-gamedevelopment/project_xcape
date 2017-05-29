# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 00:08:32 2017
@author: Gustavo
"""
import pygame as pg

from physics import PhysicsComponent
from settings import SpriteSheet


class PlayerBase(pg.sprite.Sprite):
    """
    Represents the shared characteristics and attributes of a playerOne in game.
    """

    def __init__(self, screen):
        """
        A simple constructor

        :param screen: pygame.display Class, representing the user's screen.
        """
        super().__init__()
        self.screen = screen

        # Initialising states
        self.currentDirection = "S"
        self.previousDirection = "S"
        self.canJump = False
        self.isJumping = False
        self.isHit = False
        self.lives = 3

        # Initialising sprites
        self.initialiseAnimation()

        # Initialising physics
        self.physics = PhysicsComponent(self)
        self.jumpSpeed = -12
        self.moveSpeed = 5
        self.rect = self.image.get_rect()

    def update(self):
        """
        Updates the playerOne for every frame in the game.
        """
        self.updateAnimation()
        self.physics.update()

    def eventHandler(self, event):
        """
        Handles the supplied event.

        :param event: pygame.event, representing an triggered event.
        """
        raise NotImplementedError

#################################### FUNCTIONS RESPONSIBLE ANIMATION

    def draw(self):
        """
        Draws the playerOne on the screen.
        """
        self.screen.blit(self.image, self.rect)

    def initialiseAnimation(self):
        """
        Initialises the animations of the playerOne.
        """
        self.DIMENSIONS = (50, 48)
        self.animationFrame = 0
        self.animationTicker = 0
        self.animationSpeed = 3
        self.standingFramesLeft = []
        self.standingFramesRight = []
        self.walkingFramesRight = []
        self.walkingFramesLeft = []
        self.loadWalkingSprites()
        self.loadStandingSprites()
        self.image = self.standingFramesRight[0]

    def updateAnimation(self):
        """
        Updates the animation of the playerOne based on the playerOne's state.
        """

        # Controls animation speed
        self.animationTicker += 1
        if self.animationTicker % self.animationSpeed == 0:
            self.animationFrame += 1
            self.animationTicker = 0

        if self.currentDirection == "R":
            frame = self.animationFrame % len(self.walkingFramesRight)
            self.image = self.walkingFramesRight[frame]
            self.previousDirection = "R"

        elif self.currentDirection == "L":
            frame = self.animationFrame % len(self.walkingFramesLeft)
            self.image = self.walkingFramesLeft[frame]
            self.previousDirection = "L"

        if self.currentDirection == "S":
            if self.previousDirection == "R":
                self.image = self.standingFramesRight[0]
            elif self.previousDirection == "L":
                self.image = self.standingFramesLeft[0]
            self.previousDirection = "S"

    def loadStandingSprites(self):
        """
        Loads the sprites where the playerOne is standing.
        """
        sprite_sheet = SpriteSheet("character_standing.png")
        x, y, width, height = 0, 0, 80, 77

        imageRight = sprite_sheet.get_image(x, y, width, height)
        imageRight = pg.transform.scale(imageRight, self.DIMENSIONS)
        self.standingFramesRight.append(imageRight)

        imageLeft = pg.transform.flip(imageRight, True, False)
        self.standingFramesLeft.append(imageLeft)

    def loadWalkingSprites(self):
        """
        Loads the sprites where the playerOne is walking.
        """
        sprite_sheet = SpriteSheet("main_character.png")
        x, y, width, height = 0, 0, 80, 77
        dx = 80
        SPRITE_NUM = 6

        for i in range(SPRITE_NUM):
            imageRight = sprite_sheet.get_image(x + i*dx, y, width, height)
            imageRight = pg.transform.scale(imageRight, self.DIMENSIONS)
            self.walkingFramesRight.append(imageRight)

            imageLeft = pg.transform.flip(imageRight, True, False)
            self.walkingFramesLeft.append(imageLeft)
        pass

#################################### FUNCTIONS RESPONSIBLE FOR CONTROLS

    def jump(self):
        """
        Makes the playerOne jump if the playerOne is in a state that allows isJumping.
        """
        if self.canJump:
            self.physics.velocity.y = self.jumpSpeed
            self.canJump = False

    def moveLeft(self):
        """
        Moves the playerOne left and changes the direction state.
        """
        self.physics.velocity.x = -self.moveSpeed
        self.currentDirection = "L"
        
    def moveRight(self):
        """
        Moves the playerOne right and changes the direction state.
        """
        self.physics.velocity.x = self.moveSpeed
        self.currentDirection = "R"

    def stop(self):
        """
        Stops the playerOne in place and changes the direction state.
        """
        self.physics.velocity.x = 0
        self.currentDirection = "S"


class PlayerOne(PlayerBase):
    """
    Represents the first player in game.
    """

    def __init__(self, screen):
        """
        A simple constructor

        :param screen: pygame.display Class, representing the user's screen.
        """
        super().__init__(screen)

    def eventHandler(self, event):
        """
        Handles the supplied event.

        :param event: pygame.event, representing an triggered event.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE or event.key == pg.K_UP:
                self.jump()
            if event.key == pg.K_LEFT:
                self.moveLeft()
            if event.key == pg.K_RIGHT:
                self.moveRight()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT and self.physics.velocity.x < 0:
                self.stop()
            if event.key == pg.K_RIGHT and self.physics.velocity.x > 0:
                self.stop()


class PlayerTwo(PlayerBase):
    """
    Represents the second player in game.
    """

    def __init__(self, screen):
        """
        A simple constructor

        :param screen: pygame.display Class, representing the user's screen.
        """
        super().__init__(screen)

    def eventHandler(self, event):
        """
        Handles the supplied event.

        :param event: pygame.event, representing an triggered event.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                self.jump()
            if event.key == pg.K_a:
                self.moveLeft()
            if event.key == pg.K_d:
                self.moveRight()

        if event.type == pg.KEYUP:
            if event.key == pg.K_a and self.physics.velocity.x < 0:
                self.stop()
            if event.key == pg.K_d and self.physics.velocity.x > 0:
                self.stop()

