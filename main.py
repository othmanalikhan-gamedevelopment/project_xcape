import pygame
from xcape.engines.core import CoreEngine


def main():
    """
    Runs the game.
    """
    pygame.init()
    game = CoreEngine()
    game.run()


if __name__ == "__main__":
    main()
