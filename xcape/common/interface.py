"""
The main purpose of this module is to reduce duplicate docstrings throughout
the project by allowing classes to inherit docstrings.
"""


class GameObject:
    """
    The interface for every class throughout the project.
    """

    def __init__(self):
        raise NotImplementedError

    def handleEvent(self, event):
        """
        Handles the given single pygame event.

        :param event: pygame.Event.
        """
        raise NotImplementedError

    def update(self):
        """
        Updates the state of the game object every game tick.
        """
        raise NotImplementedError

    def draw(self):
        """
        Renders the game object onto the screen every game tick.
        """
        raise NotImplementedError
