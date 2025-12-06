import asyncio

import pygame as pg

import config
from core.menu import Menu
from core.window import Window


async def main():
    await Menu(
        Window(size=config.MENU_SCREEN_SIZE, caption=config.MENU_WINDOW_CAPTION, FPS=config.FPS, flags=pg.RESIZABLE),
        games=config.GAMES
    ).run()


if __name__ == '__main__':
    pg.init()
    asyncio.run(main())
