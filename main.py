import asyncio

import pygame as pg

import settings
from scenes.menu import Menu
from core.window import Window


async def main():
    await Menu(
        Window(size=settings.MENU_SCREEN_SIZE, caption=settings.MENU_WINDOW_CAPTION, FPS=settings.FPS, flags=pg.RESIZABLE),
        games=settings.GAMES
    ).run()


if __name__ == '__main__':
    pg.init()
    asyncio.run(main())
