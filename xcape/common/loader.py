"""
Responsible for loading common game resources.

NOTE: UPON IMPORTING THIS MODULE, ALL IO GAME ASSETS ARE LOADED!
"""

import os

import pygame as pg

import xcape.common.settings as settings


def loadSound(path):
    """
    Converts all WAV files residing in the directory path into pygame sound
    objects, which are then stored into a dictionary.

    :param path: os.path, the path to a directory hosting subdirectories.
    :return: Dictionary, mapping name to pgygame.mixer.Sound object.
    """
    nameToSound = {}

    for f in os.listdir(path):
        soundPath = os.path.join(path, f)
        name = f.split(".")[0]
        nameToSound[name] = pg.mixer.Sound(soundPath)

    return nameToSound


def loadAnimations(rootDir):
    """
    Loads all the animation images stored in subdirectories below tthe
    given root directory.

    The structure of the directory is as follows: The actual list of images
    for the animations are three three levels below the root directory.

    For instance, the directory structure shown below is valid.

    - RootDir

        - SubDir1
            - animationDir1
                - image1
                - image2

        - SubDir2
            - animationDir2
                - image1
                - image2
                - image3

        - SubDir3
            - animationDir3
                - image1

    The list of images are ordered lexicographically, and ideally, should be
    just be a sequence of integers.

    :param rootDir: os.path, the path to a directory hosting subdirectories.
    :return: 2D Dictionary, e.g. content[subDir][animationDir] = [images].
    """
    content = {}

    for depth1 in os.listdir(rootDir):
        content[depth1] = {}
        pathDepth1 = os.path.join(rootDir, depth1)

        for depth2 in os.listdir(pathDepth1):
            pathDepth2 = os.path.join(rootDir, depth1, depth2)

            animation = []
            for frame in os.listdir(pathDepth2):
                pathDepth3 = os.path.join(rootDir, depth1, depth2, frame)
                animation.append(_loadImage(pathDepth3))

            content[depth1][depth2] = animation

    return content


def _loadImage(path, alpha=True):
    """
    Loads an image using pygame modules.

    :param path: os.path, the path to the image.
    :param alpha: Boolean, determining whether to apply alpha pixels.
    :return: pygame.Surface, representing the loaded image.
    """
    image = pg.image.load(path)

    if alpha is True:
        image.set_colorkey(settings.COLOURS["white"])
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


_SFX_PATH = os.path.join("sfx")
_ICONS_PATH = os.path.join("images", "icons")
_MENUS_PATH = os.path.join("images", "menus")
_ZONE1_PATH = os.path.join("images", "scenes", "zone1")
_ZONE2_PATH = os.path.join("images", "scenes", "zone2")
_CUTSCENES_PATH = os.path.join("images", "cutscenes")
_CHARACTERS_PATH = os.path.join("images", "characters")

SFX_RESOURCES = loadSound(_SFX_PATH)
ICON_RESOURCES = loadAnimations(_ICONS_PATH)
MENU_RESOURCES = loadAnimations(_MENUS_PATH)
ZONE1_RESOURCES = loadAnimations(_ZONE1_PATH)
ZONE2_RESOURCES = loadAnimations(_ZONE2_PATH)
CUTSCENE_RESOURCES = loadAnimations(_CUTSCENES_PATH)
CHARACTER_RESOURCES = loadAnimations(_CHARACTERS_PATH)
