"""
Responsible for containing all the scenes in game.
"""

import pygame as pg

import xcape.common.settings as settings
import xcape.components.dialogue as dialogue
from xcape.common.loader import ZONE1_RESOURCES
from xcape.common.scene import BaseScene
from xcape.components.render import RenderComponent, Dialogue
from xcape.entities.bosses import PigBoss
from xcape.entities.players import PlayerOne, PlayerTwo
from xcape.entities.scene import (
    Wall, SPlatform, DPlatform, MPlatform, Switch, Door, Spike, Decoration
)


class JailScene01(BaseScene):

    LEVEL_NUM = 1

    def __init__(self, screen):
        super().__init__(screen)

        self.players = self.addPlayers()
        self.walls = self.addWalls()
        self.dPlatforms = self.addDPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()
        self.decorations = self.addDecorations()

        self.elapsed = 0
        self.origin = pg.time.get_ticks()

        image = ZONE1_RESOURCES["levels"]["coop_jail_01"]
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.JAIL_COOP_1A, 10, 410, "caption")
        self.dialogue.add(dialogue.JAIL_COOP_1B, 10, 410, "caption")

    def __str__(self):
        return "coop_jail_scene_01"

    def handleEvent(self, event):
        [p.handleEvent(event) for p in self.players]

        if event.type == self.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin
        self.render.update()

        [w.update() for w in self.walls]
        [d.update() for d in self.decorations]
        [d.update() for d in self.doors]
        [s.update() for s in self.switches]
        [p.update() for p in self.dPlatforms]
        [p.update() for p in self.players]

        self.dialogue.update()
        if 5000 > self.elapsed >= 0:
            self.dialogue.index = 0
        elif 15000 > self.elapsed:
            self.dialogue.index = 1
        else:
            self.dialogue.index = None

    def draw(self, camera=None):
        self.screen.fill(settings.COLOURS["black_red"])
        self.render.draw(camera)

        [w.draw(camera) for w in self.walls]
        [d.draw(camera) for d in self.decorations]
        [d.draw(camera) for d in self.doors]
        [s.draw(camera) for s in self.switches]
        [p.draw(camera) for p in self.dPlatforms]
        [p.draw(camera) for p in self.players]
        self.dialogue.draw()

    def addPlayers(self):
        p1Spawn = (100, 400)
        p2Spawn = (150, 400)
        p1 = PlayerOne(self.screen)
        p2 = PlayerTwo(self.screen)
        p1.rect.center = p1Spawn
        p2.rect.center = p2Spawn
        players = [p1, p2]
        return players

    def addWalls(self):
        wall = ZONE1_RESOURCES["walls"]

        boundaries = \
        [
            Wall(0, 10, 8, "v", wall["boundary_left"], self.screen),
            Wall(19, 478, 3, "h", wall["boundary_bot"], self.screen),
            Wall(0, 478, 1, "h", wall["inner_corner_left"], self.screen),
            # Wall(170, 260, 4, "v", wall["boundary_right"], self.screen),
            Wall(170, 478, 1, "h", wall["inner_corner_right"], self.screen),

            Wall(584, 478, 1, "h", wall["boundary_bot"], self.screen),
            Wall(628, 138, 6, "v", wall["boundary_right"], self.screen),
            Wall(164, 138, 8, "h", wall["boundary_top"], self.screen),
            Wall(160, 138, 1, "v", wall["corner_top_left"], self.screen),
            Wall(160, 10, 2, "v", wall["boundary_right"], self.screen),
            Wall(628, 138, 1, "v", wall["upper_corner_right"], self.screen),
            Wall(628, 478, 1, "h", wall["inner_corner_right"], self.screen),

            Wall(170, 260, 1, "v", wall["plat_top"], self.screen),
            Wall(170, 324, 3, "v", wall["plat_mid"], self.screen),
            Wall(170, 470, 1, "v", wall["plat_bot"], self.screen),

            Wall(106, 478, 1, "v", wall["bot_ending_right"], self.screen),
            Wall(520, 478, 1, "v", wall["bot_ending_left"], self.screen),

        ]

        obstacles = \
        [
            Wall(48, 418, 1, "h", wall["block_left"], self.screen),
            Wall(108, 418, 1, "h", wall["block_right"], self.screen),
        ]
        return boundaries + obstacles

    def addDPlatforms(self):
        platforms = \
        [
            DPlatform(240, 255, 5, self.screen),
            DPlatform(240, 330, 4, self.screen),
        ]
        return platforms

    def addSwitches(self):
        switches = \
        [
            Switch(300, 205, 1, self.screen),
            Switch(350, 205, 2, self.screen),
            Switch(400, 205, 3, self.screen),
            Switch(450, 205, 4, self.screen),
            Switch(500, 205, 5, self.screen),

            Switch(250, 290, 5, self.screen),
            Switch(300, 290, 6, self.screen),
            Switch(350, 290, 7, self.screen),
            Switch(400, 290, 8, self.screen),
            Switch(450, 290, 9, self.screen),

            Switch(250, 400, 10, self.screen),
        ]
        return switches

    def addDoors(self):
        door1 = Door(547, 370, 1, self.screen)
        door1.switchesWaiting = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        return [door1]

    def addDecorations(self):
        deco = ZONE1_RESOURCES["decorations"]
        decorations = \
        [
            Decoration(70, 393, deco["skull"][0], self.screen),
            Decoration(90, 393, deco["skull"][0], self.screen),
            Decoration(175, 236, deco["skull"][0], self.screen),
        ]
        return decorations


class JailScene02(BaseScene):

    LEVEL_NUM = 2

    def __init__(self, screen):
        super().__init__(screen)
        self.levelNum = 2

        self.players = self.addPlayers()
        self.walls = self.addWalls()
        self.dPlatforms = self.addDPlatforms()
        self.mPlatforms = self.addMPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()
        self.spikes = self.addSpikes()
        self.decorations = self.addDecorations()

        self.elapsed = 0
        self.origin = pg.time.get_ticks()

        image = ZONE1_RESOURCES["levels"]["coop_jail_02"]
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.JAIL_COOP_2, 10, 410, "caption")

    def __str__(self):
        return "coop_jail_scene_02"

    def handleEvent(self, event):
        [p.handleEvent(event) for p in self.players]

        if event.type == self.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin
        self.render.update()

        [d.update() for d in self.decorations]
        [w.update() for w in self.walls]
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        [s.update() for s in self.spikes]
        [p.update() for p in self.mPlatforms]
        [p.update() for p in self.dPlatforms]
        [p.update() for p in self.players]

        self.dialogue.update()
        if 5000 > self.elapsed >= 0:
            self.dialogue.index = 0
        else:
            self.dialogue.index = None

    def draw(self, camera=None):
        self.screen.fill(settings.COLOURS["black_red"])
        self.render.draw(camera)

        [d.draw(camera) for d in self.decorations]
        [w.draw(camera) for w in self.walls]
        [s.draw(camera) for s in self.switches]
        [d.draw(camera) for d in self.doors]
        [s.draw(camera) for s in self.spikes]
        [p.draw(camera) for p in self.mPlatforms]
        [p.draw(camera) for p in self.dPlatforms]
        [p.draw(camera) for p in self.players]
        self.dialogue.draw()

    def addPlayers(self):
        p1Spawn = (70, 510)
        p2Spawn = (90, 510)
        p1 = PlayerOne(self.screen)
        p2 = PlayerTwo(self.screen)
        p1.rect.center = p1Spawn
        p2.rect.center = p2Spawn
        players = [p1, p2]
        return players

    def addWalls(self):
        wall = ZONE1_RESOURCES["walls"]
        platWall = [wall["plat_top"][0],
                    wall["plat_mid"][0],
                    wall["plat_bot"][0]]

        boundaries = \
            [
                Wall(50, 0, 8, "h", wall["boundary_top"], self.screen),
                Wall(0, 50, 8, "v", wall["boundary_left"], self.screen),
                Wall(0, 548, 15, "h", wall["boundary_bot"], self.screen),
                Wall(0, 548, 1, "h", wall["inner_corner_left"], self.screen),
                Wall(952, 50, 8, "v", wall["boundary_right"], self.screen),
                Wall(952, 548, 1, "h", wall["inner_corner_right"], self.screen)
            ]

        obstacles = \
            [
                Wall(210, 300, 1, "h", wall["block_left"], self.screen),
                Wall(265, 300, 1, "h", wall["block_right"], self.screen),

                Wall(435, 490, 1, "h", wall["block_left"], self.screen),
                Wall(490, 490, 1, "h", wall["block_right"], self.screen),

                Wall(655, 300, 1, "h", wall["block_left"], self.screen),
                Wall(710, 300, 1, "h", wall["block_right"], self.screen),

                Wall(770, 105, 2, "v", platWall, self.screen),
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
        vImage = ZONE1_RESOURCES["platforms"]["moving_vertical"]
        hImage = ZONE1_RESOURCES["platforms"]["moving_horizontal"]

        platforms = \
            [
                MPlatform((340, 100), (600, 500), 20, 20, self.screen, hImage),
                MPlatform((660, 350), (660, 435), 0, 0, self.screen, vImage),
                MPlatform((660, 435), (660, 530), 0, 0, self.screen, vImage),
            ]
        return platforms

    def addSwitches(self):
        switches = \
            [
                # Top
                Switch(250, 200, 1, self.screen),
                Switch(480, 200, 2, self.screen),
                Switch(700, 200, 3, self.screen),

                # Middle
                Switch(370, 430, 4, self.screen),
                Switch(480, 430, 5, self.screen),
                Switch(590, 430, 6, self.screen),

                # Corners
                Switch(50, 50, 7, self.screen),
                Switch(790, 60, 8, self.screen),
            ]
        return switches

    def addDoors(self):
        door1 = Door(865, 440, 1, self.screen)
        door1.switchesWaiting = [1, 2, 3, 4, 5, 6, 7, 8]
        return [door1]

    def addSpikes(self):
        assets = ZONE1_RESOURCES["traps"]
        spikes = \
            [
                # Floor
                Spike(325, 525, 5, "h", assets["spike_up"][0], self.screen),
                Spike(550, 525, 5, "h", assets["spike_up"][0], self.screen),

                # Roof
                Spike(300, 50, 20, "h", assets["spike_down"][0], self.screen),
            ]
        return spikes

    def addDecorations(self):
        deco = ZONE1_RESOURCES["decorations"]
        decorations = \
            [
                Decoration(778, 81, deco["skull"][0], self.screen)
            ]
        return decorations


class JailScene03(BaseScene):

    LEVEL_NUM = 3

    def __init__(self, screen):
        super().__init__(screen)
        self.levelNum = 3

        self.players = self.addPlayers()
        self.bosses = self.addBosses()
        self.bosses[0].target(self.players)
        self.walls = self.addWalls()
        self.sPlatforms = self.addSPlatforms()
        self.dPlatforms = self.addDPlatforms()
        self.mPlatforms = self.addMPlatforms()
        self.switches = self.addSwitches()
        self.doors = self.addDoors()
        self.spikes = self.addSpikes()
        self.decorations = self.addDecorations()

        self.elapsed = 0
        self.origin = pg.time.get_ticks()

        image = ZONE1_RESOURCES["levels"]["coop_jail_03"]
        self.render = RenderComponent(self)
        self.render.add("idle", image)
        self.render.state = "idle"

        self.dialogue = Dialogue(self.screen)
        self.dialogue.add(dialogue.JAIL_COOP_3, 10, 410, "caption")

        self.messageCutScene("transition", "pig_cutscene")
        self.messageMenu("transition", "blank_menu")

    def __str__(self):
        return "coop_jail_scene_03"

    def handleEvent(self, event):
        [p.handleEvent(event) for p in self.players]

        if event.type == self.SCENE_EVENT:
            [d.handleEvent(event) for d in self.doors]

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin
        self.render.update()

        [w.update() for w in self.walls]
        [s.update() for s in self.switches]
        [d.update() for d in self.doors]
        [s.update() for s in self.spikes]
        [p.update() for p in self.sPlatforms]
        [p.update() for p in self.mPlatforms]
        [p.update() for p in self.dPlatforms]
        [d.update() for d in self.decorations]
        [p.update() for p in self.players]
        [b.update() for b in self.bosses]

        self.dialogue.update()
        if 5000 > self.elapsed >= 0:
            self.dialogue.draw()
        else:
            self.dialogue.index = None

    def draw(self, camera=None):
        self.screen.fill(settings.COLOURS["black_red"])
        self.render.draw(camera)

        [w.draw(camera) for w in self.walls]
        [s.draw(camera) for s in self.switches]
        [d.draw(camera) for d in self.doors]
        [s.draw(camera) for s in self.spikes]
        [p.draw(camera) for p in self.sPlatforms]
        [p.draw(camera) for p in self.mPlatforms]
        [p.draw(camera) for p in self.dPlatforms]
        [d.draw(camera) for d in self.decorations]
        [p.draw(camera) for p in self.players]
        [b.draw(camera) for b in self.bosses]
        self.dialogue.draw()

    def addPlayers(self):
        p1Spawn = (330, 210)
        p2Spawn = (330, 210)
        p1 = PlayerOne(self.screen)
        p2 = PlayerTwo(self.screen)
        p1.rect.center = p1Spawn
        p2.rect.center = p2Spawn
        players = [p1, p2]
        return players

    def addBosses(self):
        b1Spawn = (970, 280)
        b1 = PigBoss(self.screen)
        b1.rect.center = b1Spawn
        bosses = [b1]
        return bosses

    def addWalls(self):
        wall = ZONE1_RESOURCES["walls"]
        blockWall = [wall["block_left"][0],
                     wall["block_mid"][0],
                     wall["block_right"][0]]

        boundaries = \
            [
                #Wall(600, 0, 9, "v", wall["boundary_right"], self.screen),
                Wall(600, 52, 1, "v", wall["plat_top"], self.screen),
                Wall(600, 116, 7, "v", wall["plat_mid"], self.screen),
                Wall(600, 564, 1, "v", wall["plat_bot"], self.screen),

                Wall(0, 750, 20, "h", wall["boundary_bot"], self.screen),
                Wall(0, 0, 12, "v", wall["boundary_left"], self.screen),
                Wall(0, 0, 20, "h", wall["boundary_top"], self.screen),
                Wall(1250, 0, 12, "v", wall["boundary_right"], self.screen),


                Wall(0, 0, 1, "v", wall["upper_corner_left"], self.screen),
                Wall(0, 750, 1, "v", wall["inner_corner_left"], self.screen),
                Wall(1250, 0, 1, "v", wall["upper_corner_right"], self.screen),
                Wall(1250, 750, 1, "v", wall["inner_corner_right"], self.screen),
            ]

        obstacles = \
            [
                Wall(167, 330, 3, "h", blockWall, self.screen),
                Wall(220, 600, 1, "h", blockWall, self.screen),
            ]

        return boundaries + obstacles

    def addSPlatforms(self):
        platforms = \
        [
            SPlatform(240, 240, 2, self.screen),
        ]
        return platforms

    def addMPlatforms(self):
        vImage = ZONE1_RESOURCES["platforms"]["moving_vertical"]
        hImage = ZONE1_RESOURCES["platforms"]["moving_horizontal"]

        platforms = \
            [
                MPlatform((100, 100), (100, 600), 0, 20, self.screen, vImage),
                MPlatform((130, 100), (130, 600), 0, 20, self.screen, vImage),
                MPlatform((160, 100), (160, 600), 0, 20, self.screen, vImage),
                MPlatform((190, 100), (190, 600), 0, 20, self.screen, vImage),
                MPlatform((210, 100), (210, 600), 0, 20, self.screen, vImage),
                MPlatform((240, 100), (240, 600), 0, 20, self.screen, vImage),

                MPlatform((360, 100), (360, 600), 0, 20, self.screen, vImage),
                MPlatform((390, 100), (390, 600), 0, 20, self.screen, vImage),
                MPlatform((420, 100), (420, 600), 0, 20, self.screen, vImage),
                MPlatform((450, 100), (450, 600), 0, 20, self.screen, vImage),
                MPlatform((480, 100), (480, 600), 0, 20, self.screen, vImage),
                MPlatform((510, 100), (410, 600), 0, 20, self.screen, vImage),

                MPlatform((900, 200), (1000, 200), 10, 0, self.screen, hImage),
            ]
        return platforms

    def addDPlatforms(self):
        platforms = \
        [
            DPlatform(900, 660, 1, self.screen),

            DPlatform(664, 460, 1, self.screen),
            DPlatform(1143, 460, 1, self.screen),

            DPlatform(700, 260, 1, self.screen),
            DPlatform(900, 360, 1, self.screen),
            DPlatform(1100, 160, 1, self.screen),
        ]
        return platforms

    def addSwitches(self):
        switches = \
            [
                Switch(210, 200, 1, self.screen),
                Switch(400, 200, 2, self.screen),
                Switch(100, 100, 3, self.screen),
                Switch(510, 100, 4, self.screen),
                Switch(300, 480, 5, self.screen),
                Switch(940, 600, 6, self.screen),

                Switch(1200, 700, 7, self.screen),
                Switch(940, 600, 8, self.screen),
                Switch(940, 400, 9, self.screen),
                Switch(660, 50, 10, self.screen),
            ]
        return switches

    def addDoors(self):
        doors = \
        [
            Door(280, 133, 1, self.screen),
            Door(1115, 55, 2, self.screen),
        ]
        doors[0].render.state = "open"
        doors[1].switchesWaiting = list(range(1, 11))
        return doors

    def addSpikes(self):
        assets = ZONE1_RESOURCES["traps"]
        spikes = \
            [
                Spike(50, 50, 26, "h", assets["spike_down"][0], self.screen),

                Spike(165, 305, 15, "h", assets["spike_up"][0], self.screen),
                Spike(165, 380, 15, "h", assets["spike_down"][0], self.screen),

                Spike(230, 575, 8, "h", assets["spike_up"][0], self.screen),
            ]
        return spikes

    def addDecorations(self):
        skull = ZONE1_RESOURCES["decorations"]["skull"][0]
        deco = ZONE1_RESOURCES["decorations"]
        decorations = \
            [
                Decoration(500, 730, skull, self.screen),
                Decoration(530, 730, skull, self.screen),
                Decoration(560, 730, skull, self.screen),
                Decoration(590, 730, skull, self.screen),
                Decoration(620, 730, skull, self.screen),

                Decoration(750, 730, skull, self.screen),
                Decoration(780, 730, skull, self.screen),
                Decoration(810, 730, skull, self.screen),
                Decoration(840, 730, skull, self.screen),
                Decoration(870, 730, skull, self.screen),
                Decoration(900, 730, skull, self.screen),

                Decoration(1000, 730, skull, self.screen),
                Decoration(1030, 730, skull, self.screen),
                Decoration(1060, 730, skull, self.screen),
                Decoration(1090, 730, skull, self.screen),

                Decoration(1200, 730, skull, self.screen),

                Decoration(940, 513, deco["torch"], self.screen),
            ]
        return decorations
