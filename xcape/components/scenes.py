"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.render as render
import xcape.common.settings as settings
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent


class IScene(GameObject):
    """
    The interface for a scene.
    """

    def __init__(self, screen, resources):
        """
        :param screen: pygame.Surface, representing the screen.
        :param resources: 2D Dictionary, mapping dir and file name to image.
        """
        self.screen = screen
        self.resources = resources
        self.rect = pg.Rect(0, 0, 0, 0)
        self.levelNum = 0
        self.spawnLocation = None
        self.isEnd = False
        self.state = "idle"

    def handleEvent(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass


class BlankScene(IScene):
    """
    A blank scene that does nothing except display a blank screen.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)


class SoloScene01(IScene):
    """
    The first scene of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.rect = pg.Rect(0, 0, 0, 0)
        # self.spawn = (70, 70)
        self.spawn = (70, 400)
        self.levelNum = 1

        background = self.resources["screens"]["scene_01.png"]
        background = render.addBackground(background, "black_red")
        self.animation = AnimationComponent(self)
        self.animation.addStatic("idle", background)

        self.player = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.buttons = pg.sprite.Group()
        self.enemies = pg.sprite.Group()

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            pass
            # if event.key == pg.K_RETURN:
            #     events.messageMenu("splash_menu", "transition", "main_menu")

    def update(self):
        self.animation.update()

    def draw(self):
        self.animation.draw()


    def x(self, screen, spawn):
        # Defining position of all sprites on the scenario (width, height, x, y)
        self.platStaticCoords = [[GROUND_MIDDLE_UP, 80, 478],
                           [GROUND_MIDDLE_UP, 144, 478],
                           [GROUND_MIDDLE_UP, 336, 478],
                           [GROUND_MIDDLE_UP, 400, 478],
                           [GROUND_MIDDLE_UP, 464, 478],
                           [GROUND_MIDDLE_UP, 528, 478],
                           [GROUND_RIGHTUP_CORNER, 304, 414],
                           [GROUND_LEFTUP_CORNER, 240, 414],
                           [DOWN_CORNER_LEFT, 0, 478],
                           [UP_CORNER_LEFT, 0, 450],
                           [DOWN_CORNER_RIGHT, 592, 478],
                           [UP_CORNER_RIGHT, 624, 446],
                           [UP_CORNER_RIGHT, 240, 446],
                           [DOWN_CORNER_RIGHT, 208, 478],
                           [UP_CORNER_LEFT, 316, 454],
                           [DOWN_CORNER_LEFT, 316, 478],
                           [WALL_RIGHT, 624, 382],
                           [WALL_RIGHT, 624, 318],
                           [WALL_RIGHT, 624, 254],
                           [WALL_RIGHT, 624, 190],
                           [RIGHT_INSIDEUP_CORNER, 608, 130],
                           [ROOF_MIDDLE, 544, 130],
                           [ROOF_MIDDLE, 480, 130],
                           [ROOF_MIDDLE, 416, 130],
                           [ROOF_MIDDLE, 352, 130],
                           [ROOF_MIDDLE, 288, 130],
                           [LEFT_INSIDEDOWN_CORNER, 212, 122],
                           [WALL_RIGHT, 212, 58],
                           [WALL_RIGHT, 212, 0],
                           [WALL_LEFT, 0, 386],
                           [WALL_LEFT, 0, 322],
                           [WALL_LEFT, 0, 258],
                           [WALL_LEFT, 0, 194],
                           [WALL_LEFT, 0, 130],
                           [WALL_LEFT, 0, 66],
                           [WALL_LEFT, 0, 2],
                           [BIG_PLAT_LEFT, 48, 422],
                           [BIG_PLAT_RIGHT, 76, 422],
                           [LITTLE_PLAT, 152, 446]]

                           #[JUMPING_PLAT_LEFT, 442, 332],
                           #[JUMPING_PLAT_LEFT, 258, 265],
                           #[JUMPING_PLAT_MIDDLE, 280, 265],
                           #[JUMPING_PLAT_MIDDLE, 462, 332],
                           #[JUMPING_PLAT_RIGHT, 520, 332],
                           #[JUMPING_PLAT_RIGHT, 339, 265]]

        self.doorClosedCoords = [[DOOR_CLOSED, 547, 374]]
        self.doorOpenedCoords = [[DOOR_OPENED, 547, 374]]

        self.buttonOffCoords = [[BUTTON_OFF, 300, 222]]
        self.buttonOnCoords = [[BUTTON_ON, 300, 222]]
        self.platTransparentCoords = [[JUMPING_PLAT_LEFT, 442, 332],
                                      [JUMPING_PLAT_LEFT, 258, 265],
                                      [JUMPING_PLAT_MIDDLE, 280, 265],
                                      [JUMPING_PLAT_MIDDLE, 462, 332],
                                      [JUMPING_PLAT_RIGHT, 520, 332],
                                      [JUMPING_PLAT_RIGHT, 339, 265]]








# class Scenario02(Scenario):
#     """
#     The second scenario of the game.
#     """
#
#     def __init__(self, screen, spawn):
#         """
#         A simple constructor.
#
#         :param screen: pygame.display Class, representing the user's screen.
#         :param spawn: Tuple, containing the x & y of players spawn location.
#         """
#         super().__init__(screen)
#         self.spawn = spawn
#         self.levelNum = 2
#         self.background = load_image("Scenario_2_level_1.jpg",
#                                      img_folder, alpha=True)
#
#         # Defining position of all sprites on the scenario (width, height, x, y)
#         self.platStaticCoords = [[GROUND_MIDDLE_UP, 48, 548],
#                                  [GROUND_MIDDLE_UP, 88, 548],
#                                  [GROUND_MIDDLE_UP, 152, 548],
#                                  [GROUND_MIDDLE_UP, 216, 548],
#                                  [GROUND_MIDDLE_UP, 280, 548],
#                                  [GROUND_MIDDLE_UP, 344, 548],
#                                  [GROUND_MIDDLE_UP, 408, 548],
#                                  [GROUND_MIDDLE_UP, 472, 548],
#                                  [GROUND_MIDDLE_UP, 536, 548],
#                                  [GROUND_MIDDLE_UP, 600, 548],
#                                  [GROUND_MIDDLE_UP, 664, 548],
#                                  [GROUND_MIDDLE_UP, 728, 548],
#                                  [GROUND_MIDDLE_UP, 792, 548],
#                                  [GROUND_MIDDLE_UP, 856, 548],
#
#                                  [DOWN_CORNER_LEFT, 0, 548],
#
#                                  [WALL_RIGHT, 952, 124],
#                                  [WALL_RIGHT, 952, 188],
#                                  [WALL_RIGHT, 952, 252],
#                                  [WALL_RIGHT, 952, 316],
#                                  [WALL_RIGHT, 952, 380],
#                                  [WALL_RIGHT, 952, 444],
#                                  [WALL_RIGHT, 952, 508],
#                                  [DOWN_CORNER_RIGHT, 920, 548],
#
#                                  [UP_CORNER_LEFT, 0, 520],
#                                  [WALL_LEFT, 0, 456],
#                                  [WALL_LEFT, 0, 392],
#                                  [WALL_LEFT, 0, 328],
#                                  [WALL_LEFT, 0, 264],
#                                  [WALL_LEFT, 0, 200],
#                                  [WALL_LEFT, 0, 136],
#                                  [WALL_LEFT, 0, 72],
#
#                                  #[ONE_LITTLE_PLAT, 188, 465],
#                                  #[ONE_LITTLE_PLAT, 718, 465],
#                                  #[ONE_LITTLE_PLAT, 53, 378],
#                                  #[ONE_LITTLE_PLAT, 834, 378],
#
#                                  [BIG_PLAT_RIGHT, 683, 297],
#                                  [BIG_PLAT_LEFT, 235, 297],
#                                  [BIG_PLAT_LEFT, 653, 297],
#                                  [BIG_PLAT_RIGHT, 265, 297],
#                                  [BIG_PLAT_RIGHT, 489, 489],
#                                  [BIG_PLAT_LEFT, 429, 489]]
#         self.platMovingCoords = [[MOVING_Y_PLAT, 360, 464],
#                                  [MOVING_Y_PLAT, 586, 464]]
#
#         self.platTransparentCoords = [[ONE_LITTLE_PLAT, 188, 465],
#                                       [ONE_LITTLE_PLAT, 718, 465],
#                                       [ONE_LITTLE_PLAT, 53, 378],
#                                       [ONE_LITTLE_PLAT, 834, 378]] #[[ONE_LITTLE_PLAT, 50, 280]]
#
#         self.enemyCoords = [[GROUND_SPIKES, 330, 524],
#                             [GROUND_SPIKES, 555, 524]]
#         self.doorOpenedCoords = [[DOOR_OPENED, 52, 441]]
#         self.doorClosedCoords = [[DOOR_CLOSED, 860, 441]]
#         self.doorOpenedCoords = [[DOOR_OPENED, 860, 441]]
#         self.buttonOffCoords = [[BUTTON_OFF, 480, 436]]
#         self.buttonOnCoords = [[BUTTON_ON, 480, 436]]
#
#         # Adding all sprites to the scenario
#         self.addDoors()
#         self.addButtons()
#         self.addPlatforms()
#         self.addEnemies()
#
#         # Manually adding moving plats
#         platMove1 = MovingPlatform(self.platMovingCoords[0],
#                                    0, 2, (300, 475), (0, 0), self)
#         platMove2 = MovingPlatform(self.platMovingCoords[1],
#                                    0, 2, (300, 475), (0, 0), self)
#         self.platMoving.add(platMove1)
#         self.platMoving.add(platMove2)
#
#         # Manually adding transparent platforms
#         for plat in self.platTransparentCoords:
#             self.platTransparent.add(TransparentPlatform(plat))
#
#
# class Scenario03(Scenario):
#     """
#     The third scenario of the game.
#     """
#
#     def __init__(self, screen, spawn):
#         """
#         A simple constructor.
#
#         :param spawn: Tuple, containing the x & y of players spawn location.
#         :param spawn: Tuple, containing the x & y of players spawn location.
#         """
#         super().__init__(screen)
#         self.screen = screen
#         self.spawn = spawn
#         self.background = load_image("Scenario_3_level_1.png",
#                                      img_folder, alpha=True)
#
#         # Defining position of all sprites on the scenario (width, height, x, y)
#         self.platStaticCoords = [[BIG_PLAT_MIDDLE, 291, 182],
#                                [BIG_PLAT_MIDDLE, 859, 182],
#                                [BIG_PLAT_MIDDLE, 795, 182],
#                                [BIG_PLAT_MIDDLE, 227, 182],
#                                [BIG_PLAT_LEFT, 167, 182],
#                                [BIG_PLAT_RIGHT, 923, 182],
#
#                                [WALL_RIGHT, 1102, 444],
#                                [WALL_RIGHT, 1102, 380],
#                                [WALL_RIGHT, 1102, 316],
#                                [WALL_RIGHT, 1102, 252],
#                                [WALL_RIGHT, 1102, 188],
#                                [WALL_RIGHT, 1102, 124],
#                                [WALL_RIGHT, 1102, 60],
#                                [WALL_RIGHT, 507, 423],
#
#                                [WALL_LEFT, 0, 448],
#                                [WALL_LEFT, 0, 384],
#                                [WALL_LEFT, 0, 320],
#                                [WALL_LEFT, 0, 256],
#                                [WALL_LEFT, 0, 192],
#                                [WALL_LEFT, 0, 128],
#                                [WALL_LEFT, 0, 64],
#                                [WALL_LEFT, 587, 431],
#
#                                [ROOF_MIDDLE, 995, 0],
#                                [ROOF_MIDDLE, 931, 0],
#                                [ROOF_MIDDLE, 867, 0],
#                                [ROOF_MIDDLE, 803, 0],
#                                [ROOF_MIDDLE, 739, 0],
#                                [ROOF_MIDDLE, 355, 0],
#                                [ROOF_MIDDLE, 291, 0],
#                                [ROOF_MIDDLE, 227, 0],
#                                [ROOF_MIDDLE, 163, 0],
#                                [ROOF_MIDDLE, 99, 0],
#
#                                [STANDING_TOP_PLAT, 703, 423],
#                                [STANDING_TOP_PLAT, 375, 423],
#                                [STANDING_MIDDLE_PLAT, 703, 487],
#                                [STANDING_MIDDLE_PLAT, 375, 487],
#
#                                # [TOUCHING_SUPPORT_BOTTOM, 738, 164],
#                                # [TOUCHING_SUPPORT_BOTTOM, 363, 163],
#                                # [TOUCHING_SUPPORT_TOP, 738, 52],
#                                # [TOUCHING_SUPPORT_TOP, 363, 52],
#                                # [TOUCHING_SUPPORT_MIDDLE, 738, 74],
#                                # [TOUCHING_SUPPORT_MIDDLE, 738, 104],
#                                # [TOUCHING_SUPPORT_MIDDLE, 363, 70],
#                                # [TOUCHING_SUPPORT_MIDDLE, 363, 104],
#
#                                [GROUND_LEFTUP_CORNER, 507, 363],
#                                [GROUND_RIGHTUP_CORNER, 575, 363],
#
#                                [LITTLE_PLAT, 543, 198]]
#
#         self.platMovingCoords = [[MOVING_Y_PLAT, 83, 282],
#                                  [MOVING_Y_PLAT, 1035, 282],
#                                  [MOVING_X_PLAT, 291, 372],
#                                  [MOVING_X_PLAT, 849, 372],
#                                  [MOVING_X_PLAT, 491, 279]]
#
#         self.enemyCoords = [[LEFT_SPIKES, 415, 190],
#                             [RIGHT_SPIKES, 714, 190]]
#
#         self.doorClosedCoords = [[DOOR_CLOSED, 795, 74]]
#         self.doorOpenedCoords = [[DOOR_OPENED, 795, 74]]
#         self.buttonOffCoords = [[BUTTON_OFF, 565, 146]]
#         self.buttonOnCoords = [[BUTTON_ON, 565, 146]]
#
#         # Adding all sprites to the scenario
#         self.addDoors()
#         self.addButtons()
#         self.addPlatforms()
#         self.addEnemies()
#
#         # Manually adding moving plats (plat, x.vel, y.vel, (top, bottom), (left right), self)
#         platMove1 = MovingPlatform(self.platMovingCoords[0],
#                                    0, 2, (250, 400), (0, 0), self)
#         platMove2 = MovingPlatform(self.platMovingCoords[1],
#                                    0, 2, (250, 400), (0, 0), self)
#         platMove3 = MovingPlatform(self.platMovingCoords[2],
#                                    2, 0, (0, 0), (215, 325), self)
#         platMove4 = MovingPlatform(self.platMovingCoords[3],
#                                    2, 0, (0, 0), (820, 950), self)
#         platMove5 = MovingPlatform(self.platMovingCoords[4],
#                                    2, 0, (0, 0), (420, 685), self)
#
#         self.platMoving.add(platMove1)
#         self.platMoving.add(platMove2)
#         self.platMoving.add(platMove3)
#         self.platMoving.add(platMove4)
#         self.platMoving.add(platMove5)
#
#         # Manually adding transparent platforms
#         for plat in self.platTransparentCoords:
#


        # spawn = (70, 510)
        # spawn = (315, 180)
