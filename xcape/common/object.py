"""
Responsible for mainly reducing duplicate documentation by inheriting
docstrings.
"""


class GameObject:
    """
    The interface for every class throughout the project.
    """

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

    def draw(self):
        """
        Renders the game object to the screen every game tick.
        """
        raise NotImplementedError

