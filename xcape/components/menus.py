"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.render as render
import xcape.common.settings as settings
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent


class IMenu(GameObject):
    """
    A base menu for any menus that the user can interact with.
    """

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        self.screen = screen
        self.resources = resources
        self.rect = pg.Rect(0, 0, 0, 0)
        self.background = None

    def handleEvent(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class BlankMenu(IMenu):
    """
    A blank menu that does nothing except display a blank screen.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)


class SplashMenu(IMenu):
    """
    The splash screen of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)

        background = self.resources["screens"]["splash.jpg"]
        background = render.addBackground(background)
        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", background)

        self.effect = FadeEffect(screen, resources)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("splash_menu", "transition", "main_menu")

    def update(self):
        if self.effect.isComplete:
            events.messageMenu("splash_menu", "transition", "main_menu")
        else:
            self.animation.update()
            self.effect.update()

    def draw(self):
        self.animation.draw()
        self.effect.draw()


class MainMenu(IMenu):
    """
    The main menu of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", self.resources["screens"]["main.jpg"])

        self.totalOptions = 4
        self.fontSize = 22
        self.fontColour = settings.COLOURS["white"]
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
        self.title = ImageLabel(self.resources["assets"]["title.png"],
                                60,
                                55,
                                self.screen)
        self.arrow = Arrow(self.x-40,
                           self.y+28,
                           self.dx,
                           self.dy,
                           self.totalOptions,
                           self.screen,
                           self.resources)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                self.arrow.moveUp()
            if event.key == pg.K_DOWN:
                self.arrow.moveDown()

            if event.key == pg.K_RETURN:
                if self.arrow.optionNum == 1:
                    pass
                if self.arrow.optionNum == 2:
                    pass
                if self.arrow.optionNum == 3:
                    events.messageMenu("main_menu", "transition", "options_menu")
                if self.arrow.optionNum == 4:
                    quit()

    def update(self):
        self.animation.update()
        self.title.update()
        self.option1.update()
        self.option2.update()
        self.option3.update()
        self.option4.update()
        self.arrow.update()

    def draw(self):
        self.animation.draw()
        self.title.draw()
        self.option1.draw()
        self.option2.draw()
        self.option3.draw()
        self.option4.draw()
        self.arrow.draw()


class OptionsMenu(IMenu):
    """
    The options menu of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", self.resources["screens"]["options.jpg"])

        self.totalOptions = 2
        self.fontSize = 22
        self.fontColour = settings.COLOURS["white"]
        self.x = 230
        self.y = 155
        self.dx = 0
        self.dy = 50

        self.option1 = TextLabel("Background: Flip Vertically",
                                 self.fontSize,
                                 self.fontColour,
                                 self.x,
                                 self.y + 1 * self.dy,
                                 self.screen)
        self.option2 = TextLabel("Background: Flip Horizontally",
                                 self.fontSize,
                                 self.fontColour,
                                 self.x,
                                 self.y + 2 * self.dy,
                                 self.screen)
        self.arrow = Arrow(self.x-40,
                           self.y+40,
                           self.dx,
                           self.dy,
                           self.totalOptions,
                           self.screen,
                           self.resources)
        self.escapeImage = ImageLabel(self.resources["assets"]["esc.png"],
                                      25,
                                      440,
                                      self.screen)
        self.escapeText = TextLabel("Esc para volver",
                                    14,
                                    self.fontColour,
                                    50,
                                    445,
                                    self.screen)

        self.effect = FadeEffect(self.screen, self.resources)
        self.effectDuration = (self.effect.timeEndDarken -
                               self.effect.timeStartDarken)
        self.effect.timeStartDarken = float('inf')
        self.effect.timeEndDarken = float('inf')

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                self.effect.timeStartDarken = self.effect.time
                self.effect.timeEndDarken = (self.effect.time +
                                             self.effectDuration)

            if event.key == pg.K_UP:
                self.arrow.moveUp()
            if event.key == pg.K_DOWN:
                self.arrow.moveDown()

            if event.key == pg.K_RETURN:
                if self.arrow.optionNum == 1:
                    self.animation.flip(True, False)
                if self.arrow.optionNum == 2:
                    self.animation.flip(False, True)

    def update(self):
        self.animation.update()
        self.escapeImage.update()
        self.escapeText.update()
        self.option1.update()
        self.option2.update()
        self.arrow.update()
        self.effect.update()

        if self.effect.isComplete:
            events.messageMenu("options_menu", "transition", "main_menu")

    def draw(self):
        self.animation.draw()
        self.escapeImage.draw()
        self.escapeText.draw()
        self.option1.draw()
        self.option2.draw()
        self.arrow.draw()
        self.effect.draw()


class GameOverMenu(IMenu):
    """
    The game over menu of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle",
                                 self.resources["screens"]["game_over.png"])

        self.fontSize = 18
        self.fontColour = settings.COLOURS["white"]
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
                events.messageScene("game_over_menu", "transition", "blank_scene")

    def update(self):
        self.animation.update()
        self.enterText.update()

    def draw(self):
        self.animation.draw()
        self.enterText.draw()


class PauseMenu(IMenu):
    """
    The pause menu of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle",
                                 self.resources["screens"]["fade.png"])

        self.fontSize = 40
        self.fontColour = settings.COLOURS["white"]
        self.x = 270
        self.y = 225

        self.pauseText = TextLabel("Pause",
                                   self.fontSize,
                                   self.fontColour,
                                   self.x,
                                   self.y,
                                   self.screen)

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                events.messageMenu("pause_menu", "transition", "blank_menu")

    def update(self):
        self.animation.update()
        self.pauseText.update()

    def draw(self):
        self.animation.draw()
        self.pauseText.draw()


class FadeEffect(IMenu):
    """
    Responsible for applying a transitioning fade of as follows:

    Black screen --> Normal screen --> Black screen
    """

    def __init__(self, screen, resources):
        self.screen = screen
        self.resources = resources
        self.rect = pg.Rect(0, 0, 0, 0)
        self.transparentValue = 255
        self.isComplete = False

        background = pg.Surface((settings.WIDTH, settings.HEIGHT))
        background = background.convert()
        background.fill(settings.COLOURS["black"])
        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", background)

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

            self.animation.update()

    def draw(self):
        self.animation.draw()

    def lightenScreen(self):
        """
        Increases the transparency of the background.
        """
        current = self.time - self.timeStartLighten
        duration = self.timeEndLighten - self.timeStartLighten
        percentComplete = current/duration
        self.transparentValue = (1-percentComplete) * 255
        self.animation.image.set_alpha(self.transparentValue)

    def darkenScreen(self):
        """
        Reduces the transparency of the background.
        """
        current = self.time - self.timeStartDarken
        duration = self.timeEndDarken - self.timeStartDarken
        percentComplete = current/duration
        self.transparentValue = percentComplete * 255
        self.animation.image.set_alpha(self.transparentValue)


class TextLabel(GameObject):
    """
    Represents text that can be drawn on screen.
    """

    def __init__(self, text, size, colour, x, y, screen, font="m04fatalfuryblack"):
        """
        :param text: String, the text to render.
        :param size: Integer, the size of the font.
        :param colour: 3-Tuple, containing the RGB values of the colour.
        :param x: Integer, the x-position of the text.
        :param y: Integer, the y-position of the text.
        :param screen: pygame.Surface, representing the screen.
        :param font: String, the name of the font to use.
        """
        self.rect = pg.Rect(x, y, 0, 0)
        self.screen = screen

        font = pg.font.SysFont(font, size)
        image = font.render(text, True, colour)

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", image)

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()


class ImageLabel(GameObject):
    """
    Represents text that can be drawn on screen.
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

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", image)

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()


class Arrow(GameObject):
    """
    An arrow that highlights the option that the user is hovering over.
    """

    def __init__(self, x, y, dx, dy, totalOptions, screen, resources):
        """
        :param x: Integer, the x-position of the arrow.
        :param y: Integer, the y-position of the arrow.
        :param dx: Integer, the change in x-position per movement.
        :param dy: Integer, the change in y-position per moevement.
        :param totalOptions: Integer, the total number of options.
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        self.rect = pg.Rect(x, y, 0, 0)
        self.dx = dx
        self.dy = dy
        self.totalOptions = totalOptions
        self.screen = screen
        self.optionNum = 1

        self.state = "idle"
        self.animation = AnimationComponent(self)
        self.animation.addDynamic("idle", resources["assets"]["coin"], 350)

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()

    def moveUp(self):
        """
        Moves the arrow to the previous option number.
        """
        self.optionNum -= 1
        self.rect.y -= self.dy

        if self.optionNum < 1:
            self.rect.y += self.totalOptions * self.dy
            self.optionNum = self.totalOptions

    def moveDown(self):
        """
        Moves the arrow to the next option number.
        """
        self.optionNum += 1
        self.rect.y += self.dy

        if self.optionNum > self.totalOptions:
            self.rect.y -= self.totalOptions * self.dy
            self.optionNum = 1