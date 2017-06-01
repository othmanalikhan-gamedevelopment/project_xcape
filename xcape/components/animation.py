"""
Responsible for rendering of a game object's animation.
"""

import pygame as pg

from xcape.common.object import GameObject


class AnimationComponent(GameObject):
    """
    Attaches to a game object to allow rendering of static and animated images.
    """

    def __init__(self, gameObject):
        """
        :param gameObject: GameObject Class, representing any object inheriting
        from the GameObject class.
        """
        self.gameObject = gameObject

        self.stateToType = {}
        self.stateToStatic = {}
        self.stateToDynamic = {}
        self.stateToDuration = {}
        self.animation = []
        self.image = None

        # Units are in milliseconds
        self.origin = pg.time.get_ticks()
        self.elapsed = 0.0
        self.duration = 0.0
        self.frameNum = 0

    def update(self):
        stateType = self.stateToType[self.gameObject.state]

        if stateType == "dynamic":
            self.elapsed = pg.time.get_ticks() - self.origin
            self.animation = self.stateToDynamic[self.gameObject.state]
            self.duration = self.stateToDuration[self.gameObject.state]
            frameDuration = self.duration / len(self.animation)

            # Increment animation
            if self.elapsed > frameDuration:
                self.frameNum += 1
                self.elapsed = 0
                self.origin = pg.time.get_ticks()

            # Reset animation
            if (self.frameNum+1)*frameDuration > self.duration:
                self.frameNum = 0
                self.elapsed = 0
                self.origin = pg.time.get_ticks()

            self.image = self.animation[self.frameNum]

        if stateType == "static":
            self.image = self.stateToStatic[self.gameObject.state]
            self.frameNum = 0

    def draw(self):
        self.gameObject.screen.blit(self.image, self.gameObject.rect)

    def addDynamic(self, state, images, duration):
        """
        Adds a dynamic animation to the given state.

        :param state: String, the name of the state tied to the animation.
        :param images: List, containing pygame.Surface objects.
        :param duration: Integer, the length of the animation in milliseconds.
        """
        self.stateToDynamic[state] = images
        self.stateToDuration[state] = duration
        self.stateToType[state] = "dynamic"

    def addStatic(self, state, image):
        """
        Adds a static animation to the given state.

        :param state: String, the name of the state tied to the animation.
        :param image: pygame.Surface, representing the static image.
        """
        self.stateToStatic[state] = image
        self.stateToType[state] = "static"
