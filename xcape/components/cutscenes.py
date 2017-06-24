"""
Responsible for containing all the cutscenes in game.
"""

import pygame as pg

import xcape.components.dialogue as dialogue
from xcape.common.loader import CUTSCENE_RESOURCES
from xcape.common.object import GameObject
from xcape.components.audio import AudioComponent
from xcape.components.render import RenderComponent, Dialogue


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

    def handleEvent(self, event):
        pass

    def update(self):
        pass

    def draw(self, camera=None):
        pass


# TODO: Add audio
class OfficeCutscene(BaseCutscene):
    """
    The cutscene where the dog and cat are talking in the office.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)
        office = CUTSCENE_RESOURCES["office"]

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self._isSentMessage = False

        self.render = RenderComponent(self)
        self.render.add("office_dog", office["dog"], 1500)
        self.render.add("office_cat", office["cat"], 1500)

        self.audio = AudioComponent(self, isAutoPlay=False)
        # self.audio.add("meow", SFX_RESOURCES["meow_1"])

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.OFFICE_1, 240, 50, "left")
        self.dialogue.add(dialogue.OFFICE_2, 370, 100)
        self.dialogue.add(dialogue.OFFICE_3, 240, 50, "left")
        self.dialogue.add(dialogue.OFFICE_4, 370, 100)

        speed = 1
        ts = [0, 1000, 1500, 4600, 8200, 11800, 15400]
        self.timings = [speed*t for t in ts]

    def __str__(self):
        return "office_cutscene"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._messageNextScene()

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.timings[0] > self.elapsed:
            self.render.state = "office_dog"
            self.dialogue.index = None

        elif self.timings[1] > self.elapsed:
            self.render.state = "office_cat"
            self.dialogue.index = 0

        elif self.timings[2] > self.elapsed:
            self.render.state = "office_dog"
            self.dialogue.index = 1

        elif self.timings[3] > self.elapsed:
            self.render.state = "office_cat"
            self.dialogue.index = 2

        elif self.timings[4] >= self.elapsed:
            self.render.state = "office_dog"
            self.dialogue.index = 3

        else:
            self._messageNextScene()

        self.dialogue.update()
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.dialogue.draw()

    def _messageNextScene(self):
        """
        Sends a message to play the next cutscene.
        """
        if not self._isSentMessage:
            self.messageCutScene("transition", "telephone_cutscene")
            self._isSentMessage = True


# TODO: Add audio
class TelephoneCutscene(BaseCutscene):
    """
    The cutscene where the dog is talking on the phone.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)
        telephone = CUTSCENE_RESOURCES["telephone"]

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self._isComplete = False
        self._isReversed = False

        self.render = RenderComponent(self, enableRepeat=False)
        self.render.add("telephone_none", telephone["none"])
        self.render.add("telephone_pick", telephone["pick"], 1100)
        self.render.add("telephone_hold", telephone["hold"])
        self.render.add("telephone_put", telephone["put"], 1100)

        self.audio = AudioComponent(self)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.TELEPHONE_1, 350, 150, "left")
        self.dialogue.add(dialogue.TELEPHONE_2, 350, 150, "left")

        speed = 1
        ts = [2000, 2800, 3300, 6300, 10300, 11300, 12100, 14000]
        self.timings = [speed*t for t in ts]

    def __str__(self):
        return "telephone_cutscene"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.messageCutScene("transition", "jail_cutscene")

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.timings[0] > self.elapsed:
            self.render.state = "telephone_none"
            self.dialogue.index = None

        elif self.timings[1] > self.elapsed:
            self.render.state = "telephone_pick"
            self.dialogue.index = None

        elif self.timings[2] > self.elapsed:
            self.render.state = "telephone_hold"
            self.dialogue.index = None

        elif self.timings[3] > self.elapsed:
            self.render.state = "telephone_hold"
            self.dialogue.index = 0

        elif self.timings[4] > self.elapsed:
            self.render.state = "telephone_hold"
            self.dialogue.index = 1

        elif self.timings[5] > self.elapsed:
            self.render.state = "telephone_hold"
            self.dialogue.index = None

        elif self.timings[6] > self.elapsed:
            self.render.state = "telephone_put"
            self.dialogue.index = None

        elif self.timings[7] > self.elapsed:
            self.render.state = "telephone_none"
            self.dialogue.index = None

        else:
            if not self._isComplete:
                self._isComplete = True
                self.messageCutScene("transition", "jail_cutscene")

        self.dialogue.update()
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.dialogue.draw()


# TODO: Add audio
class JailCutscene(BaseCutscene):
    """
    The cutscene where the cat is being escorted to jail.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)
        jail = CUTSCENE_RESOURCES["jail"]

        self.origin = pg.time.get_ticks()       # milliseconds
        self.elapsed = 0                        # milliseconds
        self._isComplete = False

        self.render = RenderComponent(self, enableRepeat=False)
        self.render.add("fence_show", jail["fence_show"], 2000)
        self.render.add("fence_static", jail["fence_static"])
        self.render.add("fence_hide", jail["fence_hide"], 2000)
        self.render.add("cat_static", jail["cat_static"])
        self.render.add("cat_close", jail["cat_close"], 3500)

        self.audio = AudioComponent(self)

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.JAIL_1, 19, 25, "caption")

        speed = 1
        ts = [2000, 4000, 6000, 9500, 11500]
        self.timings = [speed*t for t in ts]

    def __str__(self):
        return "jail_cutscene"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self._messageStart()

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if self.timings[0] > self.elapsed:
            self.render.state = "fence_show"
            self.dialogue.index = 0

        elif self.timings[1] > self.elapsed:
            self.render.state = "fence_static"
            self.dialogue.index = None

        elif self.timings[2] > self.elapsed:
            self.render.state = "fence_hide"
            self.dialogue.index = None

        elif self.timings[3] > self.elapsed:
            self.render.state = "cat_close"
            self.dialogue.index = None

        elif self.timings[4] > self.elapsed:
            self.render.state = "cat_static"
            self.dialogue.index = None

        else:
            if not self._isComplete:
                self._isComplete = True
                self._messageStart()

        self.dialogue.update()
        self.render.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.dialogue.draw()

    def _messageStart(self):
        """
        Sends out events to end the cutscene and start playing the game.
        """
        self.messageCutScene("transition", "blank_cutscene")
        self.messageScene("start_game", "solo")
