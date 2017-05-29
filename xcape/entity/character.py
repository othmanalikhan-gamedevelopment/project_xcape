# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from settings import *
from player import*

#=========PLATFORMS=========
BIG_PLAT_LEFT            = (0, 297, 60, 60)
BIG_PLAT_MIDDLE          = (88, 296, 64, 60)
BIG_PLAT_RIGHT           = (172, 296, 60, 60)

LITTLE_PLAT              = (236, 303, 64, 32)

JUMPING_PLAT_LEFT        = (53, 374, 24, 36)
JUMPING_PLAT_MIDDLE      = (88, 374, 59, 36)
JUMPING_PLAT_RIGHT       = (158, 374, 24, 36)

DOWN_CORNER_LEFT         = (0, 229, 80, 52)
UP_CORNER_LEFT           = (0, 193, 48, 28)
DOWN_CORNER_RIGHT        = (224, 228, 80, 53)
UP_CORNER_RIGHT          = (256, 188, 48, 32)

GROUND_MIDDLE_UP         = (118, 221, 64, 52)
GROUND_LEFTDOWN_CORNER   = (224, 188, 80, 85)
GROUND_LEFTUP_CORNER     = (80, 64, 68, 60)
GROUND_RIGHTUP_CORNER    = (164, 65, 60, 68)
GROUND_RIGHTDOWN_CORNER  = (0, 193, 80, 80)
WALL_RIGHT               = (256, 83, 48, 64)
RIGHT_INSIDEUP_CORNER    = (240, 0, 64, 60)
ROOF_MIDDLE              = (152, 0, 64, 52)
LEFT_INSIDEDOWN_CORNER   = (80, 133, 76, 60)
WALL_LEFT                = (0, 88, 48, 64)

MOVING_Y_PLAT            = (309, 439, 32, 40)
MOVING_X_PLAT            = (305, 396, 40, 36)

STANDING_TOP_PLAT        = (346, 37, 64, 64)
STANDING_MIDDLE_PLAT     = (346, 111, 64, 64)
STANDING_BOTTOM_PLAT     = (346, 188, 64, 60)

ONE_LITTLE_PLAT          = (304, 342, 89, 36)

#=============OBJECTS=============

DOOR_CLOSED              = (47, 423, 80, 108)
DOOR_OPENED              = (139, 423, 80, 108)

BUTTON_OFF               = (14, 378, 20, 28)
BUTTON_ON                = (14, 470, 20, 28)

GROUND_SPIKES            = (300, 509, 93, 24)
RIGHT_SPIKES             = (334, 292, 25, 45)
LEFT_SPIKES              = (380, 292, 25, 45)

SUPPORT_DOWN             = (240, 470, 48, 63)
SUPPORT_MIDDLE           = (240, 410, 48, 56)
SUPPORT_TOP              = (240, 341, 48, 63)

TOUCHING_SUPPORT_TOP     = (362, 384, 52, 22)
TOUCHING_SUPPORT_MIDDLE   = (362, 416, 52, 60)
TOUCHING_SUPPORT_BOTTOM  = (362, 486, 52, 19)




class GameObject(pygame.sprite.Sprite):
    """
    Represents an object in game.
    """

    def __init__(self, data):
        """
        A simple constructor.

        :param data: A list that contains the sprite sheet data,
        the x-position and y-position to deploy the object.
        """
        super().__init__()

        sprite_sheet_data, x, y = data
        sprite_sheet = SpriteSheet("spritesheet.png")
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.mask = pygame.mask.from_surface(self.image)

        
class MovingPlatform(GameObject):
    """
    Represents a moving platform in game.
    """

    def __init__(self, size, moveX, moveY,
                 boundVertical, boundHorizontal, level):
        """
        A simple constructor.
        """
        super().__init__(size)

        self.moveX = moveX
        self.moveY = moveY

        self.boundary_top = boundVertical[0]
        self.boundary_bottom = boundVertical[1]
        self.boundary_left = boundHorizontal[0]
        self.boundary_right = boundHorizontal[1]

        self.level = level

    def update(self):
        """
        Updating the moving platform to move in game.
        """
        self.rect.x += self.moveX
        self.rect.y += self.moveY

        cur_pos_x = self.rect.x - self.level.worldShiftX
        cur_pos_y = self.rect.y - self.level.worldShiftY

        if cur_pos_x < self.boundary_left or cur_pos_x > self.boundary_right:
            self.moveX *= -1
            
        if cur_pos_y > self.boundary_bottom or cur_pos_y < self.boundary_top:
            self.moveY *= -1


class TransparentPlatform(GameObject):
    """
    Represents a transparent platform in game.
    """

    def __init__(self, size):
        """
        A simple constructor.
        """
        super().__init__(size)

