"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.render as render
import xcape.common.settings as settings
from xcape.common.loader import menuResources
from xcape.common.object import GameObject
from xcape.common.render import TextLabel, ImageLabel
from xcape.components.animation import AnimationComponent


class BaseMenu(GameObject):
    """
    The base menu for any menu.
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


class SplashMenu(BaseMenu):
    """
    The splash screen of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        background = menuResources["screens"]["splash.png"]
        background = render.addBackground(background)
        self.image = background
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.effect = FadeEffect(screen)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("splash_menu", "transition", "main_menu")

    def update(self):
        if self.effect.isComplete:
            events.messageMenu("splash_menu", "transition", "main_menu")
        else:
            self.screen.blit(self.image, self.rect)
            self.effect.update()

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.effect.draw()


class MainMenu(BaseMenu):
    """
    The main menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.image = menuResources["screens"]["main.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

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
        self.title = ImageLabel(60,
                                55,
                                menuResources["assets"]["title.png"],
                                self.screen)
        self.arrow = _Arrow(self.x - 40,
                            self.y + 28,
                            self.dx,
                            self.dy,
                            self.totalOptions,
                            self.screen)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                self.arrow.moveUp()
            if event.key == pg.K_DOWN:
                self.arrow.moveDown()

            if event.key == pg.K_RETURN:
                if self.arrow.index == 0:
                    events.messageMenu("main_menu", "transition", "blank_menu")
                    events.messageCutScene("main_menu", "transition", "office_cutscene")
                if self.arrow.index == 1:
                    pass
                if self.arrow.index == 2:
                    events.messageMenu("main_menu", "transition", "options_menu")
                if self.arrow.index == 3:
                    quit()

    def update(self):
        self.title.update()
        self.arrow.update()

    def draw(self):
        self.screen.blit(self.image, self.rect)
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

        self.image = menuResources["screens"]["options.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        fontSize = 22
        fontColour = "white"
        x, y = 230, 155
        dx, dy = 0, 50

        self.arrow = _Arrow(x - 40, y - 10,
                            dx, dy,
                            2,
                            screen)

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

        self.escapeImage = ImageLabel(25, 440,
                                      menuResources["assets"]["esc.png"],
                                      screen)
        self.escapeText = TextLabel("Esc para volver",
                                    14, fontColour,
                                    50, 445,
                                    screen)

        self.effect = FadeEffect(self.screen)
        self.dt = self.effect.timeEndDarken - self.effect.timeStartDarken
        self.effect.timeStartDarken = float('inf')
        self.effect.timeEndDarken = float('inf')

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                self.effect.timeStartDarken = self.effect.time
                self.effect.timeEndDarken = self.effect.time + self.dt

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
                        self.image = pg.transform.flip(self.image, True, False)
                    if self.backgroundSetting.index == 1:
                        self.image = pg.transform.flip(self.image, False, True)

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

                    events.messageMenu("options_menu", "screen")
                    events.messageScene("options_menu", "screen")
                    events.messageCutScene("options_menu", "screen")


    def update(self):
        self.backgroundSetting.update()
        self.fullscreenSetting.update()
        self.arrow.update()
        self.escapeImage.update()
        self.effect.update()

        if self.effect.isComplete:
            events.messageMenu("options_menu", "transition", "main_menu")

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.backgroundSetting.draw()
        self.fullscreenSetting.draw()
        self.arrow.draw()
        self.escapeImage.draw()
        self.escapeText.draw()
        self.effect.draw()


class GameOverMenu(BaseMenu):
    """
    The game over menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.image = menuResources["screens"]["game_over.png"]
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


class WinMenu(BaseMenu):
    """
    The win menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)

        self.image = menuResources["screens"]["fade.png"]
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


class PauseMenu(BaseMenu):
    """
    The pause menu of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.image = menuResources["screens"]["fade.png"]
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
        self.image = background
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        # Units are in seconds (use floats to reduce rounding errors)
        self.origin = pg.time.get_ticks()/1000
        self.time = 0.0
        self.timeStartLighten = 1.0
        self.timeEndLighten = 3.0
        self.timeStartDarken = 4.0
        self.timeEndDarken = 6.0

    def update(self):
        if not self.isComplete:
            self.time = pg.time.get_ticks()/1000 - self.origin

            if self.timeEndLighten >= self.time >= self.timeStartLighten:
                self.lightenScreen()
            if self.timeEndDarken >= self.time >= self.timeStartDarken:
                self.darkenScreen()

            if self.time > self.timeEndDarken:
                self.isComplete = True

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def lightenScreen(self):
        """
        Increases the transparency of the background.
        """
        current = self.time - self.timeStartLighten
        duration = self.timeEndLighten - self.timeStartLighten
        percentComplete = current/duration
        self.transparentValue = (1-percentComplete) * 255
        self.image.set_alpha(self.transparentValue)

    def darkenScreen(self):
        """
        Reduces the transparency of the background.
        """
        current = self.time - self.timeStartDarken
        duration = self.timeEndDarken - self.timeStartDarken
        percentComplete = current/duration
        self.transparentValue = percentComplete * 255
        self.image.set_alpha(self.transparentValue)


class SoloUIMenu(BaseMenu):
    """
    The UI in a scene.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.x = 50
        self.y = 50
        self.dx = 30
        self.lives = []

    def handleEvent(self, event):
        if event.type == events.MENU_EVENT:
            if event.category == "health":
                currentHP = event.data

                if not self.lives:
                    self.setLives(currentHP)

                for heart in self.lives:
                    heart.state = "no_life"
                for heart in range(currentHP):
                    self.lives[heart].state = "life"

    def update(self):
        for live in self.lives:
            live.animation.update()

    def draw(self):
        for live in self.lives:
            live.animation.draw()

    def setLives(self, numLives):
        """
        Adds lives to the health bar.

        :param numLives: Integer, the number of lives.
        """
        assets = menuResources["assets"]
        for i in range(numLives):
            label = ImageLabel(self.x + i*self.dx, self.y, None, self.screen)
            label.state = "life"
            label.animation.add("no_life", [assets["no_life.png"]], float('inf'))
            label.animation.add("life", [assets["life.png"]], float('inf'))
            self.lives.append(label)


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
            for choice in settingChoices]

    def update(self):
        self.optionChosen = self.options[self.index]

    def draw(self):
        self.name.draw()
        self.optionChosen.draw()

    def next(self):
        """
        Increments the selected option to the next option.
        """
        self.index += 1

        if self.index > len(self.options)-1:
            self.index = 0

    def previous(self):
        """
        Decrements the selected option to the previous option.
        """
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

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.add("idle", menuResources["assets"]["coin"], 350)

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()

    def moveUp(self):
        """
        Moves the arrow to the previous option number.
        """
        self.index -= 1
        self.rect.y -= self.dy

        if self.index < 0:
            self.rect.y += self.totalOptions * self.dy
            self.index = (self.totalOptions-1)

    def moveDown(self):
        """
        Moves the arrow to the next option number.
        """
        self.index += 1
        self.rect.y += self.dy

        if self.index > self.totalOptions-1:
            self.rect.y -= self.totalOptions * self.dy
            self.index = 0
