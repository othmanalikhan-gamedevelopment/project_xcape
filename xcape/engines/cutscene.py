"""
The cutscene engine of the game.
"""

import xcape.components.cutscenes as cutscenes

import xcape.common.events as events
import xcape.common.loader as loader
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
        self.resources = loader.loadContent(loader.CUTSCENES_PATH)

        self.cutscene = cutscenes.OfficeCutscene(self.screen, self.resources)
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
                self.cutscene = cutscene(self.screen, self.resources)

    def update(self):
        self.cutscene.update()

    def draw(self):
        self.cutscene.draw()
