"""
Responsible for loading common rendering resources.
"""

import os

import pygame as pg

MENUS_PATH = os.path.join("images", "menus")
SCENES_PATH = os.path.join("images", "scenes")


COLOURS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "gray": (27, 27, 27),
    "blackred": (35, 21, 21),
}


def loadContent(path):
    """
    For the given path to a directory, loads all the images in its
    subdirectories and their animations (if any). To illustrate,
    the directory structure shown below is an example of a valid structure.

    - RootDir
        - SubDir1
            - image1
            - image2
        - SubDir2
            - image1
            - image2
            - animationDir1
                - image1
                - image2
        - SubDir3
            - image1

    If animations are present in the directory structure, they should be
    named in order (ideally each frame corresponds to an integer).

    :param path: os.path, the path to a directory hosting subdirectories.
    :return: 2D Dictionary, with the following format:
        static images:  content[subDir1][imageName] = image
        animations:     content[subDir1][animationDir] = {frameNum: image}
    """
    content = {}

    for depth1 in os.listdir(path):
        content[depth1] = {}
        pathDepth1 = os.path.join(path, depth1)

        for depth2 in os.listdir(pathDepth1):
            pathDepth2 = os.path.join(path, depth1, depth2)

            # Loading static images
            if os.path.isfile(pathDepth2):
                content[depth1][depth2] = loadImage(pathDepth2)

            # Loading animations
            else:
                animation = {}
                for i, frame in enumerate(os.listdir(pathDepth2), start=1):
                    pathDepth3 = os.path.join(path, depth1, depth2, frame)
                    animation[i] = loadImage(pathDepth3)
                content[depth1][depth2] = animation

    return content


def loadImage(path, alpha=True):
    """
    Loads an image using pygame modules.

    :param path: os.path, the path to the image.
    :param alpha: Boolean, determining whether to apply alpha pixels.
    :return: pygame.Surface, representing the loaded image.
    """
    image = pg.image.load(path)

    if alpha is True:
        image.set_colorkey(COLOURS["white"])
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def drawText(text, size, colour, x, y, surface):
    """
    Draws the supplied text on the given surface.

    :param text: String, the text to render.
    :param size: Integer, the size of the font.
    :param colour: 3-Tuple, containing the RGB values of the colour.
    :param x: Integer, the x-position of the text.
    :param y: Integer, the y-position of the text.
    :param surface: pygame.Surface, the surface to render the text onto.
    """
    FONT_NAME = "m04fatalfuryblack"
    font = pg.font.SysFont(FONT_NAME, size)
    textSurface = font.render(text, True, colour)
    surface.blit(textSurface, (x, y))

