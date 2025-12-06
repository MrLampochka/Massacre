import asyncio

import pygame as pg

import config
from core.gui.menu_button import SimpleMenuButton
from core.window import Window
from games.balls_game import BallsGame
from games.tower_defense import TowerDefense

class Menu:
    def __init__(self, window: Window = Window(), games: config.GAMES = None):
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
        self.buttons = [
            SimpleMenuButton("Бильярд", (self.window.width // 2 - self.window(x=150), button_size[1] + y_padding),
                             button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Защита башни", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 2),
                             button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Настройки", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 3), button_size, None,
                             self.FONT, self.DARKGRAY,
                             self.MEDIUMGRAY,
                             self.GRAY),
            SimpleMenuButton("Выход", (self.window.width // 2 - self.window(x=150), (button_size[1] + y_padding) * 4), button_size, None,
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
                                TowerDefense(Window(size=config.MAIN_SCREEN_SIZE, caption=config.MAIN_WINDOW_CAPTION, FPS=config.FPS, vsync=1, flags=pg.DOUBLEBUF | pg.RESIZABLE)).start()
                                self.window.update()
                            elif b.text == "Бильярд":
                                BallsGame(Window(size=config.MAIN_SCREEN_SIZE, caption="Бильярд", FPS=config.FPS, vsync=1)).start()
                                self.window.update()
                            elif b.text == "Настройки":
                                pass
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
