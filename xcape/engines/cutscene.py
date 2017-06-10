"""
The cutscene engine of the game.
"""

import xcape.common.events as events
import xcape.components.cutscenes as cutscenes
from xcape.common.object import GameObject


class CutSceneEngine(GameObject):
    """
    Responsibilities:
        - Displaying and updating the current cutscene.
        - Transitioning between cutscenes.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen

        self.cutscene = cutscenes.BlankCutscene(self.screen)
        self.nameToCutscene = \
            {
                "blank_cutscene": cutscenes.BlankCutscene,
                "office_cutscene": cutscenes.OfficeCutscene,
                "telephone_cutscene": cutscenes.TelephoneCutscene,
                "jail_cutscene": cutscenes.JailCutscene
            }

    def handleEvent(self, event):
        self.cutscene.handleEvent(event)

        if event.type == events.CUTSCENE_EVENT:
            if event.category == "transition":
                cutscene = self.nameToCutscene[event.data]
                self.cutscene = cutscene(self.screen)

    def update(self):
        self.cutscene.update()

    def draw(self):
        self.cutscene.draw()
