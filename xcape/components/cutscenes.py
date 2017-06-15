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

        self.state = "talk_cat"
        self.animation = AnimationComponent(self)
        self.animation.add("talk_dog", intro["office_dog"], 300)
        self.animation.add("talk_cat", intro["office_cat"], 300)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.OFFICE_1, 358, 165, "caption")
        self.dialogue.add(dialogue.OFFICE_2, 166, 164, "left")
        self.dialogue.add(dialogue.OFFICE_3, 358, 165)
        self.dialogue.add(dialogue.OFFICE_4, 166, 164, "left")

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self.speed = 100
        self.isSentMessage = False

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.messageNextScene()

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.speed*500 > self.elapsed >= self.speed*0:
            self.state = "talk_cat"

        elif self.speed*3600 > self.elapsed:
            self.state = "talk_cat"
            self.dialogue.index = 0

        elif self.speed*7200 > self.elapsed:
            self.state = "talk_dog"
            self.dialogue.index = 1

        elif self.speed*10800 > self.elapsed:
            self.state = "talk_cat"
            self.dialogue.index = 2

        elif self.speed*14400 >= self.elapsed:
            self.state = "talk_dog"
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
        assets = cutsceneResources["assets"]

        self.state = "no_telephone"
        self.animation = AnimationComponent(self)
        self.animation.add("pick_telephone", intro["telephone"], 1100)
        self.animation.add("no_telephone", [intro["telephone"][0]], float('inf'))
        self.animation.add("hold_telephone", [intro["telephone"][4]], float('inf'))

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
            self.state = "no_telephone"

        elif self.speed*2800 > self.elapsed:
            self.state = "pick_telephone"

        elif self.speed*3300 > self.elapsed:
            self.state = "hold_telephone"

        elif self.speed*6300 > self.elapsed:
            self.state = "hold_telephone"
            self.dialogue.index = 1

        elif self.speed*10300 > self.elapsed:
            self.state = "hold_telephone"
            self.dialogue.index = 2

        elif self.speed*11300 > self.elapsed:
            self.state = "hold_telephone"
            self.dialogue.index = 0

        elif self.speed*12100 > self.elapsed:
            self.state = "pick_telephone"
            self.animation.update()     # Needed to apply immediate update
            if not self.isReversed:
                self.animation.reverse()
                self.isReversed = True

        elif self.speed*14000 > self.elapsed:
            self.state = "no_telephone"

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
        assets = cutsceneResources["assets"]

        self.state = "empty_jail"
        self.animation = AnimationComponent(self)
        self.animation.add("escort", intro["jail"], 2500)
        self.animation.add("empty_jail", [intro["jail"][0]], float('inf'))

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(assets["jail_1.png"], 19, 25)

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self.speed = 100
        self.isComplete = False

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._messageStart()

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.speed*3000 > self.elapsed >= self.speed*0:
            self.state = "empty_jail"
            self.dialogue.index = 1

        elif self.speed*5500 > self.elapsed:
            self.state = "escort"
            self.dialogue.index = 0

        elif self.speed*6500 > self.elapsed:
            self.state = "empty_jail"

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
