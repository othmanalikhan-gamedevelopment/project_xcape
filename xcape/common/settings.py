"""
Contains a list of basic game settings.
"""
import pygame as pg

WIDTH = 640
HEIGHT = 480
FPS = 70
TITLE = "Prison Xcape"

# Defaults to pygame's default font which supports various
# non-English languages
FONT = None

COLOURS = {
    "black": (0, 0, 0),
    "navy_blue": (15, 82, 191),
    "blue": (0, 0, 255),
    "black_red": (35, 21, 21),
    "cyan": (0, 255, 255),
    "gray": (27, 27, 27),
    "green": (0, 255, 0),
    "orange": (191, 109, 15),
    "red": (255, 0, 0),
    "dark_red": (125, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "dark_blue": (15, 17, 49)
}

KEYBINDS_P1 = \
{
    "jump": pg.K_UP,
    "move_left": pg.K_LEFT,
    "move_right": pg.K_RIGHT,
    "coop_jump": pg.K_DOWN,
}
KEYBINDS_P2 = \
{
    "jump": pg.K_w,
    "move_left": pg.K_a,
    "move_right": pg.K_d,
    "coop_jump": pg.K_s,
}
