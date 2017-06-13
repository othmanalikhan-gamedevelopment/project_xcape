"""
Responsible for containing all the menus in game.
"""

import pygame as pg

import xcape.common.events as events
import xcape.common.settings as settings
from xcape.common.loader import sceneResources
from xcape.common.object import GameObject
from xcape.entities.characters import Player, PigBoss
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

        self.players = []
        self.bosses = []
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
        raise NotImplementedError

    def drawWithCamera(self, camera):
        """
        Draws the scene on the screen, shifted by the camera.

        :param camera: Camera instance, shifts the position of the drawn animation.
        """
        raise NotImplementedError

    def addPlayers(self):
        """
        Adds players to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError

    def addBosses(self):
        """
        Adds players to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError

    def addWalls(self):
        """
        Adds walls to the scene.

        :return: List, containing wall entities.
        """
        raise NotImplementedError

    def addSPlatforms(self):
        """
        Adds static platforms to the scene.

        :return: List, containing platform entities.
        """
        raise NotImplementedError

    def addMPlatforms(self):
        """
        Adds moving platforms to the scene.

        :return: List, containing platform entities.
        """
        raise NotImplementedError

    def addDPlatforms(self):
        """
        Adds directional platforms to the scene.

        :return: List, containing platform entities.
        """
        raise NotImplementedError

    def addDoors(self):
        """
        Adds doors to the scene.

        :return: List, containing door entities.
        """
        raise NotImplementedError

    def addSwitches(self):
        """
        Adds buttons to the scene.

        :return: List, containing button entities.
        """
        raise NotImplementedError

    def addSpikes(self):
        """
        Adds spikes to the scene.

        :return: List, containing enemy entities.
        """
        raise NotImplementedError


class SoloScene01(BaseScene):
    """
    The first single player scene of the game.
    """

    def __init__(self, screen):
        super().__init__(screen)
        self.spawn = (70, 300)
        self.levelNum = 1

        self.image = sceneResources["screens"]["scene_01.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.player = Player(self.screen)
        self.player.rect.center = self.spawn

        self.boss = PigBoss(self.screen)
        self.boss.rect.center = (70, 70)
        self.boss.follow(self.player)

        self.walls = self.addWalls()
        self.sPlatforms = self.addSPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()

    def handleEvent(self, event):
        self.player.handleEvent(event)
        self.boss.handleEvent(event)

        if event.type == events.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        self.player.update()
        self.boss.update()

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.sPlatforms]
        [s.drawWithCamera(camera) for s in self.switches]
        [d.drawWithCamera(camera) for d in self.doors]
        self.player.drawWithCamera(camera)
        self.boss.drawWithCamera(camera)

    def addWalls(self):
        wall = sceneResources["walls"]
        boundaries = \
        [
            Wall(0, 10, 8, "v", wall["boundary_left.png"], self.screen),
            Wall(19, 478, 4, "h", wall["boundary_bot.png"], self.screen),
            Wall(320, 478, 5, "h", wall["boundary_bot.png"], self.screen),
            Wall(628, 138, 6, "v", wall["boundary_right.png"], self.screen),
            Wall(164, 138, 8, "h", wall["boundary_top.png"], self.screen),
            Wall(160, 138, 1, "v", wall["corner_top_left.png"], self.screen),
            Wall(160, 10, 2, "v", wall["boundary_right.png"], self.screen),
            Wall(628, 138, 1, "v", wall["upper_corner_right.png"], self.screen),
            Wall(0, 478, 1, "h", wall["inner_corner_left.png"], self.screen),
            Wall(628, 478, 1, "h", wall["inner_corner_right.png"], self.screen),
            Wall(240, 478, 1, "h", wall["inner_corner_right.png"], self.screen),
            Wall(240, 426, 1, "h", wall["corner_bot_right.png"], self.screen),
            Wall(308, 426, 1, "h", wall["corner_bot_left.png"], self.screen),
            Wall(320, 478, 1, "h", wall["inner_corner_left.png"], self.screen)
        ]

        obstacles = \
        [
            Wall(48, 418, 1, "h", wall["block_left.png"], self.screen),
            Wall(108, 418, 1, "h", wall["block_right.png"], self.screen),
            Wall(170, 450, 1, "h", wall["block_small.png"], self.screen),
        ]

        return boundaries + obstacles

    def addSPlatforms(self):
        platforms = \
        [
            #SPlatform(260, 370, 2, self.screen),
            SPlatform(500, 330, 1, self.screen),
            SPlatform(200, 250, 3, self.screen),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(295, 376, 1, self.screen),
            Switch(540, 280, 2, self.screen),
            Switch(295, 205, 3, self.screen)
        ]
        return switches

    def addDoors(self):
        door1 = Door(547, 370, 1, self.screen)
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

        self.image = sceneResources["screens"]["scene_02.png"]
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
        self.spawn = (315, 180)
        # self.spawn = (70, 510)
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
        self.levelNum = 4

        self.image = sceneResources["screens"]["scene_01.png"]
        self.rect = pg.Rect(0, 0, 0, 0)
        self.rect.size = self.image.get_size()

        self.players = self.addPlayers()
        self.bosses = self.addBosses()
        self.bosses[0].follow(self.players[0])

        self.walls = self.addWalls()
        self.sPlatforms = self.addSPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()

    def handleEvent(self, event):
        [p.handleEvent(event) for p in self.players]
        [b.handleEvent(event) for b in self.bosses]

        if event.type == events.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        [p.update() for p in self.players]
        [b.update() for b in self.bosses]

    def drawWithCamera(self, camera):
        self.screen.fill(settings.COLOURS["black_red"])
        self.screen.blit(self.image, camera.apply(self))

        [w.drawWithCamera(camera) for w in self.walls]
        [p.drawWithCamera(camera) for p in self.sPlatforms]
        [s.drawWithCamera(camera) for s in self.switches]
        [d.drawWithCamera(camera) for d in self.doors]
        [p.drawWithCamera(camera) for p in self.players]
        [b.drawWithCamera(camera) for b in self.bosses]

    def addPlayers(self):
        spawn = (300, 300)
        player = [Player(self.screen)]
        player[0].rect.center = spawn
        return player

    def addBosses(self):
        spawn = (70, 70)
        boss = [PigBoss(self.screen)]
        boss[0].rect.center = spawn
        return boss

    def addWalls(self):
        wall = sceneResources["walls"]
        boundaries = \
        [
            Wall(0, 10, 8, "v", wall["boundary_left.png"], self.screen),
            Wall(19, 478, 4, "h", wall["boundary_bot.png"], self.screen),
            Wall(320, 478, 5, "h", wall["boundary_bot.png"], self.screen),
            Wall(628, 138, 6, "v", wall["boundary_right.png"], self.screen),
            Wall(164, 138, 8, "h", wall["boundary_top.png"], self.screen),
            Wall(160, 138, 1, "v", wall["corner_top_left.png"], self.screen),
            Wall(160, 10, 2, "v", wall["boundary_right.png"], self.screen),
            Wall(628, 138, 1, "v", wall["upper_corner_right.png"], self.screen),
            Wall(0, 478, 1, "h", wall["inner_corner_left.png"], self.screen),
            Wall(628, 478, 1, "h", wall["inner_corner_right.png"], self.screen),
            Wall(240, 478, 1, "h", wall["inner_corner_right.png"], self.screen),
            Wall(240, 426, 1, "h", wall["corner_bot_right.png"], self.screen),
            Wall(308, 426, 1, "h", wall["corner_bot_left.png"], self.screen),
            Wall(320, 478, 1, "h", wall["inner_corner_left.png"], self.screen)
        ]

        obstacles = \
        [
            Wall(48, 418, 1, "h", wall["block_left.png"], self.screen),
            Wall(108, 418, 1, "h", wall["block_right.png"], self.screen),
            Wall(170, 450, 1, "h", wall["block_small.png"], self.screen),
        ]

        return boundaries + obstacles

    def addSPlatforms(self):
        platforms = \
        [
            #SPlatform(260, 370, 2, self.screen),
            SPlatform(500, 330, 1, self.screen),
            SPlatform(200, 250, 3, self.screen),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(295, 376, 1, self.screen),
            Switch(540, 280, 2, self.screen),
            Switch(295, 205, 3, self.screen)
        ]
        return switches

    def addDoors(self):
        door1 = Door(547, 370, 1, self.screen)
        door1.waitForSwitches([1, 2, 3])
        return [door1]
