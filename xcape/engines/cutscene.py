"""
The cutscene engine of the game.
"""

import pygame as pg

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

        self.cutscene = None
        self.nameToCutscene = \
            {
                "blank_cutscene": None,
                "office_cutscene": cutscenes.OfficeCutscene,
                "telephone_cutscene": cutscenes.TelephoneCutscene,
                "jail_cutscene": cutscenes.JailCutscene,
                "pig_cutscene": cutscenes.PigCutscene,
            }

    def handleEvent(self, event):
        if self.cutscene:
            self.cutscene.handleEvent(event)

        if event.type == self.CUTSCENE_EVENT:
            if event.category == "transition":
                try:
                    cutscene = self.nameToCutscene[event.data]
                    self.cutscene = cutscene(self.screen)
                except TypeError:
                    self.cutscene = cutscene

            if event.category == "screen":
                self.screen = pg.display.get_surface()

    def update(self):
        if self.cutscene:
            self.cutscene.update()

    def draw(self, camera=None):
        if self.cutscene:
            self.cutscene.draw()
