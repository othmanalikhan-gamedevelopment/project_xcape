"""
Contains all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.renderer as renderer
import xcape.common.settings as settings
from xcape.common.gameobject import GameObject


class StaticMenu(GameObject):
    """
    A base menu for any non-interactive menus.
    """

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        self.screen = screen
        self.resources = resources
        self.background = None

    def handleEvent(self, event):
        """
        :param event: pygame.Event, allowing event-driven programming.
        """
        pass

    def update(self):
        pass

    def draw(self):
        pass


class InteractiveMenu(GameObject):
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
        self.background = None

    def handleEvent(self, event):
        """
        :param event: pygame.Event, allowing event-driven programming.
        """
        pass

    def update(self):
        pass

    def draw(self):
        pass


class BlankMenu(StaticMenu):
    """
    A blank menu that does nothing other than display a blank (black) screen.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)


class SplashMenu(StaticMenu):
    """
    The splash screen of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.background = self.resources["screens"]["splash.jpg"]
        self.effect = FadeEffect(screen, resources)

    def handleEvent(self, event):
        if event.type == events.MENU_EVENT:
            if event.category == "transition":
                events.messageMenu("splash_menu", "transition", "main_menu")

    def update(self):
        if self.effect.isComplete:
            events.messageMenu("splash_menu", "transition", "main_menu")
        else:
            self.effect.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.effect.draw()


class MainMenu(InteractiveMenu):
    """
    The main menu of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.background = self.resources["screens"]["main.jpg"]
        self.title = self.resources["assets"]["title.png"]

        self.fontSize = 22
        self.fontColour = renderer.COLOURS["white"]
        self.x = 250
        self.y = 155
        self.dx = 0
        self.dy = 38

        self.totalOptions = 4
        self.arrow = Arrow(self.x-40, self.y+28, self.dx, self.dy,
                           self.totalOptions, self.screen, self.resources)

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
                    pass
                if self.arrow.optionNum == 4:
                    quit()

    def update(self):
        self.arrow.update()

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.title, (60, 55))
        self.drawOptions()
        self.arrow.draw()

    def drawOptions(self):
        """
        Draws the text of the options in the main menu.
        """
        renderer.drawText("1 Jugador", self.fontSize, self.fontColour,
                          self.x, self.y + 1*self.dy, self.screen)
        renderer.drawText("2 Jugadores", self.fontSize, self.fontColour,
                          self.x, self.y + 2*self.dy, self.screen)
        renderer.drawText("Opciones", self.fontSize, self.fontColour,
                          self.x, self.y + 3*self.dy, self.screen)
        renderer.drawText("Salir", self.fontSize, self.fontColour,
                          self.x, self.y + 4*self.dy, self.screen)


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
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.totalOptions = totalOptions
        self.screen = screen

        self.optionNum = 1
        self.image = resources["assets"]["coin"]

        self.cont_coin = 0
        self.i_coin = 1
        self.velocidad = 3


    def update(self):
        if self.cont_coin == self.velocidad:
            self.i_coin = 1
        elif self.cont_coin == self.velocidad*2:
            self.i_coin = 1
        elif self.cont_coin == self.velocidad*3:
            self.i_coin = 2
        elif self.cont_coin == self.velocidad*4:
            self.i_coin = 3
        elif self.cont_coin == self.velocidad*5:
            self.i_coin = 4
        elif self.cont_coin == self.velocidad*6:
            self.i_coin = 5
            self.cont_coin = 0

        self.cont_coin += 1

    def draw(self):
        self.screen.blit(self.image[self.i_coin], (self.x, self.y))

    def moveUp(self):
        """
        Moves the arrow to the previous option number.
        """
        self.optionNum -= 1
        self.y -= self.dy

        if self.optionNum < 1:
            self.y += self.totalOptions * self.dy
            self.optionNum = self.totalOptions

    def moveDown(self):
        """
        Moves the arrow to the next option number.
        """
        self.optionNum += 1
        self.y += self.dy

        if self.optionNum > self.totalOptions:
            self.y -= self.totalOptions * self.dy
            self.optionNum = 1









# class Opciones():
#     def __init__(self, game):
#         self.game = game
#         self.fondo = load_image("option.jpg", img_folder, alpha = False)
#         self.esc = load_image("esc.png", img_folder, alpha = True)
#         self.font_color = WHITE
#         self.fade = CrossFade(self.game.screen)
#         self.fade_list = pygame.sprite.Group(self.fade)
#         self.finished = False
#         while not self.finished:
#             self.game.clock.tick(60)
#             self.opciones_events()
#             self.opciones_update()
#
#     def opciones_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == K_ESCAPE:
#                     if self.fade.trans_value == 0:
#                         self.fade.fade_dir *= -1
#
#     def opciones_update(self):
#         if self.fade.trans_value == 258:
#             self.finished = True
#         self.game.screen.blit(self.fondo, (0, 0))
#         self.fade_list.clear(self.game.screen, self.fondo)
#         self.game.screen.blit(self.esc, (10, HEIGHT - 40))
#         self.back = self.game.draw_text("ESC para volver", 10, self.font_color, 35, HEIGHT - 35)
#         self.fade_list.update()
#         self.fade_list.draw(self.game.screen)
#         pygame.display.update()
#




    #
    # def showGameOverScreen(self):
    #     """
    #     Shows the game over screen.
    #     """
    #     #raise NotImplementedError("Game Over!")
    #
    #     self.gameover = False
    #     while not self.gameover:
    #         self.fondo = load_image("game_over.png", img_folder, alpha = True)
    #         self.image = pg.transform.scale(self.fondo, (640, 480))
    #         self.screen.blit(self.image, (0, 0))
    #         self.end = False
    #         while not self.end:
    #             for event in pg.event.get():
    #                 if event.type == pg.QUIT:
    #                     self.end = True
    #                     self.gameover = True
    #                     self.kill()
    #                 if event.type == pg.KEYDOWN:
    #                     if event.key == pg.K_RETURN:
    #                         self.end = True
    #                         self.gameover = True
    #                         self.playing = False
    #             self.text2 = self.draw_text("Enter para salir", 18, WHITE, 150, HEIGHT*2/3)
    #             pg.display.update()
    #
    #
    #
    # def drawPauseScreen(self):
    #     """
    #     Draws the pause screen.
    #     """
    #     fondo = load_image("black_fade.png", img_folder, alpha=True)
    #     image = pg.transform.scale(fondo, (640, 480))
    #     self.draw_text("Pause", 32, WHITE, WIDTH/2 - 70, HEIGHT/2)
    #     self.screen.blit(image, (0, 0))
    #




class FadeEffect(StaticMenu):
    """
    Responsible for applying a transitioning fade of as follows:

    Black screen --> Normal screen --> Black screen
    """

    def __init__(self, screen, resources):
        self.screen = screen
        self.resources = resources
        self.isComplete = False

        self.background = pg.Surface((settings.WIDTH, settings.HEIGHT))
        self.background = self.background.convert()
        self.background.fill(renderer.COLOURS["black"])
        self.transparentValue = 255

        # Units are in seconds (use floats to reduce rounding errors)
        self.origin = pg.time.get_ticks()/1000
        self.time = 0.0
        self.timeStartLighten = 1.0
        self.timeEndLighten = 3.0
        self.timeStartDarken = 4.0
        self.timeEndDarken = 6.0

    def update(self):
        if not self.isComplete:
            self.background.set_alpha(self.transparentValue)
            self.time = pg.time.get_ticks()/1000 - self.origin

            if self.timeEndDarken >= self.time >= self.timeStartDarken:
                self.darkenScreen()
            if self.timeEndLighten >= self.time >= self.timeStartLighten:
                self.lightenScreen()

            if self.time > self.timeEndDarken:
                self.isComplete = True

    def draw(self):
        self.screen.blit(self.background, (0, 0))

    def lightenScreen(self):
        """
        Increases the transparency of the background.
        """
        current = self.time - self.timeStartLighten
        duration = self.timeEndLighten - self.timeStartLighten
        percentComplete = current/duration
        self.transparentValue = (1-percentComplete) * 255

    def darkenScreen(self):
        """
        Reduces the transparency of the background.
        """
        current = self.time - self.timeStartDarken
        duration = self.timeEndDarken - self.timeStartDarken
        percentComplete = current/duration
        self.transparentValue = percentComplete * 255

