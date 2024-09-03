import pygame

import config
from core.game import Game


def main():
    pygame.init()
    game = Game(
        screen_size=config.SCREEN_SIZE,
        FPS=config.FPS,
        caption=config.WINDOW_CAPTION,
    )
    game.start()


if __name__ == '__main__':
    main()
