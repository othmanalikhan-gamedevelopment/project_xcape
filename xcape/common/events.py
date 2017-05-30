"""
Responsible for simplifying the event-driven communication between game objects.
"""

import pygame as pg


MENU_EVENT = pg.USEREVENT + 1
SCENE_EVENT = pg.USEREVENT + 2



def messageMenu(sender, category, data=None):
    """
    Creates an event that is posted for the menu engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    MENU_CATEGORY = ["transition"]
    if category not in MENU_CATEGORY:
        raise KeyError("Categories allowed are {}!".format(MENU_CATEGORY))

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
    Creates an event that is posted for the menu engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    SCENE_CATEGORY = ["transition"]
    if category not in SCENE_CATEGORY:
        raise KeyError("Categories allowed are {}!".format(SCENE_CATEGORY))

    contents = \
        {
            "sender": sender,
            "category": category,
            "data": data
        }
    message = pg.event.Event(SCENE_EVENT, contents)
    pg.event.post(message)
