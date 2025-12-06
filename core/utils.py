import math
from dataclasses import dataclass

import pygame.sprite
from pygame import Vector2


def get_distance(from_pos, to_pos):
    dx = from_pos[0] - to_pos[0]
    dy = from_pos[1] - to_pos[1]
    return math.hypot(dx, dy)

    # if distance < (circle1_radius + circle2_radius):


class SimpleTimerOld:
    def __init__(self):
        self.time = None
        self.start_time = pygame.time.get_ticks()

    def __call__(self):
        return pygame.time.get_ticks() - self.start_time

    def start(self, msec):
        self.start_time = pygame.time.get_ticks()
        self.time = msec

    @property
    def ratio(self):
        if self.time == 0:
            return 1
        #
        return max(0, min((1, (pygame.time.get_ticks() - self.start_time) / self.time))) if self.time else 0

    def is_expired(self):
        if not self.time:
            return False
        return True if (pygame.time.get_ticks() >= (self.start_time + self.time)) else False

    def stop(self):
        self.__init__()

    def is_expired_restart(self, msec):
        if not self.time:
            self.start(msec)
            return False

        if self.is_expired():
            self.start(msec)
            return True
        else:
            return False


class SmoothMovementMixin:
    _x: float
    _y: float

    def __init__(self, pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pos = pos

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def pos(self):
        return Vector2(self.x, self.y)

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

class SimpleTimer:
    def __init__(self, duration=0):
        self.duration = duration
        self.time_left = 0
        self.running = False

    def start(self, duration=None):
        if duration is not None:
            self.duration = duration
        self.time_left = self.duration
        self.running = True
        return self

    def stop(self, time_left=0):
        self.time_left = time_left
        self.running = False

    @property
    def is_expired(self):
        return not self.running

    @property
    def remaining(self):
        return max(0, self.time_left)

    @property
    def ratio(self):
        if self.duration == 0:
            return 1.0
        return 1.0 - (self.time_left / self.duration)

    def update(self, dt):
        if self.running:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.running = False


@dataclass
class SV:
    current: float | None = None
    max: float | None = None

    def __init__(self, value: float | None = None, max_value: float | None = None):
        self.current = value
        self.max = max_value if max_value is not None else value

    def __bool__(self):
        return self.current is not None

    @property
    def ratio(self) -> float:
        if self.current is None or self.max in (None, 0):
            return 0.0
        return self.current / self.max

    def assign(self, current, max_value):
        self.current, self.max = current, max_value
