"""
Contains all the menus in game.
"""

import pygame as pg
from xcape.common.gameobject import GameObject
import xcape.common.events as events
import xcape.common.renderer as renderer
import xcape.common.settings as settings


class IMenu(GameObject):
    """
    The interface for every menu.
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


class BlankMenu(IMenu):
    """
    A blank menu that does nothing other than display a blank (black) screen.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)


class SplashMenu(IMenu):
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


class FadeEffect(IMenu):
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




pass
# class Menu():
#     def __init__(self, game, player):
#         self.game = game
#         self.player = player
#         self.indent = 250
#         self.coin = Coin(155, self.indent, self.game)
#         self.fondo = load_image("background.jpg", img_folder, alpha=False)
#         self.title = load_image("title.png", img_folder, alpha = True)
#         self.font_color = WHITE
#         while True:
#             self.game.clock.tick(60)
#             self.menu_events()
#             self.menu_update()
#             self.coin.update()
#             pygame.display.update()
#
#     def menu_events(self):
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 quit()
#             if event.type == pygame.KEYDOWN:
#                 if event.key == K_UP:
#                     self.coin.posicion -= 38
#                 if event.key == K_DOWN:
#                     self.coin.posicion += 38
#                 if event.key == K_RETURN:
#                     if self.coin.posicion == 155:
#                         self.game.playing = True
#                         self.player.physics.velocity.x = 0
#                         self.player.stop()
#                         self.player.lives = 3
#                         self.game.lives = 3
#                         self.game.startGame()
#                     elif self.coin.posicion == 193:
#                         pass
#                     elif self.coin.posicion == 231:
#                         self.opciones = Opciones(self.game)
#                     elif self.coin.posicion == 269:
#                         pygame.quit()
#                         quit()
#             if event.type == pygame.KEYUP:
#                 if event.key == K_UP:
#                     self.coin.posicion += 0
#                 elif event.key == K_DOWN:
#                     self.coin.posicion -= 0
#
#             if self.coin.posicion > 269:
#                 self.coin.posicion = 155
#             elif self.coin.posicion < 155:
#                 self.coin.posicion = 269
#
#     def menu_update(self):
#         self.game.screen.blit(self.fondo, (0, 0))
#         self.game.screen.blit(self.title, (60, 55))
#         self.one_player = self.game.draw_text("1 Jugador", 22, self.font_color, self.indent, 160)
#         self.two_players = self.game.draw_text("2 Jugadores", 22, self.font_color, self.indent, 198)
#         self.options = self.game.draw_text("Opciones", 22, self.font_color, self.indent, 236)
#         self.exit = self.game.draw_text("Salir", 22, self.font_color, self.indent, 274)
#
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
# class Coin():
#     def __init__(self, posicion, indent, game):
#         self.coin = load_image("coin.png", img_folder, alpha = True)
#         self.game = game
#         self.cont_coin = 0
#         self.i_coin = 0
#         self.velocidad = 3
#         self.posicion = posicion
#         self.indent = indent
#         self.xixf_coin = {}
#         self.xixf_coin[0] = (0, 0, 32, 32)
#         self.xixf_coin[1] = (32, 0, 32, 32)
#         self.xixf_coin[2] = (64, 0, 32, 32)
#         self.xixf_coin[3] = (96, 0, 32, 32)
#         self.xixf_coin[4] = (128, 0, 32, 32)
#         self.xixf_coin[5] = (160, 0, 32, 32)
#
#     def update(self):
#         if self.cont_coin == self.velocidad:
#             self.i_coin = 0
#         elif self.cont_coin == self.velocidad*2:
#             self.i_coin = 1
#         elif self.cont_coin == self.velocidad*3:
#             self.i_coin = 2
#         elif self.cont_coin == self.velocidad*4:
#             self.i_coin = 3
#         elif self.cont_coin == self.velocidad*5:
#             self.i_coin = 4
#         elif self.cont_coin == self.velocidad*6:
#             self.i_coin = 5
#             self.cont_coin = 0
#
#         self.cont_coin += 1
#
#         self.game.screen.blit(self.coin, ((self.indent - 40), self.posicion), (self.xixf_coin[self.i_coin]))
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



    #
    # def draw_text(self, text, size, colour, x, y):
    #     """
    #     Draws text on the screen.
    #     """
    #     font = pg.font.SysFont(self.font_name, size)
    #     text_surface = font.render(text, True, colour)
    #     self.screen.blit(text_surface, (x, y))

