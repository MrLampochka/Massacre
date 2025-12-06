from enum import Enum, auto

import pygame


import config
from core.gui.gui import GUI
from core.old.player_old import Player, PSide

unit_keys = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]


class GameMode(Enum):
    single = auto()
    dual = auto()


class Game:
    def __init__(
            self,
            screen_size: tuple = (400, 300),
            FPS: int = 30,
            caption: str = "",
    ):
        self._FPS = FPS
        self._caption = caption
        self._screen_size = screen_size
        self._clock = pygame.time.Clock()

    def start(self):
        self._set_game(self._screen_size)
        self._game_loop()

    def _game_loop(self):
        self._running = True
        while self._running:
            self._time_controller()
            self._events()
            self._update()
            self._draw()

    def _time_controller(self):
        self._time_delta = self._clock.tick(self._FPS) / 1000

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
                                unit = config.units_list[i]
                                self._players[1].add_unit(unit)
            else:
                self._gui.handler(event)

    def _update(self):
        self._gui.update(self._time_delta)
        self._update_units()

    def _draw(self):
        self._screen.fill(config.SCREEN_FILL)
        self._screen.blit(self.background_image, (0, 0))

        self._draw_units()
        self._gui.draw(self._screen)
        pygame.display.set_caption(f"FPS: {int(self._clock.get_fps())}")
        pygame.display.flip()

    def _draw_units(self):
        warriors = []
        for p in self._players:
            for u in p.units:
                warriors.append(u)

        warriors.sort(key=lambda s: s.rect.y)
        warriors.sort(key=lambda s: s.live)
        line_surface = pygame.Surface(config.MAIN_SCREEN_SIZE, pygame.SRCALPHA)
        for w in warriors:
            self._screen.blit(w.image, w.rect)
            w.draw_ammo(line_surface)

        self._screen.blit(line_surface, (0, 0))

    def _update_units(self):
        self._players[0].update(self._players[1].units)
        self._players[1].update(self._players[0].units)

    def _set_game(self, size):
        self._game_mode = GameMode.dual
        self._set_music()
        self._set_players()
        self._set_screen(size)

    def _set_screen(self, size):
        pygame.display.set_caption(self._caption)
        pygame.mouse.set_visible(True)
        self._screen = pygame.display.set_mode(size, pygame.DOUBLEBUF)
        self._gui = GUI(screen=self._screen, max_button_count=9, players=self._players, units=config.units_list, padding=config.GUI_PADDING)
        self.background_image = pygame.transform.scale(pygame.image.load('../../assets/images/backgrounds/background.jpg').subsurface((200, 900), (config.MAIN_SCREEN_WIDTH * 2, config.MAIN_SCREEN_HEIGHT * 2)), config.MAIN_SCREEN_SIZE)

    def _set_players(self):
        self._players = []
        self._players.append(Player(PSide.left, config.PLAYER_START_COINS, config.PLAYER_COIN_TIME))

        if self._game_mode == GameMode.dual:
            self._players.append(Player(PSide.right, config.PLAYER_START_COINS, config.PLAYER_COIN_TIME))

    def _set_music(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(64)

if __name__ == '__main__':
    pygame.init()
    Game().start()
