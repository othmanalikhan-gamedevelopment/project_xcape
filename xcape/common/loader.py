"""
Responsible for loading common rendering resources.
"""

import os

import pygame as pg
import xcape.common.settings as settings

MENUS_PATH = os.path.join("images", "menus")
SCENES_PATH = os.path.join("images", "scenes")


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
        static animations:    content[subDir1][imageName] = image
        dynamic animations:   content[subDir1][animationDir] = [image1, image2]
    """
    content = {}

    for depth1 in os.listdir(path):
        content[depth1] = {}
        pathDepth1 = os.path.join(path, depth1)

        for depth2 in os.listdir(pathDepth1):
            pathDepth2 = os.path.join(path, depth1, depth2)

            # Loading static animations
            if os.path.isfile(pathDepth2):
                content[depth1][depth2] = loadImage(pathDepth2)

            # Loading dynamic animations
            else:
                animation = []
                for frame in os.listdir(pathDepth2):
                    pathDepth3 = os.path.join(path, depth1, depth2, frame)
                    animation.append(loadImage(pathDepth3))
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
        image.set_colorkey(settings.COLOURS["white"])
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
