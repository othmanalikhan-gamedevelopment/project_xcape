"""
Responsible for simplifying the event-driven communication between game objects.
"""

import pygame as pg


MENU_EVENT = pg.USEREVENT + 1
SCENE_EVENT = pg.USEREVENT + 2

_MENU_CATEGORY = ["transition"]
_SCENE_CATEGORY = ["transition"]


def messageMenu(sender, category, data=None):
    """
    Creates a message that should be posted to the menu engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    if category not in _MENU_CATEGORY:
        raise KeyError("Categories allowed are {}!".format(_MENU_CATEGORY))

    contents = \
        {
            "sender": sender,
            "category": category,
            "data": data
        }
    message = pg.event.Event(MENU_EVENT, contents)
    pg.event.post(message)


def messageScene(sender, category, data=None):
    """
    Creates a message that should be posted to the scene engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    if category not in _SCENE_CATEGORY:
        raise KeyError("Categories allowed are {}!".format(_SCENE_CATEGORY))

    contents = \
        {
            "sender": sender,
            "category": category,
            "data": data
        }
    message = pg.event.Event(SCENE_EVENT, contents)
    pg.event.post(message)


#
# #=================Constants====================
# WIDTH = 640
# HEIGHT = 480
# FPS = 60
# TITLE = "Prison xCape"
# FONT_NAME = "m04fatalfuryblack"
#
# #=================Colors=======================
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)
# GREEN = (0, 255, 0)
# BLUE = (0, 0, 255)
# YELLOW = (255, 255, 0)
# CYAN = (0, 255, 255)
# GRAY = (27, 27, 27)
# LEVEL_ONE_COLOR = (35, 21, 21)
#
# #==============Importing images================
# def load_image(nombre, dir_imagen, alpha=False):
#     ruta = os.path.join(dir_imagen, nombre)
#     try:
#         image = pygame.image.load(ruta)
#     except:
#         print("Error, no se puede cargar la imagen: " + ruta)
#         sys.exit(1)
#     if alpha is True:
#         image = image.convert_alpha()
#         pass
#     else:
#         image = image.convert()
#     return image
#
# class SpriteSheet:
#     sprite_sheet = None
#
#     def __init__(self, file_name):
#         ruta = os.path.join("imagenes", file_name)
#         self.sprite_sheet = pygame.image.load(ruta).convert()
#
#     def get_image(self, x, y, width, height):
#         image = pygame.Surface([width, height])
#         image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
#         image.set_colorkey(WHITE)
#         return image
