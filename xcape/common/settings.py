"""
Contains a list of basic game settings.
"""
import pygame as pg

WIDTH = 640
HEIGHT = 480
FPS = 60
TITLE = "Prison Xcape"

FONT = "m04.TFF"
# print(__file__)
# FONT = os.path.join("C:\\", "Oz", "3_projects", "1_programming", "1_active",
#                     "project_xcape", "prison_xcape", "fonts", "m04.TFF")
# FONT = "times new roman"
# print(pg.font.get_fonts())

COLOURS = {
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "black_red": (35, 21, 21),
    "cyan": (0, 255, 255),
    "gray": (27, 27, 27),
    "green": (0, 255, 0),
    "red": (255, 0, 0),
    "dark_red": (125, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
}

KEYBINDS_P1 = \
{
    "jump": pg.K_UP,
    "move_left": pg.K_LEFT,
    "move_right": pg.K_RIGHT,
}
KEYBINDS_P2 = \
{
    "jump": pg.K_w,
    "move_left": pg.K_a,
    "move_right": pg.K_d,
}
