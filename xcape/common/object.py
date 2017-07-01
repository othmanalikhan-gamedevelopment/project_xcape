"""
The base class that all other classes should inherit from.

The methods provided from this class simplifies event-driven communication.
"""

import pygame as pg


class GameObject:
    """
    The base class for all other classes.
    """

    MENU_EVENT = pg.USEREVENT + 1
    SCENE_EVENT = pg.USEREVENT + 2
    CUTSCENE_EVENT = pg.USEREVENT + 3

    CATEGORIES_MENU = [
        "screen",
        "transition",
        "complete",
        "health",
        "max_health"
    ]
    CATEGORIES_SCENE = [
        "screen",
        "transition",
        "complete",
        "pause",
        "unpause",
        "no_mode",
        "start_game",
        "switch",
        "door",
        "death",
        "revive"
    ]
    CATEGORIES_CUTSCENE = [
        "screen",
        "transition"
    ]

    def handleEvent(self, event):
        """
        Handles the given event.

        :param event: pygame.Event, allowing event-driven programming.
        """
        raise NotImplementedError

    def update(self):
        """
        Updates the logic of the game object every game tick.
        """
        raise NotImplementedError

    def draw(self, camera=None):
        """
        Renders the game object to the screen every game tick.
        """
        raise NotImplementedError

    def messageMenu(self, category, data=None):
        """
        Creates an event that is posted for the menu engine.

        :param category: String, the category of the message.
        :param data: N-Tuple, containing the data for the relevant category.
        """
        self._messageEngine(GameObject.CATEGORIES_MENU,
                            GameObject.MENU_EVENT,
                            self.__str__(),
                            category,
                            data)

    def messageScene(self, category, data=None):
        """
        Creates an event that is posted for the scene engine.

        :param sender: String, the sender of the message.
        :param category: String, the category of the message.
        :param data: N-Tuple, containing the data for the relevant category.
        """
        self._messageEngine(GameObject.CATEGORIES_SCENE,
                            GameObject.SCENE_EVENT,
                            self.__str__(),
                            category,
                            data)

    def messageCutScene(self, category, data=None):
        """
        Creates an event that is posted for the cutscene engine.

        :param category: String, the category of the message.
        :param data: N-Tuple, containing the data for the relevant category.
        """
        self._messageEngine(GameObject.CATEGORIES_CUTSCENE,
                            GameObject.CUTSCENE_EVENT,
                            self.__str__(),
                            category,
                            data)

    def _messageEngine(self, CATEGORIES, EVENT, sender, category, data=None):
        """
        Creates an event that is posted to an engine.

        :param CATEGORIES: List, containing strings of valid categories.
        :param EVENT: pygame.event, the event that the engine handles.
        :param sender: String, the sender of the message.
        :param category: String, the category of the message.
        :param data: N-Tuple, containing the data for the relevant category.
        """
        if category not in CATEGORIES:
            raise KeyError("'{}' is an invalid category! The categories allowed "
                           "are {}!".format(category, CATEGORIES))

        contents = \
            {
                "sender": sender,
                "category": category,
                "data": data
            }

        message = pg.event.Event(EVENT, contents)
        pg.event.post(message)

