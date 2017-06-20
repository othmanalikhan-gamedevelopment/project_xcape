"""
Responsible for rendering of a game object.
"""

import pygame as pg

from xcape.common.object import GameObject


class RenderComponent(GameObject):
    """
    Attaches to a game object to allow rendering.
    """

    def __init__(self, gameObject, enableOrientation=False, enableRepeat=True):
        """
        :param gameObject: GameObject instance, the instance to attach to.
        :param enableOrientation: Boolean, whether to consider direction.
        :param enableRepeat: Boolean, whether to keep repeating the animation.
        """
        self.gameObject = gameObject
        self.enableOrientation = enableOrientation
        self.enableRepeat = enableRepeat

        self.state = None
        self.orientation = None

        self.stateToAnimation = {}
        self.stateToTiming = {}
        self.animation = []
        self.timings = []
        self.image = None

        # Units are in milliseconds
        self.origin = pg.time.get_ticks()
        self.elapsed = 0.0
        self.frameNum = 0

    def update(self):
        self._updateOrientation()
        self._updateAnimation()
        self.gameObject.rect.size = self.image.get_size()

    def draw(self, camera=None):
        if camera:
            self.gameObject.screen.blit(self.image, camera.apply(self.gameObject))
        else:
            self.gameObject.screen.blit(self.image, self.gameObject.rect)

    def add(self, state, images, duration=1000):
        """
        Links a given state to a sequence of images that can be rendered as
        an animation and sets it as the current state.

        The timing of each frame in the animation is automatically partitioned
        such that each frame has uniform of length (and if a single image is
        given, its duration will span forever). This can be technically
        modified after adding the animation for fine tuning.

        :param state: String, the name of the state tied to the animation.
        :param images: List, containing pygame.Surface objects.
        :param duration: Integer, the length of the animation in milliseconds.
        """
        self.state = state

        try:
            dt = duration / len(images)
            timings = [i*dt for i, _ in enumerate(images, start=1)]
            self.stateToTiming[state] = timings
            self.stateToAnimation[state] = images

        except TypeError:
            timings = [float('inf')]
            self.stateToTiming[state] = timings
            self.stateToAnimation[state] = [images]

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
        self.stateToAnimation[self.state] = \
            list(reversed(self.animation))

    def scaleAll(self, DIMENSIONS):
        """
        Scales the size of each frame in all animations.

        :param DIMENSIONS: 2-Tuple, containing integers for new (x, y) size.
        """
        for state, frames in self.stateToAnimation.items():
            frames = [pg.transform.scale(f, DIMENSIONS) for f in frames]
            self.stateToAnimation[state] = frames

    def _updateAnimation(self):
        """
        Ensures that the correct animation frame is displayed (based on its
        timing).
        """
        self.elapsed = pg.time.get_ticks() - self.origin
        self._changeAnimation(self.state)

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

    def _updateOrientation(self):
        """
        Ensures that the rendered image is facing either left or right correctly.
        """
        if self.enableOrientation:
            if self.orientation == "left":
                self.image = pg.transform.flip(self.image, True, False)

    def _changeAnimation(self, name):
        """
        Change to the animation of the given name if it exists.

        :param name: String, the name of the animation.
        """
        oldAnimation = self.animation
        newAnimation = self.stateToAnimation[name]

        if oldAnimation != newAnimation:
            self.timings = self.stateToTiming[name]
            self.animation = self.stateToAnimation[name]
            self._resetAnimation()

    def _resetAnimation(self):
        """
        Resets the current animation to its start.
        """
        self.frameNum = 0
        self.elapsed = 0
        self.origin = pg.time.get_ticks()

    def _applyEffect(self, effect, args):
        """
        Applies the given effect on the current animation.

        :param effect: Function, the effect to apply on the current animation.
        :param args: Tuple, containing the arguments of the effect function.
        """
        flipped = [effect(frame, *args) for frame in self.animation]
        self.stateToAnimation[self.state] = flipped

