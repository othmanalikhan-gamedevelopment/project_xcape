# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 23:42:57 2017
@author: Gustavo León Sazo
"""
import pygame
from pygame.locals import *
from settings import*
from player import*

img_folder = "imagenes"

class Start:
    def __init__(self, game):
        self.game = game
        self.sponsor = load_image("raspberry.jpg", img_folder, alpha = False)
        self.game.screen.blit(self.sponsor, (0, 0))
        self.fade = CrossFade(self.game.screen)
        self.fade_list = pygame.sprite.Group(self.fade)
        self.done = False
        while not self.done:
            self.game.clock.tick(60) 
            self.start_events()
            self.update()
            
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
                
    def update(self):
        if self.fade.trans_value == 0:
            pygame.time.delay(3000)
            self.fade.fade_dir *= -1
        if self.fade.trans_value == 258:
            self.done = True
        self.fade_list.clear(self.game.screen, self.sponsor)
        self.fade_list.update()
        self.fade_list.draw(self.game.screen)
        pygame.display.update()


class Menu():
    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.indent = 250
        self.coin = Coin(155, self.indent, self.game)
        self.fondo = load_image("background.jpg", img_folder, alpha=False)
        self.title = load_image("title.png", img_folder, alpha = True)
        self.font_color = WHITE
        while True:
            self.game.clock.tick(60)
            self.menu_events()
            self.menu_update()
            self.coin.update()
            pygame.display.update()
            
    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_UP:
                    self.coin.posicion -= 38
                if event.key == K_DOWN:
                    self.coin.posicion += 38
                if event.key == K_RETURN:
                    if self.coin.posicion == 155:
                        self.game.playing = True
                        self.player.physics.velocity.x = 0
                        self.player.stop()
                        self.player.lives = 3
                        self.game.lives = 3
                        self.game.startGame()
                    elif self.coin.posicion == 193:
                        pass
                    elif self.coin.posicion == 231:
                        self.opciones = Opciones(self.game)
                    elif self.coin.posicion == 269:
                        pygame.quit()
                        quit()
            if event.type == pygame.KEYUP:
                if event.key == K_UP:
                    self.coin.posicion += 0
                elif event.key == K_DOWN:
                    self.coin.posicion -= 0
                    
            if self.coin.posicion > 269:
                self.coin.posicion = 155
            elif self.coin.posicion < 155:
                self.coin.posicion = 269
        
    def menu_update(self):
        self.game.screen.blit(self.fondo, (0, 0))
        self.game.screen.blit(self.title, (60, 55))
        self.one_player = self.game.draw_text("1 Jugador", 22, self.font_color, self.indent, 160)
        self.two_players = self.game.draw_text("2 Jugadores", 22, self.font_color, self.indent, 198)
        self.options = self.game.draw_text("Opciones", 22, self.font_color, self.indent, 236)
        self.exit = self.game.draw_text("Salir", 22, self.font_color, self.indent, 274)
        
class Opciones():
    def __init__(self, game):
        self.game = game
        self.fondo = load_image("option.jpg", img_folder, alpha = False)
        self.esc = load_image("esc.png", img_folder, alpha = True)
        self.font_color = WHITE
        self.fade = CrossFade(self.game.screen)
        self.fade_list = pygame.sprite.Group(self.fade)
        self.finished = False
        while not self.finished:
            self.game.clock.tick(60)
            self.opciones_events()
            self.opciones_update()
    
    def opciones_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.fade.trans_value == 0:
                        self.fade.fade_dir *= -1
        
    def opciones_update(self):
        if self.fade.trans_value == 258:
            self.finished = True
        self.game.screen.blit(self.fondo, (0, 0))
        self.fade_list.clear(self.game.screen, self.fondo)
        self.game.screen.blit(self.esc, (10, HEIGHT - 40))
        self.back = self.game.draw_text("ESC para volver", 10, self.font_color, 35, HEIGHT - 35)
        self.fade_list.update()
        self.fade_list.draw(self.game.screen)
        pygame.display.update()
    
class Coin():
    def __init__(self, posicion, indent, game):
        self.coin = load_image("coin.png", img_folder, alpha = True)
        self.game = game
        self.cont_coin = 0
        self.i_coin = 0
        self.velocidad = 3
        self.posicion = posicion
        self.indent = indent
        self.xixf_coin = {}
        self.xixf_coin[0] = (0, 0, 32, 32)
        self.xixf_coin[1] = (32, 0, 32, 32)
        self.xixf_coin[2] = (64, 0, 32, 32)
        self.xixf_coin[3] = (96, 0, 32, 32)
        self.xixf_coin[4] = (128, 0, 32, 32)
        self.xixf_coin[5] = (160, 0, 32, 32)
    
    def update(self):
        if self.cont_coin == self.velocidad:
            self.i_coin = 0
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

        self.game.screen.blit(self.coin, ((self.indent - 40), self.posicion), (self.xixf_coin[self.i_coin]))

class CrossFade(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(screen.get_size())
        self.image = self.image.convert()
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.fade_dir = 1
        self.trans_value = 255
        self.fade_speed = 6
        self.delay = 1
        self.increment = 0
        self.image.set_alpha(self.trans_value)
        self.rect.centerx = 320
        self.rect.centery = 240

    def update(self):
        self.image.set_alpha(self.trans_value)
        self.increment += 1

        if self.increment >= self.delay:
            self.increment = 0
            if self.fade_dir > 0:
                if self.trans_value - self.fade_speed < 0:
                    self.trans_value = 0
                else:
                    self.trans_value -= self.fade_speed

            elif self.fade_dir < 0:
                if self.trans_value + self.delay > 255:
                    self.trans_value = 255
                else:
                    self.trans_value += self.fade_speed