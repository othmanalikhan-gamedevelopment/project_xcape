"""
Responsible for simplifying the event-driven communication between game objects.
"""

import pygame as pg


MENU_EVENT = pg.USEREVENT + 1
SCENE_EVENT = pg.USEREVENT + 2
CUTSCENE_EVENT = pg.USEREVENT + 3


def messageMenu(sender, category, data=None):
    """
    Creates an event that is posted for the menu engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    CATEGORIES = ["transition", "health"]
    _messageEngine(CATEGORIES, MENU_EVENT, sender, category, data)


def messageScene(sender, category, data=None):
    """
    Creates an event that is posted for the menu engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    CATEGORIES = ["transition", "switch"]
    _messageEngine(CATEGORIES, SCENE_EVENT, sender, category, data)


def messageCutScene(sender, category, data=None):
    """
    Creates an event that is posted for the cut scene engine.

    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    CATEGORIES = ["transition"]
    _messageEngine(CATEGORIES, CUTSCENE_EVENT, sender, category, data)


def _messageEngine(CATEGORIES, EVENT, sender, category, data=None):
    """
    Creates an event that is posted to an engine.

    :param CATEGORIES: List, containing strings of valid categories.
    :param EVENT: pygame.event, the event that the engine handles.
    :param sender: String, the sender of the message.
    :param category: String, the category of the message.
    :param data: N-Tuple, containing the data for the relevant category.
    """
    if category not in CATEGORIES:
        raise KeyError("Invalid category! The categories allowed are {}!"
                       .format(CATEGORIES))

    contents = \
        {
            "sender": sender,
            "category": category,
            "data": data
        }

    message = pg.event.Event(EVENT, contents)
    pg.event.post(message)
