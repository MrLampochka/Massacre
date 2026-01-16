import asyncio

import pygame as pg

import settings
from scenes.game_preview import SimpleGame
from gui.menu_button import SimpleMenuButton
from core.window import Window
from scenes.balls_game import BallsGame
from scenes.tower_defense import TowerDefense

class Menu:
    def __init__(self, window: Window = Window(), games: settings.GAMES = None):
        # Инициализация Pygame
        self.window = window

        # Цвета
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.MEDIUMGRAY = (100, 100, 100)
        self.DARKGRAY = (50, 50, 50)
        self.BLACK = (15, 15, 15)

        self.FONT = None
        self.buttons = []

        self._set_menu()

    def _set_menu(self):
        self.FONT = pg.font.Font(None, int(self.window(40)))
        button_size = self.window(x=300, y=50)
        y_padding = 10
        top_offset = 20
        self.buttons = [
            SimpleMenuButton("Бильярд", (self.window.width // 2 - self.window(x=150), button_size[1] + y_padding - top_offset) ,
                             button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Защита башни", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 2 - top_offset) ,
                             button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Preview", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 3 - top_offset),
                             button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Настройки", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 4 - top_offset), button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Выход", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 5 - top_offset), button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
        ]

    def draw(self):
        for b in self.buttons:
            b.update_color()
            b.draw(self.window.screen)

    async def run(self):
        running = True
        clock = pg.time.Clock()
        self._set_menu()

        while running:

            self.window.screen.fill(self.BLACK)
            self.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in self.buttons:
                        if b.is_hovered():
                            if b.text == "Защита башни":
                                TowerDefense(Window(size=settings.MAIN_SCREEN_SIZE, caption=settings.MAIN_WINDOW_CAPTION, FPS=settings.FPS, vsync=1, flags=pg.DOUBLEBUF | pg.RESIZABLE)).start()
                                self.window.update()
                            elif b.text == "Бильярд":
                                BallsGame(Window(size=settings.MAIN_SCREEN_SIZE, caption="Бильярд", FPS=settings.FPS, vsync=1)).start()
                                self.window.update()
                            elif b.text == "Настройки":
                                pass
                            elif b.text == "Preview":
                                SimpleGame(Window(size=(800, 600), caption="Simple Game", FPS=60)).start()
                                self.window.update()
                            elif b.text == "Выход":
                                self.window.screen.fill((0, 0, 0))
                                running = False


                if event.type == pg.VIDEORESIZE:
                    self.window.resize(event.size)
                    self._set_menu()

            pg.display.flip()
            clock.tick(self.window.FPS)
            await asyncio.sleep(0)



# Запуск меню
if __name__ == "__main__":
    asyncio.run(Menu().run())
    pg.quit()
