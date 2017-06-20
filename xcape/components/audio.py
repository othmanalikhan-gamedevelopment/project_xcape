"""
Responsible for the audio of a game object.
"""

import pygame as pg

from xcape.common.object import GameObject


class AudioComponent(GameObject):
    """
    Attaches to a game object to allow playing of audio.
    """

    def __init__(self, gameObject, enableRepeat=False):
        """
        :param gameObject: GameObject instance, representing any object
        inheriting from the GameObject class.
        :param enableRepeat: Boolean, whether to repeat the animation endlessly.
        """
        self.state = None

        self.gameObject = gameObject
        self.enableRepeat = enableRepeat

        self.stateToSound = {}
        self.stateToLink = {}
        self.soundPlaying = None
        self.isSoundPlayed = False

        self.origin = 0
        self.elapsed = 0
        self.duration = 0

    def update(self):
        self.elapsed = pg.time.get_ticks() - self.origin

        if not self.isSoundPlayed:
            self.soundPlaying = self.stateToSound[self.state]
            self.soundPlaying.play()
            self.isSoundPlayed = True
            self.origin = pg.time.get_ticks()
            self.elapsed = 0

        # Checking if to play next sound or repeat current sound
        if self.elapsed > 1000*self.soundPlaying.get_length():
            try:
                self.state, self.duration = self.stateToLink[self.state]
                self.isSoundPlayed = False
            except KeyError:
                if self.enableRepeat:
                    self.isSoundPlayed = False

    def add(self, state, sound):
        """
        Links a sound effect to a state and sets it as the current state.

        :param sound: pygame.mixer.Sound, the sound effect object.
        :param state: String, the name of the state.
        """
        self.state = state
        self.stateToSound[state] = sound

    def link(self, state1, state2, delay=0):
        """
        Links the given two states so that two sound effects are played
        successively, separated in time by the given delay.

        :param state1: String, the name of the state to link from.
        :param state2: String, the name of the state to link to.
        :param delay: Number, the delay between transitioning states.
        """
        self.stateToLink[state1] = (state2, delay)

