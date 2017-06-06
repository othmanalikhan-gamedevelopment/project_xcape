"""
Responsible for rendering of a game object's animation.
"""

import pygame as pg

from xcape.common.object import GameObject


class AnimationComponent(GameObject):
    """
    Attaches to a game object to allow rendering of static and animated images.
    """

    def __init__(self, gameObject, enableOrientation=False):
        """
        :param gameObject: GameObject Class, representing any object inheriting
        from the GameObject class.
        :param enableOrientation: Boolean, causing animations to take into
        account direction of the gameobject.
        """
        self.gameObject = gameObject
        self.enableOrientation = enableOrientation

        self.stateToAnimation = {}
        self.stateToDuration = {}
        self.animation = []
        self.image = None

        # Units are in milliseconds
        self.origin = pg.time.get_ticks()
        self.elapsed = 0.0
        self.duration = 0.0
        self.frameNum = 0

    def update(self):
        self.image, self.frameNum = self._updateAnimation(self.frameNum)
        self.gameObject.rect.size = self.image.get_size()

        if self.enableOrientation:
            if self.gameObject.orientation == "left":
                self.image = pg.transform.flip(self.image, True, False)

    def _updateAnimation(self, currentFrame):
        """
        Updates the animation.

        :param currentFrame: Integer, the frame number of the current animation.
        :return: 2-Tuple, containing the pygame.Surface needed to be drawn
        and an Integer frame number.
        """
        self.elapsed = pg.time.get_ticks() - self.origin
        self.duration = self.stateToDuration[self.gameObject.state]

        # Resetting frames if a new animation
        newAnimation = self.stateToAnimation[self.gameObject.state]
        if newAnimation != self.animation:
            currentFrame = 0

        self.animation = newAnimation
        frameDuration = self.duration / len(self.animation)

        # Increment animation
        if self.elapsed > frameDuration:
            currentFrame += 1
            self.elapsed = 0
            self.origin = pg.time.get_ticks()

        # Reset animation when complete
        if (currentFrame+1)*frameDuration > self.duration:
            currentFrame = 0
            self.elapsed = 0
            self.origin = pg.time.get_ticks()

        image = self.animation[currentFrame]
        return image, currentFrame

    def draw(self):
        self.gameObject.screen.blit(self.image, self.gameObject.rect)

    def drawWithCamera(self, camera):
        """
        Draws the animation on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        self.gameObject.screen.blit(self.image, camera.apply(self.gameObject))

    def add(self, state, images, duration):
        """
        Adds an animation to the given state.

        :param state: String, the name of the state tied to the animation.
        :param images: List, containing pygame.Surface objects.
        :param duration: Integer, the length of the animation in milliseconds.
        """
        self.stateToAnimation[state] = images
        self.stateToDuration[state] = duration
        self.image = images[0]

    def scaleAll(self, DIMENSIONS):
        """
        Scales the size of each frame in all animations.

        :param DIMENSIONS: 2-Tuple, containing integers for new (x, y) size.
        """
        for state, frames in self.stateToAnimation.items():
            frames = [pg.transform.scale(f, DIMENSIONS) for f in frames]
            self.stateToAnimation[state] = frames

    def flip(self, isVertical, isHorizontal):
        """
        Reflects vertically the images of the current animation.
        """
        effect = pg.transform.flip
        args = (isVertical, isHorizontal)
        self._applyEffect(effect, args)

    def reverse(self):
        """
        Reverses the animation sequence for animations.
        """
        self.stateToAnimation[self.gameObject.state] = \
            list(reversed(self.animation))

    def _applyEffect(self, effect, args):
        """
        Applies the given effect on the current animation.

        :param effect: Function, the effect to apply on the current animation.
        :param args: Tuple, containing the arguments of the effect function.
        """
        flipped = [effect(frame, *args) for frame in self.animation]
        self.stateToAnimation[self.gameObject.state] = flipped
