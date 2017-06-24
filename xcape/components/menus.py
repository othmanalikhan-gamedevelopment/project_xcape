"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.settings as settings
from xcape.common.loader import MENU_RESOURCES, SFX_RESOURCES
from xcape.common.object import GameObject
from xcape.components.audio import AudioComponent
from xcape.components.render import (
    RenderComponent, ImageLabel, TextLabel, addBackground
)


class BaseMenu(GameObject):
    """
    The base menu that should be inherited by all menus.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.rect = pg.Rect(0, 0, 0, 0)

    def handleEvent(self, event):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self, camera=None):
        raise NotImplementedError


class SplashMenu(BaseMenu):
    """
    The splash screen of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.effect = FadeEffect(screen)

        background = MENU_RESOURCES["screens"]["splash"][0]
        background = addBackground(background)
        self.render = RenderComponent(self)
        self.render.add("background", background)
        self.render.state = "background"

        self.audio = AudioComponent(self)
        self.audio.add("door_knock", SFX_RESOURCES["splash_door_knock"])
        self.audio.add("door_open", SFX_RESOURCES["splash_door_open"])
        self.audio.add("door_close", SFX_RESOURCES["splash_door_close"])
        self.audio.add("meow", SFX_RESOURCES["splash_meow"])
        self.audio.link("door_knock", "door_open", delay=1000)
        self.audio.link("door_open", "meow")
        self.audio.link("meow", "door_close")
        self.audio.state = "door_knock"

    def __str__(self):
        return "splash_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.messageMenu("transition", "main_menu")

    def update(self):
        self.audio.update()
        self.render.update()

        if not self.effect.isComplete:
            self.effect.update()
        else:
            self.messageMenu("transition", "main_menu")

    def draw(self, camera=None):
        self.render.draw(camera)
        self.effect.draw()


class MainMenu(BaseMenu):
    """
    The main menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.totalOptions = 4
        self.fontSize = 22
        self.fontColour = "white"
        self.x = 250
        self.y = 155
        self.dx = 0
        self.dy = 38

        self.option1 = TextLabel("1 Jugador",
                                 self.fontSize,
                                 self.fontColour,
                                 self.x,
                                 self.y + 1 * self.dy,
                                 self.screen)
        self.option2 = TextLabel("2 Jugadores",
                                 self.fontSize,
                                 self.fontColour,
                                 self.x,
                                 self.y + 2 * self.dy,
                                 self.screen)
        self.option3 = TextLabel("Opciones",
                                 self.fontSize,
                                 self.fontColour,
                                 self.x,
                                 self.y + 3 * self.dy,
                                 self.screen)
        self.option4 = TextLabel("Salir",
                                 self.fontSize,
                                 self.fontColour,
                                 self.x,
                                 self.y + 4 * self.dy,
                                 self.screen)
        self.title = ImageLabel(MENU_RESOURCES["assets"]["title"][0],
                                60,
                                55,
                                self.screen)
        self.arrow = _Arrow(self.x - 40,
                            self.y + 28,
                            self.dx,
                            self.dy,
                            self.totalOptions,
                            self.screen)

        background = MENU_RESOURCES["screens"]["main"][0]
        self.render = RenderComponent(self)
        self.render.add("background", background)
        self.render.state = "background"

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("enter", SFX_RESOURCES["menu_enter"])

    def __str__(self):
        return "main_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                self.arrow.moveUp()
            if event.key == pg.K_DOWN:
                self.arrow.moveDown()

            if event.key == pg.K_RETURN:
                self.audio.state = "enter"
                if self.arrow.index == 0:
                    self.messageMenu("transition", "blank_menu")
                    self.messageCutScene("transition", "office_cutscene")
                if self.arrow.index == 1:
                    self.messageMenu("transition", "blank_menu")
                    self.messageScene("start_game", "coop")
                if self.arrow.index == 2:
                    self.messageMenu("transition", "options_menu")
                if self.arrow.index == 3:
                    quit()

    def update(self):
        self.render.update()
        self.audio.update()

        self.option1.update()
        self.option2.update()
        self.option3.update()
        self.option4.update()
        self.title.update()
        self.arrow.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.title.draw()
        self.option1.draw()
        self.option2.draw()
        self.option3.draw()
        self.option4.draw()
        self.arrow.draw()


class OptionsMenu(BaseMenu):
    """
    The options menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        fontSize = 22
        fontColour = "white"
        x, y = 230, 155
        dx, dy = 0, 50

        self.backgroundSetting = _SettingsLabel("Background Flip: ",
                                                ["Vertical", "Horizontal"],
                                                fontSize, fontColour,
                                                x, y,
                                                130,
                                                screen)
        self.fullscreenSetting = _SettingsLabel("Full Screen: ",
                                                ["Disable", "Enable"],
                                                fontSize, fontColour,
                                                x, y+dy,
                                                130,
                                                screen)

        self.arrow = _Arrow(x - 40, y - 10, dx, dy, 2, screen)
        self.escapeImage = ImageLabel(MENU_RESOURCES["assets"]["esc"], 25, 440, screen)
        self.escapeText = TextLabel("Esc para volver", 14, fontColour, 50, 445, screen)

        self.effect = FadeEffect(self.screen)
        self.effect.timeStartDarken = float('inf')
        self.effect.timeEndDarken = float('inf')
        self.dt = 2

        background = MENU_RESOURCES["screens"]["options"][0]
        self.render = RenderComponent(self)
        self.render.add("background", background)
        self.render.state = "background"

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("exit", SFX_RESOURCES["menu_exit"])

    def __str__(self):
        return "options_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                self.effect.timeStartDarken = self.effect.time
                self.effect.timeEndDarken = self.effect.time + self.dt
                self.audio.state = "exit"

            if event.key == pg.K_UP:
                self.arrow.moveUp()
            if event.key == pg.K_DOWN:
                self.arrow.moveDown()

            if self.arrow.index == 0:
                if event.key == pg.K_RIGHT:
                    self.backgroundSetting.next()
                if event.key == pg.K_LEFT:
                    self.backgroundSetting.previous()
                if event.key == pg.K_RETURN:
                    if self.backgroundSetting.index == 0:
                        self.render.flip(True, False)
                    if self.backgroundSetting.index == 1:
                        self.render.flip(False, True)

            if self.arrow.index == 1:
                if event.key == pg.K_RIGHT:
                    self.fullscreenSetting.next()
                if event.key == pg.K_LEFT:
                    self.fullscreenSetting.previous()
                if event.key == pg.K_RETURN:
                    if self.fullscreenSetting.index == 0:
                        pg.display.set_mode((settings.WIDTH, settings.HEIGHT))
                    if self.fullscreenSetting.index == 1:
                        pg.display.set_mode((settings.WIDTH, settings.HEIGHT),
                                            pg.FULLSCREEN)

                    self.messageMenu("screen")
                    self.messageScene("screen")
                    self.messageCutScene("screen")

    def update(self):
        self.render.update()
        self.audio.update()
        self.effect.update()

        self.backgroundSetting.update()
        self.fullscreenSetting.update()
        self.escapeImage.update()
        self.escapeText.update()
        self.arrow.update()

        if self.effect.isComplete:
            self.messageMenu("transition", "main_menu")

    def draw(self, camera=None):
        self.render.draw(camera)
        self.backgroundSetting.draw()
        self.fullscreenSetting.draw()
        self.escapeImage.draw()
        self.escapeText.draw()
        self.arrow.draw()
        self.effect.draw()


class DeathMenu(BaseMenu):
    """
    The death screen of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.effect = FadeEffect(screen)
        self.effect.timeStartLighten = 0.0
        self.effect.timeEndLighten = 1.0
        self.effect.timeStartDarken = 1.0
        self.effect.timeEndDarken = 1.5

        image = pg.Surface((settings.WIDTH, settings.HEIGHT))
        image.fill(settings.COLOURS["dark_red"])
        image = image.convert()
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"

        self.audio = AudioComponent(self,
                                    enableAutoPlay=True,
                                    enableRepeat=False)
        self.audio.add("death", SFX_RESOURCES["menu_death"])
        self.audio.state = "death"

    def __str__(self):
        return "death_menu"

    def handleEvent(self, event):
        print("'{}' safely ignored event {}".format(self.__str__(), event))

    def update(self):
        self.render.update()
        self.audio.update()
        self.effect.update()

        if self.effect.isComplete:
            self.messageScene("complete")

    def draw(self, camera=None):
        self.render.draw()
        self.effect.draw()


class LoseMenu(BaseMenu):
    """
    The game over menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.fontSize = 18
        self.fontColour = "white"
        self.x = 150
        self.y = 320

        self.enterText = TextLabel("Enter para salir",
                                   self.fontSize,
                                   self.fontColour,
                                   self.x,
                                   self.y,
                                   self.screen)

        image = MENU_RESOURCES["screens"]["lose"][0]
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("meow", SFX_RESOURCES["menu_lose"])
        self.audio.state = "meow"

    def __str__(self):
        return "lose_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.messageMenu("transition", "splash_menu")
                self.messageScene("no_mode")

    def update(self):
        self.render.update()
        self.audio.update()
        self.enterText.update()

    def draw(self, camera=None):
        self.render.draw()
        self.enterText.draw()


class WinMenu(BaseMenu):
    """
    The win menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.fontSize = 18
        self.fontColour = "white"
        self.x = 150
        self.y = 320

        self.enterText = TextLabel("Enter para salir",
                                   self.fontSize,
                                   self.fontColour,
                                   self.x,
                                   self.y,
                                   self.screen)

        image = MENU_RESOURCES["screens"]["fade"][0]
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"

        self.audio = AudioComponent(self,
                                    enableAutoPlay=False,
                                    enableRepeat=True)
        self.audio.add("win", SFX_RESOURCES["scene_win"])
        self.audio.state = "win"

    def __str__(self):
        return "win_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                self.messageMenu("transition", "main_menu")
                self.messageScene("no_mode")

    def update(self):
        self.render.update()
        self.audio.update()
        self.enterText.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.enterText.draw()


class PauseMenu(BaseMenu):
    """
    The pause menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.fontSize = 50
        self.fontColour = "orange"
        self.x = 270
        self.y = 225

        self.pauseText = TextLabel("Pause",
                                   self.fontSize,
                                   self.fontColour,
                                   self.x,
                                   self.y,
                                   self.screen,
                                   isItalic=True)

        image = MENU_RESOURCES["screens"]["fade"][0]
        self.render = RenderComponent(self)
        self.render.add("background", image)
        self.render.state = "background"

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("pause", SFX_RESOURCES["menu_pause"])
        self.audio.state = "pause"

    def __str__(self):
        return "pause_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.audio.state = "pause"

    def update(self):
        self.render.update()
        self.audio.update()
        self.pauseText.update()

    def draw(self, camera=None):
        self.render.draw(camera)
        self.pauseText.draw()


class FadeEffect(BaseMenu):
    """
    Responsible for applying a transitioning fade of as follows:

    Black screen --> Normal screen --> Black screen
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.transparentValue = 255
        self.isComplete = False

        background = pg.Surface((settings.WIDTH, settings.HEIGHT))
        background.fill(settings.COLOURS["black"])
        background = background.convert()

        self.render = RenderComponent(self)
        self.render.add("background", background)
        self.render.state = "background"

        # Units are in seconds (use floats to reduce rounding errors)
        self.origin = pg.time.get_ticks()/1000
        self.time = 0.0
        self.timeStartLighten = 1.0
        self.timeEndLighten = 3.0
        self.timeStartDarken = 5.0
        self.timeEndDarken = 8.0

    def __str__(self):
        return "fade_effect"

    def update(self):
        self.render.update()

        if not self.isComplete:
            self.time = pg.time.get_ticks()/1000 - self.origin

            if self.timeEndLighten >= self.time >= self.timeStartLighten:
                self.lightenScreen()
            if self.timeEndDarken >= self.time >= self.timeStartDarken:
                self.darkenScreen()

            if self.time > self.timeEndDarken:
                self.isComplete = True

    def draw(self, camera=None):
        self.render.draw(camera)

    def lightenScreen(self):
        """
        Increases the transparency of the background.
        """
        current = self.time - self.timeStartLighten
        duration = self.timeEndLighten - self.timeStartLighten
        percentComplete = current/duration
        self.transparentValue = (1-percentComplete) * 255
        self.render.image.set_alpha(self.transparentValue)

    def darkenScreen(self):
        """
        Reduces the transparency of the background.
        """
        current = self.time - self.timeStartDarken
        duration = self.timeEndDarken - self.timeStartDarken
        percentComplete = current/duration
        self.transparentValue = percentComplete * 255
        self.render.image.set_alpha(self.transparentValue)


class SoloUIMenu(BaseMenu):
    """
    The single player UI in a scene.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.x = 50
        self.y = 50
        self.dx = 30

        self._HP = None
        self._maxHP = None
        self._lives = []

        self._audio = AudioComponent(self, enableAutoPlay=False, enableRepeat=True)
        self._audio.add("healthy", SFX_RESOURCES["menu_heartbeat_healthy"])
        self._audio.add("injured", SFX_RESOURCES["menu_heartbeat_injured"])
        self._audio.add("danger", SFX_RESOURCES["menu_heartbeat_danger"])

    def __str__(self):
        return "solo_ui_menu"

    def handleEvent(self, event):
        if event.type == self.MENU_EVENT:
            if event.category == "max_health":
                self.maxLife = event.data
            if event.category == "health":
                self.currentLife = event.data
                self.audio = event.data

    def update(self):
        self.audio.update()
        for live in self._lives:
            live.render.update()

    def draw(self, camera=None):
        for live in self._lives:
            live.render.draw(camera)

    @property
    def currentLife(self):
        return self._HP

    @currentLife.setter
    def currentLife(self, value):
        for heart in self._lives:
            heart.render.state = "no_life"
        for heart in range(value):
            self._lives[heart].render.state = "life"

    @property
    def maxLife(self):
        return self._maxHP

    @maxLife.setter
    def maxLife(self, value):
        assets = MENU_RESOURCES["assets"]
        for i in range(value):
            label = ImageLabel(None, self.x + i*self.dx, self.y, self.screen)
            label.render.add("no_life", assets["life_empty"])
            label.render.add("life", assets["life_gray"])
            label.render.state = "life"
            self._lives.append(label)

    @property
    def audio(self):
        return self._audio

    @audio.setter
    def audio(self, value):
        if value > 3:
            self._audio.state = "healthy"
        elif value > 1:
            self._audio.state = "injured"
        elif value == 1:
            self._audio.state = "danger"


class CoopUIMenu(BaseMenu):
    """
    The mutliplayer UI in a scene.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.x1 = 50
        self.y1 = 50
        self.x2 = 50
        self.y2 = 85
        self.spacing = 30

        self.p1Text = TextLabel("P1",
                                30,
                                "orange",
                                self.x1 - 35,
                                self.y1 + 4,
                                self.screen)
        self.p2Text = TextLabel("P2",
                                30,
                                "navy_blue",
                                self.x2 - 35,
                                self.y2 + 4,
                                self.screen)

        self._p1HP = None
        self._p1MaxHP = None
        self._p1Lives = []
        self._p2HP = None
        self._p2MaxHP = None
        self._p2Lives = []

        self._audio = AudioComponent(self, enableAutoPlay=False, enableRepeat=True)
        self._audio.add("healthy", SFX_RESOURCES["menu_heartbeat_healthy"])
        self._audio.add("injured", SFX_RESOURCES["menu_heartbeat_injured"])
        self._audio.add("danger", SFX_RESOURCES["menu_heartbeat_danger"])

    def __str__(self):
        return "coop_ui_menu"

    def handleEvent(self, event):
        if event.type == self.MENU_EVENT:
            if event.category == "max_health":
                p1HP, p2HP = event.data
                self.p1MaxHP = p1HP
                self.p2MaxHP = p2HP

            if event.category == "health":
                p1HP, p2HP = event.data
                self.p1HP = p1HP
                self.p2HP = p2HP
                self.audio = min(p1HP, p2HP)

    def update(self):
        self.audio.update()
        [l.render.update() for l in self._p1Lives]
        [l.render.update() for l in self._p2Lives]
        self.p1Text.update()
        self.p2Text.update()

    def draw(self, camera=None):
        [l.render.draw(camera) for l in self._p1Lives]
        [l.render.draw(camera) for l in self._p2Lives]
        self.p1Text.draw()
        self.p2Text.draw()

    @property
    def p1HP(self):
        return self._p1HP

    @p1HP.setter
    def p1HP(self, value):
        for heart in self._p1Lives:
            heart.render.state = "no_life"
        for i in range(value):
            self._p1Lives[i].render.state = "life"

    @property
    def p1MaxHP(self):
        return self._p1MaxHP

    @p1MaxHP.setter
    def p1MaxHP(self, value):
        assets = MENU_RESOURCES["assets"]
        for i in range(value):
            label = ImageLabel(None, self.x1+i*self.spacing, self.y1, self.screen)
            label.render.add("no_life", assets["life_empty"])
            label.render.add("life", assets["life_orange"])
            label.render.state = "life"
            self._p1Lives.append(label)

    @property
    def p2HP(self):
        return self._p2HP

    @p2HP.setter
    def p2HP(self, value):
        for heart in self._p2Lives:
            heart.render.state = "no_life"
        for i in range(value):
            self._p2Lives[i].render.state = "life"

    @property
    def p2MaxHP(self):
        return self._p2MaxHP

    @p2MaxHP.setter
    def p2MaxHP(self, value):
        assets = MENU_RESOURCES["assets"]
        for i in range(value):
            label = ImageLabel(None, self.x2+i*self.spacing, self.y2, self.screen)
            label.render.add("no_life", assets["life_empty"])
            label.render.add("life", assets["life_blue"])
            label.render.state = "life"
            self._p2Lives.append(label)

    @property
    def audio(self):
        return self._audio

    @audio.setter
    def audio(self, value):
        if value > 3:
            self._audio.state = "healthy"
        elif value > 1:
            self._audio.state = "injured"
        elif value == 1:
            self._audio.state = "danger"


class _SettingsLabel(GameObject):
    """
    Represents an option that the user can change.
    """

    def __init__(self, settingName, settingChoices, size, colour, x, y,
                 spacing, screen):
        """
        :param settingName: String, the name of the setting.
        :param settingChoices: List, containing string options choices.
        :param size: Integer, the size of the font.
        :param colour: 3-Tuple, containing the RGB values of the colour.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param spacing: Integer, the gap between the setting name and choice.
        :param screen: pygame.Surface, representing the screen.
        """
        self.rect = pg.Rect(x, y, 0, 0)
        self.screen = screen

        self.index = 0
        self.optionChosen = None
        self.name = TextLabel(settingName, size, colour, x, y, self.screen)

        self.options = [
            TextLabel(choice, size, colour, x + spacing, y, self.screen)
            for choice in settingChoices
        ]

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("switch", SFX_RESOURCES["menu_option_switch"])
        self.audio.state = "switch"

    def __str__(self):
        return "settings_label"

    def update(self):
        self.name.update()
        self.optionChosen = self.options[self.index]
        self.optionChosen.update()

    def draw(self, camera=None):
        self.audio.update()
        self.name.draw()
        self.optionChosen.draw()

    def next(self):
        """
        Increments the selected option to the next option.
        """
        self.audio.state = "switch"
        self.index += 1

        if self.index > len(self.options)-1:
            self.index = 0

    def previous(self):
        """
        Decrements the selected option to the previous option.
        """
        self.audio.state = "switch"
        self.index -= 1

        if self.index < 0:
            self.index = len(self.options)-1


class _Arrow(GameObject):
    """
    An arrow that highlights the option that the user is hovering over.
    """

    def __init__(self, x, y, dx, dy, totalOptions, screen):
        """
        :param x: Integer, the x-position of the arrow.
        :param y: Integer, the y-position of the arrow.
        :param dx: Integer, the change in x-position per movement.
        :param dy: Integer, the change in y-position per moevement.
        :param totalOptions: Integer, the total number of options.
        :param screen: pygame.Surface, representing the screen.
        """
        self.rect = pg.Rect(x, y, 0, 0)
        self.dx = dx
        self.dy = dy
        self.totalOptions = totalOptions
        self.screen = screen
        self.index = 0

        self.render = RenderComponent(self)
        self.render.add("spin", MENU_RESOURCES["assets"]["coin"], 350)
        self.render.state = "spin"

        self.audio = AudioComponent(self, enableAutoPlay=False)
        self.audio.add("move", SFX_RESOURCES["menu_arrow"])
        self.audio.state = "move"

    def __str__(self):
        return "arrow"

    def update(self):
        self.render.update()
        self.audio.update()

    def draw(self, camera=None):
        self.render.draw(camera)

    def moveUp(self):
        """
        Moves the arrow to the previous option number.
        """
        self.audio.state = "move"
        self.index -= 1
        self.rect.y -= self.dy

        if self.index < 0:
            self.rect.y += self.totalOptions * self.dy
            self.index = (self.totalOptions-1)

    def moveDown(self):
        """
        Moves the arrow to the next option number.
        """
        self.audio.state = "move"
        self.index += 1
        self.rect.y += self.dy

        if self.index > self.totalOptions-1:
            self.rect.y -= self.totalOptions * self.dy
            self.index = 0

