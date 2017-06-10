"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.settings as settings
from xcape.common.loader import sceneResources
from xcape.common.object import GameObject
from xcape.entities.characters import Player
from xcape.entities.scene import (
    Wall, SPlatform, DPlatform, MPlatform, Switch, Door, Spike
)


class BaseScene(GameObject):
    """
    The base scene for any scene.
    """

    def __init__(self, screen):
        """
        :param screen: pygame.Surface, representing the screen.
        """
        self.screen = screen
        self.rect = pg.Rect(0, 0, 0, 0)
        self.levelNum = 0
        self.spawn = None

        self.walls = []
        self.sPlatforms = []
        self.mPlatforms = []
        self.dPlatforms = []
        self.switches = []
        self.doors = []
        self.spikes = []

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

    def addSPlatforms(self):
        """
        Adds static platforms to the scene.

        :return: List, containing platform entities.
        """
        pass

    def addMPlatforms(self):
        """
        Adds moving platforms to the scene.

        :return: List, containing platform entities.
        """
        pass

    def addDPlatforms(self):
        """
        Adds directional platforms to the scene.

        :return: List, containing platform entities.
        """
        pass

    def addDoors(self):
        """
        Adds doors to the scene.

        :return: List, containing door entities.
        """
        pass

    def addSwitches(self):
        """
        Adds buttons to the scene.

        :return: List, containing button entities.
        """
        pass

    def addSpikes(self):
        """
        Adds enemies to the scene.

        :return: List, containing enemy entities.
        """
        pass


class BlankScene(BaseScene):
    """
    A blank scene that does nothing except display a blank screen.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.player = Player(screen)
        self.spawn = (0, 0)


class SoloScene01(BaseScene):
    """
    The first single player scene of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.spawn = (70, 70)
        self.levelNum = 1

        self.image = sceneResources["screens"]["scene_01.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.walls = self.addWalls()
        self.sPlatforms = self.addSPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()

    def handleEvent(self, event):
        if event.type == events.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.sPlatforms]
        [s.drawWithCamera(camera) for s in self.switches]
        [d.drawWithCamera(camera) for d in self.doors]

    def addWalls(self):
        wall = sceneResources["walls"]
        boundaries = \
        [
            Wall(-45, 10, 8, "v", wall["boundary_left.png"], self.screen),
            Wall(-45, 520, 11, "h", wall["boundary_bot.png"], self.screen),
            Wall(610, 138, 6, "v", wall["boundary_right.png"], self.screen),
            Wall(164, 138, 7, "h", wall["boundary_top.png"], self.screen),
            Wall(160, 9, 2, "v", wall["boundary_right.png"], self.screen),
        ]

        obstacles = \
        [
            Wall(5, 460, 1, "h", wall["block_left.png"], self.screen),
            Wall(65, 460, 1, "h", wall["block_right.png"], self.screen),
            Wall(150, 490, 1, "h", wall["block_small.png"], self.screen),
        ]

        return boundaries + obstacles

    def addSPlatforms(self):
        platforms = \
        [
            SPlatform(260, 370, 2, self.screen),
            SPlatform(500, 310, 1, self.screen),
            SPlatform(200, 250, 3, self.screen),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(330, 320, 1, self.screen),
            Switch(540, 260, 2, self.screen),
            Switch(210, 200, 3, self.screen)
        ]
        return switches

    def addDoors(self):
        door1 = Door(515, 410, 1, self.screen)
        door1.waitForSwitches([1, 2, 3])
        return [door1]


class SoloScene02(BaseScene):
    """
    The second single player scene of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.spawn = (70, 510)
        self.levelNum = 2

        self.image = sceneResources["screens"]["scene_02.jpg"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.walls = self.addWalls()
        self.dPlatforms = self.addDPlatforms()
        self.mPlatforms = self.addMPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()
        self.spikes = self.addSpikes()

    def handleEvent(self, event):
        if event.type == events.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        [p.update() for p in self.mPlatforms]

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.dPlatforms]
        [p.drawWithCamera(camera) for p in self.mPlatforms]
        [s.drawWithCamera(camera) for s in self.switches]
        [d.drawWithCamera(camera) for d in self.doors]
        [s.drawWithCamera(camera) for s in self.spikes]

    def addWalls(self):
        wall = sceneResources["walls"]
        boundaries = \
        [
            Wall(0, 10, 9, "v", wall["boundary_left.png"], self.screen),
            Wall(0, 548, 15, "h", wall["boundary_bot.png"], self.screen),
            Wall(952, 25, 9, "v", wall["boundary_right.png"], self.screen),
        ]

        obstacles = \
        [
            Wall(210, 300, 1, "h", wall["block_left.png"], self.screen),
            Wall(265, 300, 1, "h", wall["block_right.png"], self.screen),

            Wall(435, 490, 1, "h", wall["block_left.png"], self.screen),
            Wall(490, 490, 1, "h", wall["block_right.png"], self.screen),

            Wall(655, 300, 1, "h", wall["block_left.png"], self.screen),
            Wall(710, 300, 1, "h", wall["block_right.png"], self.screen),

            Wall(770, 42, 4, "v", wall["plat_mid.png"], self.screen),
            Wall(770, 297, 1, "v", wall["plat_bot.png"], self.screen),
        ]

        return boundaries + obstacles

    def addDPlatforms(self):
        platforms = \
        [
            DPlatform(170, 450, 1, self.screen),
            DPlatform(60, 330, 0, self.screen),
        ]
        return platforms

    def addMPlatforms(self):
        vImage = sceneResources["platforms"]["moving_vertical.png"]
        hImage = sceneResources["platforms"]["moving_horizontal.png"]

        platforms = \
        [
            MPlatform((150, 260), (350, 260), 10, 0, self.screen, hImage),
            MPlatform((340, 450), (600, 450), 10, 0, self.screen, hImage),
            MPlatform((340, 300), (600, 300), 10, 0, self.screen, hImage),
            MPlatform((660, 350), (660, 435), 0, 0, self.screen, vImage),
            MPlatform((660, 435), (660, 520), 0, 0, self.screen, vImage),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(250, 200, 1, self.screen),
            Switch(480, 200, 2, self.screen),
            Switch(480, 430, 3, self.screen),
            Switch(700, 200, 4, self.screen),
        ]
        return switches

    def addDoors(self):
        door1 = Door(850, 440, 1, self.screen)
        door1.waitForSwitches([1, 2, 3, 4])
        return [door1]

    def addSpikes(self):
        spike = sceneResources["spikes"]
        spikes = \
        [
            Spike(325, 525, 5, "h", spike["up.png"], self.screen),
            Spike(550, 525, 5, "h", spike["up.png"], self.screen),
        ]
        return spikes


class SoloScene03(BaseScene):
    """
    The third single player scene of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        # self.spawn = (315, 180)
        self.spawn = (70, 510)
        self.levelNum = 2

        self.image = sceneResources["screens"]["scene_02.jpg"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.walls = self.addWalls()
        self.dPlatforms = self.addDPlatforms()
        self.mPlatforms = self.addMPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()
        self.spikes = self.addSpikes()

    def handleEvent(self, event):
        if event.type == events.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        [p.update() for p in self.mPlatforms]

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.dPlatforms]
        [p.drawWithCamera(camera) for p in self.mPlatforms]
        [s.drawWithCamera(camera) for s in self.switches]
        [d.drawWithCamera(camera) for d in self.doors]
        [s.drawWithCamera(camera) for s in self.spikes]

    def addWalls(self):
        wall = sceneResources["walls"]
        boundaries = \
        [
            Wall(0, 10, 9, "v", wall["boundary_left.png"], self.screen),
            Wall(0, 548, 15, "h", wall["boundary_bot.png"], self.screen),
            Wall(952, 25, 9, "v", wall["boundary_right.png"], self.screen),
        ]

        obstacles = \
        [
            Wall(210, 300, 1, "h", wall["block_left.png"], self.screen),
            Wall(265, 300, 1, "h", wall["block_right.png"], self.screen),

            Wall(435, 490, 1, "h", wall["block_left.png"], self.screen),
            Wall(490, 490, 1, "h", wall["block_right.png"], self.screen),

            Wall(655, 300, 1, "h", wall["block_left.png"], self.screen),
            Wall(710, 300, 1, "h", wall["block_right.png"], self.screen),

            Wall(770, 42, 4, "v", wall["plat_mid.png"], self.screen),
            Wall(770, 297, 1, "v", wall["plat_bot.png"], self.screen),
        ]

        return boundaries + obstacles

    def addDPlatforms(self):
        platforms = \
        [
            DPlatform(170, 450, 1, self.screen),
            DPlatform(60, 330, 0, self.screen),
        ]
        return platforms

    def addMPlatforms(self):
        vImage = sceneResources["platforms"]["moving_vertical.png"]
        hImage = sceneResources["platforms"]["moving_horizontal.png"]

        platforms = \
        [
            MPlatform((150, 260), (350, 260), 10, 0, self.screen, hImage),
            MPlatform((340, 450), (600, 450), 10, 0, self.screen, hImage),
            MPlatform((340, 300), (600, 300), 10, 0, self.screen, hImage),
            MPlatform((660, 350), (660, 435), 0, 0, self.screen, vImage),
            MPlatform((660, 435), (660, 520), 0, 0, self.screen, vImage),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(250, 200, 1, self.screen),
            Switch(480, 200, 2, self.screen),
            Switch(480, 430, 3, self.screen),
            Switch(700, 200, 4, self.screen),
        ]
        return switches

    def addDoors(self):
        door1 = Door(850, 440, 1, self.screen)
        door1.waitForSwitches([1, 2, 3, 4])
        return [door1]

    def addSpikes(self):
        spike = sceneResources["spikes"]
        spikes = \
        [
            Spike(325, 525, 5, "h", spike["up.png"], self.screen),
            Spike(550, 525, 5, "h", spike["up.png"], self.screen),
        ]
        return spikes


class SoloScene04(BaseScene):
    """
    The first single player scene of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.spawn = (70, 70)
        self.levelNum = 1

        self.image = sceneResources["screens"]["scene_01.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.player = Player(self.screen)



        self.walls = self.addWalls()
        self.sPlatforms = self.addSPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()
        # self.bosses = [PigBoss(screen["characters"])]

    def handleEvent(self, event):
        self.player.handleEvent(event)

        if event.type == events.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        # [b.update() for b in self.bosses]
        self.player.update()

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.sPlatforms]
        [s.drawWithCamera(camera) for s in self.switches]
        [d.drawWithCamera(camera) for d in self.doors]
        self.player.drawWithCamera(camera)

    def addWalls(self):
        wall = sceneResources["walls"]
        boundaries = \
        [
            Wall(-45, 10, 8, "v", wall["boundary_left.png"], self.screen),
            Wall(-45, 520, 11, "h", wall["boundary_bot.png"], self.screen),
            Wall(610, 138, 6, "v", wall["boundary_right.png"], self.screen),
            Wall(164, 138, 7, "h", wall["boundary_top.png"], self.screen),
            Wall(160, 9, 2, "v", wall["boundary_right.png"], self.screen),
        ]

        obstacles = \
        [
            Wall(5, 460, 1, "h", wall["block_left.png"], self.screen),
            Wall(65, 460, 1, "h", wall["block_right.png"], self.screen),
            Wall(150, 490, 1, "h", wall["block_small.png"], self.screen),
        ]

        return boundaries + obstacles

    def addSPlatforms(self):
        platforms = \
        [
            SPlatform(260, 370, 2, self.screen),
            SPlatform(500, 310, 1, self.screen),
            SPlatform(200, 250, 3, self.screen),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(330, 320, 1, self.screen),
            Switch(540, 260, 2, self.screen),
            Switch(210, 200, 3, self.screen)
        ]
        return switches

    def addDoors(self):
        door1 = Door(515, 410, 1, self.screen)
        door1.waitForSwitches([1, 2, 3])
        return [door1]

