import asyncio
from abc import ABC, abstractmethod
import pygame
from core.window import Window


class BaseGame(ABC):
    """Базовый класс для игры на Pygame с поддержкой дельты времени и окна."""

    def __init__(self, window: Window):
        self._window = window
        self.screen: pygame.Surface = self._window.screen
        self._clock = pygame.time.Clock()
        self._running = False
        self._dt = 0

    def start(self):
        """Запуск игры: синхронно или асинхронно."""
        self._set_game()
        self._running = True

        try:
            asyncio.get_running_loop().run_until_complete(self._async_game_loop)
        except RuntimeError:
            self._game_loop()

    def stop(self):
        self._running = False

    def _tick(self):
        self._dt = self._clock.tick(self._window.FPS) / 1000
        self._events()
        self._update(self._dt)
        self._draw(self.screen)
        self._render()

    async def _async_game_loop(self):
        while self._running:
            self._tick()
            await asyncio.sleep(0)

    def _game_loop(self):
        while self._running:
            self._tick()

    @staticmethod
    def _render():
        pygame.display.flip()

    @abstractmethod
    def _set_game(self):
        """Инициализация объектов игры (переопределяется в наследнике)."""
        pass

    @abstractmethod
    def _events(self):
        """Обработка событий Pygame (переопределяется в наследнике)."""
        pass

    @abstractmethod
    def _update(self, dt: float):
        """Логика обновления состояния игры (переопределяется в наследнике)."""
        pass

    @abstractmethod
    def _draw(self, screen: pygame.Surface):
        """Отрисовка объектов на экране (переопределяется в наследнике)."""
        pass

    def resize(self, size):
        self._window.resize(size)