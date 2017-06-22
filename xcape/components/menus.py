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
        self.animationState = "idle"

    def handleEvent(self, event):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def draw(self):
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

    def draw(self):
        self.render.draw()
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
        self.audio.state = "enter"

    def __str__(self):
        return "main_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                self.arrow.moveUp()
            if event.key == pg.K_DOWN:
                self.arrow.moveDown()

            if event.key == pg.K_RETURN:
                self.audio.play("enter")
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
        self.option1.update()
        self.option2.update()
        self.option3.update()
        self.option4.update()
        self.title.update()
        self.arrow.update()

    def draw(self):
        self.render.draw()
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
        self.audio.state = "exit"

    def __str__(self):
        return "options_menu"

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                self.effect.timeStartDarken = self.effect.time
                self.effect.timeEndDarken = self.effect.time + self.dt
                self.audio.play("exit")

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
        self.backgroundSetting.update()
        self.fullscreenSetting.update()
        self.escapeImage.update()
        self.escapeText.update()
        self.arrow.update()
        self.effect.update()

        if self.effect.isComplete:
            self.messageMenu("transition", "main_menu")

    def draw(self):
        self.render.draw()
        self.backgroundSetting.draw()
        self.fullscreenSetting.draw()
        self.escapeImage.draw()
        self.escapeText.draw()
        self.arrow.draw()
        self.effect.draw()


# TODO: Refactor
class DeathMenu(BaseMenu):
    """
    The death screen of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        background = pg.Surface((settings.WIDTH, settings.HEIGHT))
        background.fill(settings.COLOURS["dark_red"])
        background = background.convert()
        self.image = background
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.effect = FadeEffect(screen)
        self.effect.timeStartLighten = 0.0
        self.effect.timeEndLighten = 0.5
        self.effect.timeStartDarken = 0.5
        self.effect.timeEndDarken = 1.0

    def update(self):
        if self.effect.isComplete:
            events.messageScene("death_menu", "complete")
        else:
            self.screen.blit(self.image, self.rect)
            self.effect.update()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.effect.draw()


# TODO: Refactor
class GameOverMenu(BaseMenu):
    """
    The game over menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.image = MENU_RESOURCES["screens"]["game_over.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

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

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("game_over_menu", "transition", "splash_menu")
                events.messageScene("game_over_menu", "no_mode")

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.enterText.draw()


# TODO: Refactor
class WinMenu(BaseMenu):
    """
    The win menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.image = MENU_RESOURCES["screens"]["fade.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

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

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("game_over_menu", "transition", "main_menu")
                events.messageScene("game_over_menu", "no_mode")

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.enterText.draw()


# TODO: Refactor
class PauseMenu(BaseMenu):
    """
    The pause menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.image = MENU_RESOURCES["screens"]["fade.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.fontSize = 40
        self.fontColour = "white"
        self.x = 270
        self.y = 225

        self.pauseText = TextLabel("Pause",
                                   self.fontSize,
                                   self.fontColour,
                                   self.x,
                                   self.y,
                                   self.screen,
                                   isItalic=True)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("pause_menu", "transition", "blank_menu")

    def update(self):
        self.screen.blit(self.image, self.rect)

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.pauseText.draw()


class FadeEffect(BaseMenu):
    """
    Responsible for applying a transitioning fade of as follows:

    Black screen --> Normal screen --> Black screen
    """

    def __init__(self, screen):
        self.screen = screen
        self.rect = pg.Rect(0, 0, 0, 0)
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

    def draw(self):
        self.render.draw()

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


# TODO: Refactor
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
        self.lives = []

    def __str__(self):
        return "solo_ui_menu"

    def handleEvent(self, event):
        if event.type == self.MENU_EVENT:
            if event.category == "max_health":
                maxHP = event.data
                self.setMaxLives(maxHP)

            if event.category == "health":
                currentHP = event.data
                for heart in self.lives:
                    heart.state = "no_life"
                for heart in range(currentHP):
                    self.lives[heart].state = "life"

    def update(self):
        for live in self.lives:
            live.render.update()

    def draw(self):
        for live in self.lives:
            live.render.draw()

    def setMaxLives(self, numLives):
        """
        Sets the maximum number of hearts on the health bar.

        :param numLives: Integer, the number of lives.
        """
        assets = MENU_RESOURCES["assets"]
        for i in range(numLives):
            label = ImageLabel(None, self.x + i*self.dx, self.y, self.screen)
            label.render.add("no_life", assets["life_empty"])
            label.render.add("life", assets["life_gray"])
            label.render.state = "life"
            self.lives.append(label)


# TODO: Refactor
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

        self.livesP1 = []
        self.livesP2 = []

    def handleEvent(self, event):
        if event.type == self.MENU_EVENT:
            if event.category == "max_health":
                p1HP, p2HP = event.data
                self.setMaxLives(p1HP, p2HP)

            if event.category == "health":
                p1HP, p2HP = event.data

                for heart in self.livesP1:
                    heart.state = "no_life"
                for i in range(p1HP):
                    self.livesP1[i].state = "life"

                for heart in self.livesP2:
                    heart.state = "no_life"
                for i in range(p2HP):
                    self.livesP2[i].state = "life"

    def update(self):
        [l.animation.update() for l in self.livesP1]
        [l.animation.update() for l in self.livesP2]

    def draw(self):
        [l.animation.draw() for l in self.livesP1]
        [l.animation.draw() for l in self.livesP2]

        self.p1Text.draw()
        self.p2Text.draw()

    def setMaxLives(self, livesP1, livesP2):
        """
        Sets the maximum number of hearts on the health bar.

        :param livesP1: Integer, the max number of lives for player 1.
        :param livesP2: Integer, the max number of lives for player 2.
        """
        assets = MENU_RESOURCES["assets"]

        for i in range(livesP1):
            label = ImageLabel(self.x1 + i*self.spacing, self.y1,
                               None, self.screen)
            label.state = "life"
            label.render.add("no_life",
                             [assets["life_empty.png"]],
                             float('inf'))
            label.render.add("life",
                             [assets["life_orange.png"]],
                             float('inf'))
            self.livesP1.append(label)

        for i in range(livesP2):
            label = ImageLabel(self.x2 + i*self.spacing, self.y2,
                               None, self.screen)
            label.state = "life"
            label.render.add("no_life",
                             [assets["life_empty.png"]],
                             float('inf'))
            label.render.add("life",
                             [assets["life_blue.png"]],
                             float('inf'))
            self.livesP2.append(label)


#TODO: Complete
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

    def draw(self):
        self.name.draw()
        self.optionChosen.draw()

    def next(self):
        """
        Increments the selected option to the next option.
        """
        self.audio.play("switch")
        self.index += 1

        if self.index > len(self.options)-1:
            self.index = 0

    def previous(self):
        """
        Decrements the selected option to the previous option.
        """
        self.audio.play("switch")
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

    def draw(self):
        self.render.draw()

    def moveUp(self):
        """
        Moves the arrow to the previous option number.
        """
        self.audio.play("move")
        self.index -= 1
        self.rect.y -= self.dy

        if self.index < 0:
            self.rect.y += self.totalOptions * self.dy
            self.index = (self.totalOptions-1)

    def moveDown(self):
        """
        Moves the arrow to the next option number.
        """
        self.audio.play("move")
        self.index += 1
        self.rect.y += self.dy

        if self.index > self.totalOptions-1:
            self.rect.y -= self.totalOptions * self.dy
            self.index = 0

