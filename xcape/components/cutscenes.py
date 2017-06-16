"""
Responsible for containing all the cutscenes in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.components.dialogue as dialogue
from xcape.common.loader import cutsceneResources
from xcape.common.object import GameObject
from xcape.common.render import Dialogue
from xcape.components.animation import AnimationComponent


class BaseCutscene(GameObject):
    """
    The base cutscene for any cutscene.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.rect = pg.Rect(0, 0, 0, 0)
        self.state = "idle"

    def handleEvent(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class OfficeCutscene(BaseCutscene):
    """
    The cutscene where the dog and cat are talking in the office.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)
        intro = cutsceneResources["intro"]

        self.state = "office_cat"
        self.animation = AnimationComponent(self)
        self.animation.add("office_dog", intro["office_dog"], 1500)
        self.animation.add("office_cat", intro["office_cat"], 1500)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.OFFICE_1, 240, 50, "left")
        self.dialogue.add(dialogue.OFFICE_2, 370, 100)
        self.dialogue.add(dialogue.OFFICE_3, 240, 50, "left")
        self.dialogue.add(dialogue.OFFICE_4, 370, 100)

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self.speed = 1
        self.isSentMessage = False

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.messageNextScene()

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.speed*500 > self.elapsed >= self.speed*0:
            self.state = "office_cat"

        elif self.speed*3600 > self.elapsed:
            self.state = "office_cat"
            self.dialogue.index = 0

        elif self.speed*7200 > self.elapsed:
            self.state = "office_dog"
            self.dialogue.index = 1

        elif self.speed*10800 > self.elapsed:
            self.state = "office_cat"
            self.dialogue.index = 2

        elif self.speed*14400 >= self.elapsed:
            self.state = "office_dog"
            self.dialogue.index = 3

        else:
            self.messageNextScene()

        self.animation.update()

    def draw(self):
        self.animation.draw()
        self.dialogue.draw()

    def messageNextScene(self):
        """
        Sends a message to play the next cutscene.
        """
        if not self.isSentMessage:
            events.messageCutScene("office_cutscene",
                                   "transition",
                                   "telephone_cutscene")
            self.isSentMessage = True


class TelephoneCutscene(BaseCutscene):
    """
    The cutscene where the dog is talking on the phone.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)
        intro = cutsceneResources["intro"]

        self.state = "telephone_none"
        self.animation = AnimationComponent(self, enableRepeat=False)
        self.animation.add("telephone_none", intro["telephone_none"], float('inf'))
        self.animation.add("telephone_pick", intro["telephone_pick"], 1100)
        self.animation.add("telephone_hold", intro["telephone_hold"], float('inf'))
        self.animation.add("telephone_put", intro["telephone_put"], 1100)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.TELEPHONE_1, 350, 150, "left")
        self.dialogue.add(dialogue.TELEPHONE_2, 350, 150, "left")

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
            self.state = "telephone_none"

        elif self.speed*2800 > self.elapsed:
            self.state = "telephone_pick"

        elif self.speed*3300 > self.elapsed:
            self.state = "telephone_hold"

        elif self.speed*6300 > self.elapsed:
            self.state = "telephone_hold"
            self.dialogue.index = 0

        elif self.speed*10300 > self.elapsed:
            self.state = "telephone_hold"
            self.dialogue.index = 1

        elif self.speed*11300 > self.elapsed:
            self.state = "telephone_hold"
            self.dialogue.index = None

        elif self.speed*12100 > self.elapsed:
            self.state = "telephone_put"

        elif self.speed*14000 > self.elapsed:
            self.state = "telephone_none"

        else:
            if not self.isComplete:
                self.isComplete = True
                events.messageCutScene("telephone_cutscene",
                                       "transition",
                                       "jail_cutscene")

        self.animation.update()

    def draw(self):
        self.animation.draw()
        self.dialogue.draw()


class JailCutscene(BaseCutscene):
    """
    The cutscene where the cat is being escorted to jail.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)
        intro = cutsceneResources["intro"]

        self.state = "jail"
        self.animation = AnimationComponent(self, enableRepeat=False)
        self.animation.add("fence_show", intro["jail_fence_show"], 2000)
        self.animation.add("fence_static", intro["jail_fence_static"], float("inf"))
        self.animation.add("fence_hide", intro["jail_fence_hide"], 2000)
        self.animation.add("cat_static", intro["jail_cat_static"], float('inf'))
        self.animation.add("cat_close", intro["jail_cat_close"], 3500)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.JAIL_1, 19, 25, "caption")

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self.speed = 1
        self.isComplete = False

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._messageStart()

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.speed*2000 > self.elapsed >= self.speed*0:
            self.state = "fence_show"
            self.dialogue.index = 0

        elif self.speed*4000 > self.elapsed:
            self.state = "fence_static"
            self.dialogue.index = None

        elif self.speed*6000 > self.elapsed:
            self.state = "fence_hide"

        elif self.speed*9500 > self.elapsed:
            self.state = "cat_close"

        elif self.speed*11500 > self.elapsed:
            self.state = "cat_static"

        else:
            if not self.isComplete:
                self.isComplete = True
                self._messageStart()

        self.animation.update()

    def draw(self):
        self.animation.draw()
        self.dialogue.draw()

    def _messageStart(self):
        """
        Sends out events to end the cutscene and start playing the game.
        """
        events.messageCutScene("jail_cutscene", "transition", "blank_cutscene")
        events.messageScene("jail_cutscene", "start_game", "solo")
