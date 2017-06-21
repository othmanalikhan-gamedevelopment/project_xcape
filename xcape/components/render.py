"""
Responsible for rendering of a game object.
"""

import pygame as pg

from xcape.common import settings as settings
from xcape.common.loader import CUTSCENE_RESOURCES
from xcape.common.object import GameObject


# TODO: Complete
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
        self.enableOrientation = enableOrientation
        self.enableRepeat = enableRepeat

        self.stateToAnimation = {}
        self.stateToTiming = {}
        self.animation = []
        self.timings = []
        self.image = None

        # Units are in milliseconds
        self.origin = pg.time.get_ticks()
        self.elapsed = 0.0
        self.frameNum = 0

        self._state = None
        self._orientation = "right"
        self._gameObject = gameObject

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
        an animation.

        The timing of each frame in the animation is automatically partitioned
        such that each frame has uniform of length (and if a single image is
        given, its duration will span forever). This can be technically
        modified after adding the animation for fine tuning.

        :param state: String, the name of the state tied to the animation.
        :param images: List, containing pygame.Surface objects.
        :param duration: Integer, the length of the animation in milliseconds.
        """
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
            if self._orientation == "left":
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

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        faces = ["left", "right", "up", "down"]
        if value in faces:
            self._orientation = value
        else:
            raise ValueError("The only orientations allowed are {} "
                             .format(faces))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        states = self.stateToAnimation.keys()
        if value in states:
            self._state = value
        else:
            raise ValueError("'{}' is in an invalid state! The states allowed "
                             "for '{}' are '{}'"
                             .format(value, self.gameObject, states))

    @property
    def gameObject(self):
        return self._gameObject

    @gameObject.setter
    def gameObject(self, value):
        if not hasattr(value, 'rect'):
            raise AttributeError("'{}' does not have required 'rect' attribute"
                                 .format(value))


# TODO: Complete
class ImageLabel(GameObject):
    """
    Represents an image that is intended to be drawn on screen.
    """

    def __init__(self, image, x, y, screen):
        """
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param image: pygame.Surface, representing the image to display.
        :param screen: pygame.Surface, representing the screen.
        """
        self.render = RenderComponent(self)
        self.render.add("background", image)
        self.rect = pg.Rect(x, y, 0, 0)
        self.screen = screen

    def update(self):
        self.render.update()

    def draw(self):
        self.render.draw()


# TODO: Complete
class TextLabel(GameObject):
    """
    Represents text that is intended to be drawn on screen.
    """

    def __init__(self, text, size, colour, x, y, screen, isItalic=False):
        """
        :param text: String, the text to render.
        :param size: Integer, the size of the font.
        :param colour: String, the name of the colour to be used.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param screen: pygame.Surface, representing the screen.
        :param isItalic: Boolean, whether the text is italics.
        """
        font = pg.font.SysFont(settings.FONT, size)
        font.set_italic(isItalic)
        image = font.render(text, True, settings.COLOURS[colour])
        self.render = RenderComponent(self)
        self.render.add("background", image)

        self.rect = pg.Rect(x, y, 0, 0)
        self.screen = screen

    def update(self):
        self.render.update()

    def draw(self):
        self.render.draw()


class WrappedTextLabel:
    """
    Represents text that is wrapped.
    """

    def __init__(self, text, minSize, maxSize, colour, width, height, spacing,
                 x, y):
        """
        :param text: String, the text to render.
        :param minSize: Integer, the minimum size of the font.
        :param maxSize: Integer, the maximum size of the font.
        :param colour: String, the name of the colour to be used.
        :param width: Integer, the width of the output image.
        :param height: Integer, the height of the output image.
        :param spacing: Integer, the spacing between lines in the image.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        """
        lines, font = \
            self.wrap(text, settings.FONT, minSize, maxSize, width, height, spacing)
        self.image = \
            self.renderLines(lines, font, colour, width, height, spacing)

        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def wrap(self, text, fontPath, minSize, maxSize, width, height, spacing):
        """
        Attempts to wrap the given text as best as possible.

        The wrapped text will always be less than the specified width long.

        :param text: String, the text to be wrapped.
        :param fontPath: os.path, representing the path to the font to use.
        :param minSize: Integer, the minimium size of the font.
        :param maxSize: Integer, the maximum size of the font.
        :param width: Integer, the width of the rendered text image.
        :param height: Integer, the height of the rendered text image.
        :param spacing: Integer, the spacing between lines in the image.
        :return: List, containing strings which represent each line.
        :return: 2-Tuple, as (lines, font).
        """
        for s in range(maxSize, minSize, -1):
            font = pg.font.SysFont(fontPath, s)
            lines, ws, hs = self._wrapWidthOnly(text, font, width, spacing)

            if height > sum(hs):
                return lines, font

        raise ValueError("Insufficient space to wrap the font!")

    def _wrapWidthOnly(self, text, font, width, spacing):
        """
        Wraps the text ensuring that each line is at most the given width
        length.

        This function does NOT take consider the heights of the lines.

        :param text: String, the text to be wrapped.
        :param font: pygame.font.Font, the font to be used (fixed size).
        :param width: Integer, the width of the rendered text image.
        :param spacing: Integer, the spacing between lines in the image.
        :return: 3-Tuple, as (lines, widths, heights).
        """
        built = ""
        lines = []
        heights = []
        widths = []

        for word in text.split():
            w, h = font.size(built + " " + word)

            if width > w:
                built += " " + word
            else:
                lines.append(built)
                w, h = font.size(built)
                heights.append(h + spacing)
                widths.append(w)
                built = word

            built = built.strip()

        lines.append(built)
        w, h = font.size(built)
        heights.append(h)
        widths.append(w)
        return lines, widths, heights

    def renderLines(self, lines, font, colour, width, height, spacing):
        """
        Renders the given into an image.

        :param lines: List, where each element is a string.
        :param font: pygame.font.Font, representing the font to use.
        :param colour: String, the name of the colour to be used.
        :param width: Integer, the width of the output image.
        :param height: Integer, the height of the output image.
        :param spacing: Integer, the spacing between lines in the image.
        :return: pygame.Surface, the image of the rendered lines.
        """
        c = settings.COLOURS[colour]
        images = [font.render(l, True, c) for l in lines]

        merged = pg.Surface((width, height))
        merged.fill(settings.COLOURS["white"])
        merged.set_colorkey(settings.COLOURS["white"])
        [merged.blit(img, (0, n*spacing)) for n, img in enumerate(images)]
        return merged


# TODO: Complete
class Dialogue(GameObject):
    """
    Represents a collection of dialogue bubbles that are intended to be drawn
    on the screen, one at a time.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.allBubbles = []
        self.bubble = None

    def update(self):
        if self.bubble:
            self.bubble.update()

    def draw(self, camera=None):
        if self.bubble:
            self.bubble.draw(camera)

    def add(self, text, x, y, bubbleType="right"):
        """
        Adds a dialogue bubble and sets it as the current bubble to display.

        :param text: Text, the text in the bubble.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param bubbleType: String, either 'right', 'left', or 'caption'.
        """
        bubble = _Bubble(text, bubbleType, x, y, self.screen)
        self.allBubbles.append(bubble)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, value):
        if not self.allBubbles or value is None:
            self._index = None
            self.bubble = None
        elif len(self.allBubbles) > value >= 0:
            self._index = value
            self.bubble = self.allBubbles[value]
        else:
            raise IndexError("There is no speech bubble with index {}!"
                             .format(value))


# TODO: Complete
class _Bubble(GameObject):
    """
    Represents a dialogue bubble that can be drawn on screen.
    """

    def __init__(self, text, bubbleType, x, y, screen):
        """
        :param text: Text, the text in the bubble.
        :param bubbleType: String, either 'right', 'left', or 'caption'.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param screen: pygame.Surface, representing the screen.
        """
        image = self.generate(text, bubbleType)
        self.render = RenderComponent(self)
        self.render.add("background", image)
        self.render.state = "background"
        self.rect = pg.Rect(x, y, 0, 0)

        self.text = text
        self.screen = screen

    def __str__(self):
        return "Bubble: " + self.text

    def update(self):
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)

    def generate(self, text, bubbleType):
        """
        Generates the image of the bubble with text in it.

        :param text: Text, the text in the bubble.
        :param bubbleType: String, either 'right', 'left', or 'caption'.
        :return: pygame.Surface, the image of the bubble with text.
        """
        text = WrappedTextLabel(text=str(text),
                                minSize=16,
                                maxSize=22,
                                colour="black",
                                width=177,
                                height=65,
                                spacing=20,
                                x=0, y=0)
        image = self._loadEmptyBubble(bubbleType)
        image.blit(text.image, (10, 10))
        return image

    def _loadEmptyBubble(self, name):
        """
        Loads an bubble image with no text on it.

        :param name: String, the name of the globe image.
        :return: pygame.Surface, the image of the empty bubble.
        """
        bubble = CUTSCENE_RESOURCES["globes"][name][0]
        bubble = addBackground(bubble)
        bubble.set_colorkey(settings.COLOURS["blue"])
        return bubble


# TODO: Complete
def addBackground(surface, colour="white"):
    """
    Adds a background with the given colour to the supplied surface.

    :param surface: pygame.Surface, the surface to render the background onto.
    :param colour: String, the name of the colour.
    :return: pygame.Surface, the original surface with a coloured background.
    """
    background = pg.Surface(surface.get_size())
    background.fill(settings.COLOURS[colour])
    background.blit(surface, (0, 0))
    background = background.convert()
    return background


# TODO: Complete
def buildParts(blocks, orientation, images):
    """
    Builds the image that consists of three separate parts, and allows
    scaling of the middle image so that the output image has greater length.

    :param blocks: Integer, the number of times to replicate the mid image.
    :param orientation: String, either 'v' or 'h' for vertical or horizontal.
    :param images: Tuple, containing three pygame.Surfaces to build from.
    :return: pygame.Surface, the built image.
    """
    w0, h0 = images[0].get_size()
    w1, h1 = images[1].get_size()
    w2, h2 = images[2].get_size()

    if orientation == "h":
        img = pg.Surface((w0 + blocks*w1 + w2, h0))
        img.blit(images[0], (0, 0))
        for i in range(blocks):
            img.blit(images[1], (w0 + i*w1, 0))
        img.blit(images[2], (w0 + blocks*w1, 0))

    if orientation == "v":
        img = pg.Surface((w0, h0 + blocks*h1 + h2))
        img.blit(images[0], (0, 0))
        for i in range(blocks):
            img.blit(images[1], (0, h0 + i*h1))
        img.blit(images[2], (0, h0 + blocks*h1))

    # Removing black pixels on newly created surface
    img.set_colorkey(settings.COLOURS["black"])
    img = img.convert_alpha()
    return img


# TODO: Complete
def replicate(amount, orientation, image):
    """
    Extends the image by duplicating it either vertically or horizontally.

    :param amount: Integer, the amount of times to replicate the image.
    :param orientation: String, either 'v' or 'h' for vertical or horizontal.
    :param image: pygame.Surface, the original image.
    :return: pygame.Surface, the replicated image.
    """
    w, h = image.get_size()

    if orientation == "h":
        img = pg.Surface((amount*w, h))
        for i in range(amount):
            img.blit(image, (i*w, 0))

    if orientation == "v":
        img = pg.Surface((w, amount*h))
        for i in range(amount):
            img.blit(image, (0, i*h))

    img.set_colorkey(settings.COLOURS["black"])
    img = img.convert_alpha()
    return img
