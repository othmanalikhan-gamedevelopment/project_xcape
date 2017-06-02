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

        self.state = "office_cat"
        self.animation = AnimationComponent(self)
        self.animation.addDynamic("office_dog", intro["office_dog"], 300)
        self.animation.addDynamic("office_cat", intro["office_cat"], 300)

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
            self.state = "office_cat"
            if self.elapsed > self.speed*100:
                self.dialogue.index = 1

        elif self.speed*7200 > self.elapsed:
            self.state = "office_dog"
            self.dialogue.index = 2

        elif self.speed*10800 > self.elapsed:
            self.state = "office_cat"
            self.dialogue.index = 3

        elif self.speed*14400 >= self.elapsed:
            self.state = "office_dog"
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


class TelephoneCutscene(ICutscene):
    """
    The cutscene where the dog is talking on the phone.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)
        intro = self.resources["intro"]
        assets = self.resources["assets"]

        self.state = "telephone_0"
        self.animation = AnimationComponent(self)
        self.animation.addDynamic("telephone", intro["telephone"], 1100)
        self.animation.addStatic("telephone_0", intro["telephone"][0])
        self.animation.addStatic("telephone_4", intro["telephone"][4])

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(assets["telephone_1.png"], 375, 100)
        self.dialogue.add(assets["telephone_2.png"], 375, 100)

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self.speed = 1
        self.isComplete = False
        self.isReversed = False

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageCutScene("telephone_cutscene",
                                       "transition",
                                       "jail_cutscene")

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.speed*2000 > self.elapsed >= self.speed*0:
            self.state = "telephone_0"

        elif self.speed*2800 > self.elapsed:
            self.state = "telephone"

        elif self.speed*3300 > self.elapsed:
            self.state = "telephone_4"

        elif self.speed*6300 > self.elapsed:
            self.state = "telephone_4"
            self.dialogue.index = 1

        elif self.speed*8300 > self.elapsed:
            self.state = "telephone_4"
            self.dialogue.index = 2

        elif self.speed*9300 > self.elapsed:
            self.state = "telephone_4"
            self.dialogue.index = 0

        elif self.speed*10100 > self.elapsed:
            self.state = "telephone"

            if not self.isReversed:
                self.animation.reverse()
                self.isReversed = True

        elif self.speed*12000 > self.elapsed:
            self.state = "telephone_0"

        else:
            if not self.isComplete:
                self.isComplete = True
                events.messageCutScene("telephone_cutscene",
                                       "transition",
                                       "jail_cutscene")

        self.dialogue.update()
        self.animation.update()

    def draw(self):
        self.animation.draw()
        self.dialogue.draw()


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

