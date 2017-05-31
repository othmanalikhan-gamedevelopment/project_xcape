"""
Responsible for loading common rendering resources.
"""

import os

import pygame as pg


FONT_NAME = "m04fatalfuryblack"


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


def loadMenus():
    """
    Loads all the images for the menus.

    :return: 2D Dictionary, mapping dir and file name to image.
    """
    menu = {}
    MENUS_PATH = os.path.join("images", "menus")

    for d in os.listdir(MENUS_PATH):
        menu[d] = {}
        for f in os.listdir(os.path.join(MENUS_PATH, d)):
            image = loadImage(os.path.join(MENUS_PATH, d, f))
            menu[d][f] = image

    return menu


def loadScenes():
    """
    Loads all the images for the scenes.

    :return: 2D Dictionary, mapping dir and file name to image.
    """
    scene = {}
    SCENES_PATH = os.path.join("images", "scenes")

    for d in os.listdir(SCENES_PATH):
        scene[d] = {}
        for f in os.listdir(os.path.join(SCENES_PATH, d)):
            image = loadImage(os.path.join(SCENES_PATH, d, f))
            scene[d][f] = image

    return scene


def loadImage(path, alpha=False):
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
