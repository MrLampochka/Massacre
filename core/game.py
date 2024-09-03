from enum import Enum, auto

import pygame


import config
from core.gui import GUI
from core.player import Player, PlayerSide

unit_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]


class GameMode(Enum):
    single = auto()
    dual = auto()


class Game:
    def __init__(
            self,
            screen_size: tuple = (400, 300),
            FPS: int = 30,
            caption: str = "Default caption",
    ):
        self._FPS = FPS
        self._caption = caption
        self._screen_size = screen_size
        self._clock = pygame.time.Clock()
        self._gui = GUI(max_button_count=9)
        self.last_time = 0

    def start(self):
        self._set_game_mode()
        self._set_music()
        self._set_players()
        self._set_units()
        self._set_screen(self._screen_size)
        self._start_game_loop()

    def _start_game_loop(self):
        self._running = True
        while self._running:
            self._time_controller()
            self._events()
            self._update()
            self._draw()

    def _update(self):
        self._gui.update(self._time_delta, self._players[0].coins, self._players[1].coins)
        self._update_units()

    def _events(self):
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                self._set_screen(event.size)
            elif event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                if event.key == pygame.K_r:
                    self.start()
                else:
                    if self._players[1]:
                        for i, k in enumerate(unit_keys):
                            if event.key == k:
                                self._players[1].add_unit(i)
            else:
                self._gui.process_event(event)

    def _draw(self):
        self._screen.fill(config.SCREEN_FILL)
        self._draw_units()
        self._gui.draw(self._screen)
        pygame.display.set_caption(f"FPS: {int(self._clock.get_fps())}")
        pygame.display.flip()

    def _time_controller(self):
        self._time_delta = self._clock.tick(self._FPS) / 1000

    def _set_players(self):
        self._players = []
        self._players.append(Player(config.PLAYER_START_COINS, side=PlayerSide.left))
        # for n in range(1000):
        #     self._players[0].add_unit(0)

        if self._game_mode == GameMode.dual:
            self._players.append(Player(config.PLAYER_START_COINS, side=PlayerSide.right))

    def _draw_units(self):
        warriors = []
        for p in self._players:
            for u in p.units:
                warriors.append(u)

        warriors.sort(key=lambda s: s.rect.y)
        warriors.sort(key=lambda s: s.live)
        line_surface = pygame.Surface(config.SCREEN_SIZE, pygame.SRCALPHA)
        for w in warriors:
            self._screen.blit(w.image, w.rect)
            w.draw_ammo(line_surface)

        self._screen.blit(line_surface, (0, 0))

    def _update_units(self):
        # current_time = pygame.time.get_ticks()
        #
        # # Проверяем, прошло ли 10 секунд (10000 миллисекунд)
        # if current_time - self.last_time >= 1000:
        #     self._players[1].add_unit(0)
        #     self.last_time = current_time  # Обновляем время
        self._players[0].update(self._players[1].units)
        self._players[1].update(self._players[0].units)

    def _set_screen(self, size):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(True)
        self._screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        self._gui.set(self._screen)

    def _set_game_mode(self):
        self._game_mode = GameMode.dual

    def _set_units(self):
        for i, b in enumerate(config.units_list):
            self._gui.add_button(f"{b['name']} {b['cost']}", self._players[0].add_unit)

    def _set_music(self):
        pygame.mixer.set_num_channels(9999)
