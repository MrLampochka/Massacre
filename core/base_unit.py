import math
from enum import IntEnum
from typing import Tuple, Union

import pygame.draw
import pygame.mixer
import pygame.sprite

import config
from core.utils import SimpleTimer


class Direction(IntEnum):
    left = -1
    right = 1


class PowerHealthBar:
    def update_power_health_bar(self):
        height = config.BAR_HEIGHT
        health_bar_color = config.HEALTH_BAR_COLOR
        reload_bar_color = config.RELOAD_BAR_COLOR
        bar_background_color = config.BACKGROUND_BAR_COLOR

        health_bar_pos = 0, 0
        health_ratio = self._current_health / self._max_health
        pygame.draw.rect(self.image, bar_background_color, (*health_bar_pos, self.rect.width, height))
        pygame.draw.rect(self.image, health_bar_color, (*health_bar_pos, self.rect.width * health_ratio, height))

        reload_bar_pos = 0, height
        pygame.draw.rect(self.image, bar_background_color, (*reload_bar_pos, self.rect.width, height))
        pygame.draw.rect(self.image, reload_bar_color,
                         (*reload_bar_pos, self.rect.width * self._reload_timer.ratio, height))


class BaseUnit(pygame.sprite.Sprite, PowerHealthBar):
    def __init__(
            self,
            group: pygame.sprite.Group,
            pos: tuple[int, int],
            direction: int,
            size: Tuple[int, int],
            health: int,
            speed: float,
            damage: int,
            reload_time: int,
            attack_radius: int,
            visible_radius: int,
            sound: str,
            color: Union[Tuple[int, int, int], Tuple[int, int, int, int]] = (255, 255, 255),
    ):
        super().__init__(group)
        self.pos = self.x, self.y = pos
        self.size = self.width, self.height = size
        self._killing_time = config.UNIT_KILLING_TIME
        self._current_health = self._max_health = health
        self._reload_time = reload_time
        self._attack_area = attack_radius
        self._visible_area = visible_radius
        self._damage = damage
        self._color = color
        self._speed = speed
        self._direction = direction

        self.image = pygame.Surface((self.width, self.height + 10), pygame.SRCALPHA)
        self.rect = pygame.Rect(self.pos, self.size)
        self.image.fill(color)
        self._sound = pygame.mixer.Sound(sound)
        self._killing_timer = SimpleTimer()
        self._reload_timer = SimpleTimer()

        self._units = None
        self._attacking = False
        self._live = True
        self._target = None

    def update(self, units: pygame.sprite.Group):
        self._get_units_by_distance(units)

        if not self._live:
            return self._killing()

        if self._target and self._target.live:
            self._update_attack()
        else:
            self._detect_target()

        self._update_live()
        self.update_power_health_bar()
        self._update_position()

    def _update_position(self):
        self.rect.topleft = self.pos = round(self.x), round(self.y)

    def _update_attack(self):
        if not self._attacking:
            self._reload_timer.start(self._reload_time)
            self._attacking = True

        if self._reload_timer.is_expired():
            self._sound.play()
            self.attack()
            self._reload_timer.start(self._reload_time)

    def attack(self):
        pass

    def get_damage(self, damage):
        self._current_health -= damage
        return self._current_health

    def draw_ammo(self, screen):
        pass

    def _killing(self):
        if self._killing_timer.is_expired():
            self.kill()
        else:
            self.image.set_alpha(max(0, 255 - int(255 * self._killing_timer.ratio)))

    @property
    def live(self):
        return self._live

    def _update_live(self):
        if self._current_health <= 0:
            self._reload_timer.stop()
            self._killing_timer.start(self._killing_time)
            self._live = False

    def _detect_target(self):
        if self._units:
            nearest = self._units[0]
            distance_to_nearest = math.dist(nearest.rect.center, self.rect.center)

            if distance_to_nearest < self._attack_area:
                self._target = nearest
                return
            elif distance_to_nearest < self._visible_area:
                self._move_toward(nearest.rect.center)
            else:
                self._move()
        else:
            self._move()

        if self._attacking:
            self._reload_timer.stop()
            self._attacking = False

    def _get_units_by_distance(self, units):
        self._units = sorted(
            [u for u in units if u.live],
            key=lambda u: math.dist(u.rect.center, self.rect.center)
        )

    def _move(self):
        self.x += self._speed * self._direction

    def _move_toward(self, pos):
        dx, dy = pos[0] - self.rect.x, pos[1] - self.rect.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.x += dx / distance * self._speed
            self.y += dy / distance * self._speed

    @staticmethod
    def add_unit(group, pos, direction, unit):
        return unit["unit"]["class"](group, pos, direction, **unit["unit"]["kwargs"])
