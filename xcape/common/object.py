"""
Responsible for reducing duplicate documentation by inheriting docstrings.
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
        pass

    def update(self):
        """
        Updates the logic of the game object every game tick.
        """
        pass

    def draw(self):
        """
        Renders the game object to the screen every game tick.
        """
        pass

