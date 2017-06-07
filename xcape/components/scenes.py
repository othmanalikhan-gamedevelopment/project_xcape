"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.render as render
import xcape.common.settings as settings
import xcape.entities.scene as entitites

from xcape.entities.scene import Wall, StaticPlatform, Button
from xcape.common.object import GameObject
from xcape.components.animation import AnimationComponent


class BaseScene(GameObject):
    """
    The base scene for any scene.
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

    def drawWithCamera(self, camera):
        """
        Draws the scene on the screen, shifted by the camera.

        :param camera: Camera class, shifts the position of the drawn animation.
        """
        pass

    def addWalls(self):
        """
        Adds walls to the scene.

        :return: List, containing wall entities.
        """
        pass

    def addPlatforms(self):
        """
        Adds platforms to the scene.

        :return: List, containing platform entities.
        """
        pass

    def addDoors(self):
        """
        Adds doors to the scene.

        :return: List, containing door entities.
        """
        pass

    def addButtons(self):
        """
        Adds buttons to the scene.

        :return: List, containing button entities.
        """
        pass

    def addEnemies(self):
        """
        Adds enemies to the scene.

        :return: List, containing enemy entities.
        """
        pass


class BlankScene(BaseScene):
    """
    A blank scene that does nothing except display a blank screen.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.spawn = (0, 0)


class SoloScene01(BaseScene):
    """
    The first scene of the game.
    """

    def __init__(self, screen, resources):
        super().__init__(screen, resources)
        self.spawn = (70, 70)
        # self.spawn = (300, 0)
        self.levelNum = 1

        self.image = self.resources["screens"]["scene_01.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.walls = self.addWalls()
        self.platforms = self.addPlatforms()
        self.buttons = self.addButtons()
        # self.doors = pg.sprite.Group()
        # self.enemies = pg.sprite.Group()

    def addWalls(self):
        wall = self.resources["walls"]
        boundaries = \
        [
            Wall(-45, 10, 8, "v", wall["boundary_left.png"], self.screen),
            Wall(-45, 520, 11, "h", wall["boundary_bot.png"], self.screen),
            Wall(610, 138, 6, "v", wall["boundary_right.png"], self.screen),
            Wall(164, 138, 7, "h", wall["boundary_top.png"], self.screen),
            Wall(160, 9, 2, "v", wall["boundary_right.png"], self.screen),
        ]

        decorations = \
        [
            Wall(5, 460, 1, "h", wall["block_left.png"], self.screen),
            Wall(65, 460, 1, "h", wall["block_right.png"], self.screen),
            Wall(150, 490, 1, "h", wall["block_small.png"], self.screen),
        ]

        return boundaries + decorations

    def addPlatforms(self):
        platforms = \
        [
            StaticPlatform(260, 370, 2, self.screen, self.resources),
            StaticPlatform(500, 310, 1, self.screen, self.resources),
            StaticPlatform(200, 250, 3, self.screen, self.resources),
        ]
        return platforms

    def addButtons(self):
        buttons = \
        [
            Button(100, 450, self.screen, self.resources),
        ]
        return buttons

    def handleEvent(self, event):
        if event.type == pg.KEYDOWN:
            pass
            # if event.key == pg.K_RETURN:
            #     events.messageMenu("splash_menu", "transition", "main_menu")

    def update(self):
        [b.update() for b in self.buttons]

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.platforms]
        [b.drawWithCamera(camera) for b in self.buttons]










pass
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



#
#         spawn = (70, 70)
#         spawn = (70, 510)
#         spawn = (315, 180)
