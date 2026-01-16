import random
from dataclasses import dataclass
from enum import IntEnum

from pygame import Vector2

from core.component import Component


#
#
# def get_distance(from_pos, to_pos):
#     dx = from_pos[0] - to_pos[0]
#     dy = from_pos[1] - to_pos[1]
#     return math.hypot(dx, dy)
#
#     # if distance < (circle1_radius + circle2_radius):


# class SimpleTimerOld:
#     def __init__(self):
#         self.time = None
#         self.start_time = pygame.time.get_ticks()
#
#     def __call__(self):
#         return pygame.time.get_ticks() - self.start_time
#
#     def start(self, msec):
#         self.start_time = pygame.time.get_ticks()
#         self.time = msec
#
#     @property
#     def ratio(self):
#         if self.time == 0:
#             return 1
#         #
#         return max(0, min((1, (pygame.time.get_ticks() - self.start_time) / self.time))) if self.time else 0
#
#     def is_expired(self):
#         if not self.time:
#             return False
#         return True if (pygame.time.get_ticks() >= (self.start_time + self.time)) else False
#
#     def stop(self):
#         self.__init__()
#
#     def is_expired_restart(self, msec):
#         if not self.time:
#             self.start(msec)
#             return False
#
#         if self.is_expired():
#             self.start(msec)
#             return True
#         else:
#             return False


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
        self.value: SV = SV(0)

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
            self.value = SV(self.duration - self.time_left, self.duration)
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

    def ratio(self, rev=False) -> float:
        if self.current is None or self.max in (None, 0):
            return 0.0 if not rev else 1.0
        r = self.current / self.max
        return 1.0 - r if rev else r

    def assign(self, current, max_value):
        self.current, self.max = current, max_value


class Timer:
    def __init__(self, value=None, cb=None):
        super().__init__()
        self.value: SV = SV(value) if value else SV(0)
        self.running = False
        self.cb = cb
        self.is_expired = False

    def start(self, value=None, cb=None):
        if value:
            self.value = SV(value)
        else:
            self.value.current = self.value.max

        if cb:
            self.cb = cb

        self.running = True
        self.is_expired = False

    def stop(self):
        self.running = False
        self.is_expired = False
        self.value.current = self.value.max

    def update(self, dt):
        if self.running:
            self.value.current -= dt

        if self.value.current <= 0:
            self.value.current = 0
            self.running = False
            self.is_expired = True

            if self.cb:
                self.cb()


def merge_dicts(a, b):
    cfg = a.copy()
    for k, v in b.items():
        if k in cfg and isinstance(v, dict) and isinstance(cfg[k], dict):
            cfg[k] = merge_dicts(cfg[k], v)
        else:
            cfg[k] = v

    return cfg


class GroupContainer:
    class Layer(IntEnum):
        TOWER = 0
        UNIT = 1
        PROJECTILE = 2
        UI = 3

    def __init__(self, **groups):
        self._groups = groups

    def __getattr__(self, item):
        try:
            return self._groups[item]
        except KeyError:
            raise AttributeError(item)

    def draw(self, screen):
        for group in self._groups.values():
            group.draw(screen)

    def update(self, dt):
        for group in self._groups.values():
            group.update(dt)


class Point:
    def __init__(self, area: tuple[tuple[int, int], tuple[int, int]] = None, points: list[tuple[int, int]] = None):
        self.area = area
        self.points = points

    def get_random(self) -> Vector2:
        if self.area is None:
            raise ValueError("No area defined for random position")

        (_x, _y), (w, h) = self.area
        x = random.uniform(_x, _x + w)
        y = random.uniform(_y, _y + h)
        return Vector2(x, y)

    def get_point(self, index: int) -> Vector2:
        if not self.points:
            raise ValueError("No points defined for this Position")
        return Vector2(self.points[index % len(self.points)])

    def get(self, index: int = 0) -> Vector2:
        if self.points:
            return self.get_point(index)
        elif self.area:
            return self.get_random()
        else:
            raise ValueError("Position must have either points or area")
