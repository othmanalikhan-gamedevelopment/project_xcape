# -*- coding: utf-8 -*-
"""
Created on Wed Apr 7 03:44:48 2017
@author: Gustavo León Sazo
"""
import pygame as pg

from collision import CollisionEngine
from settings import *
from player import*
from menu import*
from levels import*


class Game:
    """
    Responsible for running the game.
    """

    def __init__(self):
        """
        A simple constructor.
        """
        # Initialise pygame and mixer for music
        pg.init()
        pg.mixer.init()
        
        # Initialise screen and window
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.font_name = FONT_NAME

        # Initialises state variables
        self.clock = pg.time.Clock()
        self.running = True
        self.pause = False
        self.playing = True

        # Initialise playerOne
        self.playerOne = PlayerOne(self.screen)
        self.playerTwo = PlayerTwo(self.screen)
        self.spawn = None

        # Initialise level
        self.scenario = None
        self.level = 0
        self.collisionEngine1 = None
        self.collisionEngine2 = None

    def startGame(self):
        """
        Starts a new game.
        """
        #self.loadScenario01()
        #self.loadScenario02()
        self.loadScenario03()
        self.run()

    def loadScenario01(self):
        """
        Loads the first level of the game.
        """
        spawn = (70, 70)
        self.level = 1
        self.playerOne.rect.center = spawn
        self.scenario = Scenario01(self.screen, spawn)
        self.collisionEngine1 = CollisionEngine(self.playerOne, self.scenario)

    def loadScenario02(self):
        """
        Loads the second level of the game.
        """
        spawn = (70, 510)
        self.level = 2
        self.playerOne.rect.center = spawn
        self.scenario = Scenario02(self.screen, spawn)
        self.collisionEngine1 = CollisionEngine(self.playerOne, self.scenario)

    def loadScenario03(self):
        """
        Loads the third level of the game.
        """
        spawn = (315, 180)
        self.level = 3
        self.playerOne.rect.center = spawn
        self.playerTwo.rect.center = spawn
        self.scenario = Scenario03(self.screen, spawn)
        self.collisionEngine1 = CollisionEngine(self.playerOne, self.scenario)
        self.collisionEngine2 = CollisionEngine(self.playerTwo, self.scenario)

    def updateCameraX(self):
        """
        Updates the camera view in the x-axis.
        """
        maxCamera_x = int(WIDTH * 2 / 3)
        minCamera_x = int(WIDTH / 3)

        if self.playerOne.rect.right >= maxCamera_x:
            diff = maxCamera_x - self.playerOne.rect.right
            self.playerOne.rect.right = maxCamera_x
            self.scenario.shiftWorldX(diff)

        if self.playerOne.rect.left <= minCamera_x:
            diff = minCamera_x - self.playerOne.rect.left
            self.playerOne.rect.left = minCamera_x
            self.scenario.shiftWorldX(diff)

    def updateCameraY(self):
        """
        Updates the camera view in the y-axis.
        """
        maxCamera_y = int(HEIGHT * 2 / 3)
        minCamera_y = int(HEIGHT / 3)

        if self.playerOne.rect.top <= minCamera_y:
            diff = minCamera_y - self.playerOne.rect.top
            self.playerOne.rect.top = minCamera_y
            self.scenario.shiftWorldY(diff)

        if self.playerOne.rect.bottom >= maxCamera_y:
            diff = maxCamera_y - self.playerOne.rect.bottom
            self.playerOne.rect.bottom = maxCamera_y
            self.scenario.shiftWorldY(diff)

    def update(self):
        """
        Updates the game every frame.
        """
        if not self.pause:

            # Updates game state
            self.playerOne.update()
            self.playerTwo.update()
            self.scenario.update()
            self.collisionEngine1.update()
            self.collisionEngine2.update()

            # Updates camera
            self.updateCameraX()
            self.updateCameraY()

            # Changes level if complete
            if self.scenario.isEnd:
                self.level += 1
                if self.level == 2:
                    self.loadScenario02()
                if self.level == 3:
                    self.loadScenario03()

            # Restarts level upon being hit
            if self.playerOne.isHit:
                self.playerOne.lives -= 1
                self.playerOne.isHit = False
                if self.level == 2:
                    self.loadScenario02()
                if self.level == 3:
                    self.loadScenario03()

            # Ends game if playerOne loses
            if self.playerOne.lives == 0:
                print("game over")
                self.showGameOverScreen()
                #raise Exception("GAME OVER")

    def events(self):
        """
        Handles game events.
        """
        for event in pg.event.get():

            # Passes event to the event handler of playerOne
            self.collisionEngine1.eventHandler(event)
            self.collisionEngine2.eventHandler(event)
            self.playerOne.eventHandler(event)
            self.playerTwo.eventHandler(event)

            # Quits the game
            if event.type == pg.QUIT:
                self.kill()
                pygame.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.pause = not self.pause

                if event.key == pg.K_F4:
                    self.kill()
                    pygame.quit()
                    quit()

    def draw(self):
        """
        Draws all game objects on the screen.
        """
        self.scenario.draw()
        self.playerOne.draw()
        self.playerTwo.draw()

        #=====draws playerOne's lives on the screen=======
        self.showLives("no_life.png", 3)
        self.showLives("life.png", self.playerOne.lives)
        
        
        if self.pause:
            self.drawPauseScreen()

        pg.display.update()

    def drawPauseScreen(self):
        """
        Draws the pause screen.
        """
        fondo = load_image("black_fade.png", img_folder, alpha=True)
        image = pg.transform.scale(fondo, (640, 480))
        self.draw_text("Pause", 32, WHITE, WIDTH/2 - 70, HEIGHT/2)
        self.screen.blit(image, (0, 0))

    def run(self):
        """
        Runs the game loop.
        """
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def showStartScreen(self):
        """
        Shows the start screen of the game.
        """
        #Start(self)
        Menu(self, self.playerOne)

    def showGameOverScreen(self):
        """
        Shows the game over screen.
        """
        #raise NotImplementedError("Game Over!")
        
        self.gameover = False
        while not self.gameover:
            self.fondo = load_image("game_over.png", img_folder, alpha = True)
            self.image = pg.transform.scale(self.fondo, (640, 480))
            self.screen.blit(self.image, (0, 0))       
            self.end = False
            while not self.end:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.end = True
                        self.gameover = True
                        self.kill()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_RETURN:
                            self.end = True
                            self.gameover = True
                            self.playing = False
                self.text2 = self.draw_text("Enter para salir", 18, WHITE, 150, HEIGHT*2/3)
                pg.display.update()

    def draw_text(self, text, size, colour, x, y):
        """
        Draws text on the screen.
        """
        font = pg.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, colour)
        self.screen.blit(text_surface, (x, y))

    def kill(self):
        if self.playing:
            self.playing = False
        self.running = False
        
    def showLives(self, file_name, range_number):
        self.life_icon = load_image(file_name, img_folder, alpha=True)
        self.space = 25
        for x in range(range_number):
            self.screen.blit(self.life_icon, (self.space, 40))
            self.space += 25


def main():
    """
    Main method to run the game.
    """
    game = Game()
    game.showStartScreen()
    pg.quit()


if __name__ == "__main__":
    main()
