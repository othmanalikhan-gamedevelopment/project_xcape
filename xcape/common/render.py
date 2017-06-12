"""
Responsible for containing common rendering functions.
"""

import pygame as pg

from xcape.common import settings as settings
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
        """
        font = pg.font.SysFont(settings.FONT, size)
        font.set_italic(isItalic)
        self.image = font.render(text, True, settings.COLOURS[colour])
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = self.image.get_size()
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)


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

        blankBubble = _Bubble(pg.Surface((0, 0)), 0, 0, self.screen)
        self.bubbles.append(blankBubble)

    def draw(self):
        self.bubbles[self.index].draw()

    def add(self, image, x, y):
        """
        Adds a dialogue bubble.

        :param image: pygame.Surface, representing the image to display.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        """
        self.bubbles.append(_Bubble(image, x, y, self.screen))


class _Bubble(GameObject):
    """
    Represents a dialogue bubble.
    """

    def __init__(self, image, x, y, screen):
        """
        :param image: pygame.Surface, representing the image to display.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param screen: pygame.Surface, representing the screen.
        """
        self.rect = pg.Rect(x, y, 0, 0)
        self.screen = screen

        image = addBackground(image)
        image.set_colorkey(settings.COLOURS["blue"])
        self.image = image
        self.rect = pg.Rect(x, y, 0, 0)
        self.rect.size = image.get_size()
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, self.rect)
