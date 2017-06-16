"""
Responsible for containing common rendering functions.
"""

import pygame as pg

from xcape.common import settings as settings
from xcape.common.loader import cutsceneResources
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent


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


class ImageLabel(GameObject):
    """
    Represents an image that can be drawn on screen.
    """

    def __init__(self, x, y, image, screen):
        """
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param image: pygame.Surface, representing the image to display.
        :param screen: pygame.Surface, representing the screen.
        """
        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.add("idle", [image], float('inf'))
        self.screen = screen
        self.rect = pg.Rect(x, y, 0, 0)

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()


class TextLabel(GameObject):
    """
    Represents text that can be drawn on screen.
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
        self.image = font.render(text, True, settings.COLOURS[colour])
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)


class WrappedTextLabel:
    """
    Represents text that is wrapped.
    """

    def __init__(self, text, size, colour, width, height, spacing, x, y):
        """
        :param text: String, the text to render.
        :param size: Integer, the size of the font.
        :param colour: String, the name of the colour to be used.
        :param width: Integer, the width of the output image.
        :param height: Integer, the height of the output image.
        :param spacing: Integer, the spacing between lines in the image.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.

        """
        lines, font = \
            self.wrap(text, settings.FONT, size, width, height, spacing)
        self.image = \
            self.renderLines(lines, font, colour, width, height, spacing)

        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()

    def wrap(self, text, fontPath, size, width, height, spacing):
        """
        Attempts to wrap the given text as best as possible.

        The wrapped text will always be less than the specified width long.

        :param text: String, the text to be wrapped.
        :param fontPath: os.path, representing the path to the font to use.
        :param size: Integer, the preferred size of the font to use.
        :param width: Integer, the width of the rendered text image.
        :param height: Integer, the height of the rendered text image.
        :param spacing: Integer, the spacing between lines in the image.
        :return: List, containing strings which represent each line.
        :return: 2-Tuple, as (lines, font).
        """
        for s in range(size, 12, -1):
            font = pg.font.SysFont(fontPath, s)
            lines, ws, hs = self._wrapWidthOnly(text, font, width, spacing)

            print(lines, ws, hs, s, "\n")
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


class Dialogue(GameObject):
    """
    Represents a collection of dialogue bubbles.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.bubbles = []
        self.index = 0

    def draw(self):
        if self.index >= 0:
            self.bubbles[self.index].draw()

    def drawWithCamera(self, camera):
        """
        Draws the dialogue on the screen, shifted by the camera.

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        if self.index >= 0:
            self.bubbles[self.index].drawWithCamera(camera)

    def add(self, text, x, y, bubbleType="right"):
        """
        Adds a dialogue bubble.

        :param text: Text, the text in the bubble.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param bubbleType: String, either 'right', 'left', or 'caption'.
        """
        bubble = _Bubble(text, bubbleType, x, y, self.screen)
        self.bubbles.append(bubble)


class _Bubble(GameObject):
    """
    Represents a dialogue bubble.
    """

    def __init__(self, text, bubbleType, x, y, screen):
        """
        :param text: Text, the text in the bubble.
        :param bubbleType: String, either 'right', 'left', or 'caption'.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param screen: pygame.Surface, representing the screen.
        """
        self.types = \
            {
                "right": "globe_right.png",
                "caption": "globe_caption.png",
                "left": "globe_left.png",
            }

        self.text = text
        self.image = self.generate(text, bubbleType)
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()
        self.screen = screen

    def generate(self, text, bubbleType):
        """
        Generates the image of the bubble with text in it.

        :param text: Text, the text in the bubble.
        :param bubbleType: String, either 'right', 'left', or 'caption'.
        :return: pygame.Surface, the image of the bubble with text.
        """
        text = WrappedTextLabel(text=str(text),
                                size=22,
                                colour="black",
                                width=172,
                                height=55,
                                spacing=20,
                                x=0, y=0)
        bubble = self._loadEmptyBubble(self.types[bubbleType])
        bubble.blit(text.image, (10, 10))
        return bubble

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def drawWithCamera(self, camera):
        """
        Draws the dialogue on the screen, shifted by the camera.

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        self.screen.blit(self.image, camera.apply(self))

    def _loadEmptyBubble(self, name):
        """
        Loads an bubble image with no text on it.

        :param name: String, the name of the globe image.
        :return: pygame.Surface, the image of the empty bubble.
        """
        bubble = cutsceneResources["assets"][name]
        bubble = addBackground(bubble)
        bubble.set_colorkey(settings.COLOURS["blue"])
        return bubble
