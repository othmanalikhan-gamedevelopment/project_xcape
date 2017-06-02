"""
Responsible for containing all the cutscenes in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.render as render
import xcape.common.settings as settings
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent


class ICutscene(GameObject):
    """
    A base cutscene for any cutscenes.
    """

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        self.screen = screen
        self.resources = resources
        self.rect = pg.Rect(0, 0, 0, 0)

    def handleEvent(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class BlankCutscene(ICutscene):
    """
    A blank cutscene that does nothing except display a blank screen.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)


class OfficeCutscene(ICutscene):
    """
    The cutscene where the dog and cat are talking in the office.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)
        intro = self.resources["intro"]
        assets = self.resources["assets"]

        self.state = "speak_cat"
        self.animation = AnimationComponent(self)
        self.animation.addDynamic("speak_dog", intro["speak_dog"], 300)
        self.animation.addDynamic("speak_cat", intro["speak_cat"], 300)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(assets["office_1.png"], 358, 165)
        self.dialogue.add(assets["office_2.png"], 166, 164)
        self.dialogue.add(assets["office_3.png"], 358, 165)
        self.dialogue.add(assets["office_4.png"], 166, 164)

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self.speed = 1
        self.isComplete = False

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageCutScene("office_cutscene",
                                       "transition",
                                       "telephone_cutscene")

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.speed*3600 > self.elapsed >= self.speed*0:
            self.state = "speak_cat"
            if self.elapsed > self.speed*100:
                self.dialogue.index = 1

        elif self.speed*7200 > self.elapsed:
            self.state = "speak_dog"
            self.dialogue.index = 2

        elif self.speed*10800 > self.elapsed:
            self.state = "speak_cat"
            self.dialogue.index = 3

        elif self.speed*14400 >= self.elapsed:
            self.state = "speak_dog"
            self.dialogue.index = 4

        else:
            if not self.isComplete:
                self.isComplete = True
                events.messageCutScene("office_cutscene",
                                       "transition",
                                       "telephone_cutscene")

        self.dialogue.update()
        self.animation.update()

    def draw(self):
        self.animation.draw()
        self.dialogue.draw()

#
# class SoloCutscene(ICutscene):
#     """
#     The single player cutscene.
#     """
#
#     def __init__(self, screen, resources):
#         super().__init__(screen, resources)
#         self.rect = pg.Rect(0, 0, 0, 0)
#         intro = self.resources["intro"]
#         assets = self.resources["assets"]
#
#         self.state = "telephone_0"
#         self.animation = AnimationComponent(self)
#         self.animation.addDynamic("speak_dog", intro["speak_dog"], 300)
#         self.animation.addDynamic("speak_cat", intro["speak_cat"], 300)
#         self.animation.addDynamic("jail", intro["jail"], 1700)
#         self.animation.addDynamic("telephone", intro["telephone_dog"], 700)
#         self.animation.addStatic("jail_0", intro["jail"][0])
#         self.animation.addStatic("telephone_0", intro["telephone_dog"][0])
#         self.animation.addStatic("telephone_4", intro["telephone_dog"][4])
#
#         self.dialogue = Dialogue(self.screen)
#         self.dialogue.add(assets["globe_1.png"], 358, 165)
#         self.dialogue.add(assets["globe_2.png"], 166, 164)
#         self.dialogue.add(assets["globe_3.png"], 358, 165)
#         self.dialogue.add(assets["globe_4.png"], 166, 164)
#         self.dialogue.add(assets["globe_5.png"], 375, 100)
#         self.dialogue.add(assets["globe_6.png"], 375, 100)
#         self.dialogue.add(assets["globe_7.png"], 19, 25)
#
#         # Units are in milliseconds
#         self.origin = pg.time.get_ticks()
#         self.elapsed = 0
#
#     def handleEvent(self, event):
#         if event.type == pg.KEYDOWN:
#             if event.key == pg.K_RETURN:
#                 events.messageMenu("solo_cutscene", "transition", "blank_menu")
#                 events.messageScene("solo_cutscene", "transition", "scene_01")
#
#     def update(self):
#         self.elapsed = pg.time.get_ticks() - self.origin + 7200
#
#         # self.updatePartOne()
#         self.updatePartTwo()
#         self.dialogue.update()
#         self.animation.update()
#
#     def updatePartOne(self):
#         """
#         Updates part one of the cutscene.
#         """
#         DEBUG_SPEED = 1     # Keep this to unity unless testing scene speed
#
#         if DEBUG_SPEED*3600 > self.elapsed > DEBUG_SPEED*0:
#             self.state = "speak_cat"
#             if self.elapsed > DEBUG_SPEED*100:
#                 self.dialogue.index = 1
#
#         elif DEBUG_SPEED*7200 > self.elapsed:
#             self.state = "speak_dog"
#             self.dialogue.index = 2
#
#         elif DEBUG_SPEED*10800 > self.elapsed:
#             self.state = "speak_cat"
#             self.dialogue.index = 3
#
#         elif DEBUG_SPEED*14400 > self.elapsed:
#             self.state = "speak_dog"
#             self.dialogue.index = 4
#
#     def updatePartTwo(self):
#         """
#         Updates part two of the cutscene.
#         """
#         print(self.elapsed)
#         DEBUG_SPEED = 10     # Keep this to unity unless testing scene speed
#         self.isReversed = False
#
#         if DEBUG_SPEED*1180 > self.elapsed > DEBUG_SPEED*720:
#             self.state = "telephone"
#
#             if DEBUG_SPEED*900 > self.elapsed:
#                 self.state = "telephone_0"
#                 self.dialogue.index = 5
#
#             elif DEBUG_SPEED*1080 > self.elapsed:
#                 self.dialogue.index = 6
#
#             # else:
#             #     self.state = "telephone"
#             #     self.dialogue.index = 0
#             #
#             #     if not self.isReversed:
#             #         self.animation.flip(True, False)
#             #         self.isReversed = True
#
#
#     def draw(self):
#         self.animation.draw()
#         self.dialogue.draw()


class Dialogue(GameObject):
    """
    Represents a collection of dialogue bubbles.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.bubbles = []
        self.index = 0

        blankBubble = _Bubble(pg.Surface((0, 0)), 0, 0, self.screen)
        self.bubbles.append(blankBubble)

    def update(self):
        self.bubbles[self.index].update()

    def draw(self):
        self.bubbles[self.index].draw()

    def add(self, image, x, y):
        """
        Adds a dialogue bubble.

        :param image: pygame.Surface, representing the image to display.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        """
        self.bubbles.append(_Bubble(image, x, y, self.screen))


class _Bubble(GameObject):
    """
    Represents a dialogue bubble.
    """

    def __init__(self, image, x, y, screen):
        """
        :param image: pygame.Surface, representing the image to display.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param screen: pygame.Surface, representing the screen.
        """
        self.rect = pg.Rect(x, y, 0, 0)
        self.screen = screen

        image = render.addBackground(image)
        image.set_colorkey(settings.COLOURS["blue"])

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", image)

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()

