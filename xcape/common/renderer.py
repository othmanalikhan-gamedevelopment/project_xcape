"""
Responsible for loading common rendering resources.
"""

import os

import pygame as pg


class Renderer:
    """
    Container class that holds common game resources.
    """

    def __init__(self):
        self.FONT_NAME = self.initialiseFonts()
        self.COLOURS = self.initialiseColours()
        self.IMAGES = self.initialiseImages()

    def initialiseFonts(self):
        """
        Initialises the font resources.

        :return: String, the name of the font used in-game.
        """
        FONT_NAME = "m04fatalfuryblack"
        return FONT_NAME

    def initialiseColours(self):
        """
        Initialises the colour resources.

        :return: Dictionary, mapping name of the colour to an RGB value.
        """
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
        return COLOURS

    def initialiseImages(self):
        """
        Initialises the image resource.

        :return: _ImageLoader, an object that has images loaded.
        """
        imageLoader = _ImageLoader()
        return imageLoader


class _ImageLoader:
    """
    Responsible for loading all game assets (images) only once.
    """
    MENUS_PATH = os.path.join("images", "menus")
    SCENES_PATH = os.path.join("images", "scenes")
    CHARACTERS_PATH = os.path.join("images", "characters")

    def __init__(self):
        self.menu = self._loadMenus()
        self.scene = self._loadScenes()
        self.characters = {}

    def _loadMenus(self):
        """
        Loads all the images for the menus.

        :return: 2D Dictionary, mapping dir and file name to image.
        """
        menu = {}
        root = _ImageLoader.MENUS_PATH

        for d in os.listdir(root):
            menu[d] = {}

            for f in os.listdir(os.path.join(root, d)):
                image = self._loadImage(os.path.join(root, d, f))
                menu[d][f] = image

        return menu

    def _loadScenes(self):
        """
        Loads all the images for the scenes.

        :return: 2D Dictionary, mapping dir and file name to image.
        """
        scene = {}
        root = _ImageLoader.SCENES_PATH

        for d in os.listdir(root):
            scene[d] = {}

            for f in os.listdir(os.path.join(root, d)):
                image = self._loadImage(os.path.join(root, d, f))
                scene[d][f] = image

        return scene

    def _loadImage(self, path, alpha=False):
        """
        Loads an image using pygame modules.

        :param path: os.path, the path to the image.
        :param alpha: Boolean, determining whether to apply alpha pixels.
        :return: pygame.Surface, representing the loaded image.
        """
        image = pg.image.load(path)

        if alpha is True:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image


class _SpriteSheet:

    def __init__(self, file_name):
        ruta = os.path.join("imagenes", file_name)
        self.sprite_sheet = pygame.image.load(ruta).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height])
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(WHITE)
        return image
