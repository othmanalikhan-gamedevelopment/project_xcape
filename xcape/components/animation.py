"""
Responsible for rendering of a game object's animation.
"""

import pygame as pg

from xcape.common.object import GameObject


class AnimationComponent(GameObject):
    """
    Attaches to a game object to allow rendering of static and animated images.
    """

    def __init__(self, gameObject, enableOrientation=False, enableRepeat=True):
        """
        :param gameObject: GameObject instance, representing any object
        inheriting from the GameObject class.
        :param enableOrientation: Boolean, causing animations to take into
        account direction of the gameobject.
        :param enableRepeat: Boolean, whether to repeat the animation endlessly.
        """
        self.gameObject = gameObject
        self.enableOrientation = enableOrientation
        self.enableRepeat = enableRepeat

        self.stateToAnimation = {}
        self.stateToTiming = {}
        self.animation = []
        self.image = None

        # Units are in milliseconds
        self.origin = pg.time.get_ticks()
        self.timings = []
        self.elapsed = 0.0
        self.frameNum = 0

    def update(self):
        self._updateAnimation()
        self.gameObject.rect.size = self.image.get_size()

        if self.enableOrientation:
            if self.gameObject.orientation == "left":
                self.image = pg.transform.flip(self.image, True, False)

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

        The timing of each frame in the animation is automatically
        partitioned such that each frame has uniform of length. This can be
        technically modified after adding the animation.

        :param state: String, the name of the state tied to the animation.
        :param images: List, containing pygame.Surface objects.
        :param duration: Integer, the length of the animation in milliseconds.
        """
        dt = duration / len(images)
        timings = [i*dt for i, _ in enumerate(images, start=1)]
        self.stateToTiming[state] = timings
        self.timings = timings

        self.stateToAnimation[state] = images
        self.animation = images
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

    def _updateAnimation(self):
        """
        Updates the animation.
        """
        self.elapsed = pg.time.get_ticks() - self.origin
        self._changeAnimation(self.gameObject.state)

        lastIndex = len(self.animation)-1
        duration = self.timings[-1]

        if duration >= self.elapsed >= 0:
            if self.elapsed > self.timings[self.frameNum]:
                self.frameNum += 1
            # Safety check due to rounding errors
            if self.frameNum > lastIndex:
                self.frameNum = lastIndex

        elif self.elapsed > duration and not self.enableRepeat:
            self.frameNum = lastIndex

        else:
            self._resetAnimation()

        self.image = self.animation[self.frameNum]

    def _changeAnimation(self, name):
        """
        Attempts to change to the animation of the given name if it exists.

        :param name: String, the name of the animation.
        """
        try:
            oldAnimation = self.animation
            newAnimation = self.stateToAnimation[name]

            if oldAnimation != newAnimation:
                self.timings = self.stateToTiming[name]
                self.animation = self.stateToAnimation[name]
                self._resetAnimation()

        except KeyError:    # No existing animation found
            pass

    def _resetAnimation(self):
        """
        Resets the current animation to its start.
        """
        self.frameNum = 0
        self.elapsed = 0
        self.origin = pg.time.get_ticks()


