import math
from enum import IntEnum
from typing import Tuple, Union

import pygame.draw
import pygame.image
import pygame.mixer
import pygame.sprite
import pygame.transform

import config
from core.ammo import Ammo, HeavyAmmo
from core.utils import SimpleTimer


class Direction(IntEnum):
    left = -1
    right = 1


class PowerHealthBar:
    def update_power_health_bar(self):
        height = config.BAR_HEIGHT
        width = self.rect.width / 2
        health_bar_color = config.HEALTH_BAR_COLOR
        reload_bar_color = config.RELOAD_BAR_COLOR
        bar_background_color = config.BACKGROUND_BAR_COLOR

        health_bar_pos = 0, 0
        health_ratio = self._current_health / self._max_health
        pygame.draw.rect(self.image, bar_background_color, (*health_bar_pos, width, height))
        pygame.draw.rect(self.image, health_bar_color, (*health_bar_pos, width * health_ratio, height))

        reload_bar_pos = 0, height
        pygame.draw.rect(self.image, bar_background_color, (*reload_bar_pos, width, height))
        pygame.draw.rect(self.image, reload_bar_color,
                         (*reload_bar_pos, width * self._reload_timer.ratio, height))


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
        self.image_dict = self.image_dict = [pygame.transform.smoothscale(pygame.image.load(f'sprites/rifle/move/survivor-move_rifle_{i}.png'), (50, 50)) for i in range(0, 19)]
        self.rect = pygame.Rect(self.pos, self.size)
        self.image.fill(color)
        self._sound = pygame.mixer.Sound(sound)
        self._killing_timer = SimpleTimer()
        self._reload_timer = SimpleTimer()

        self._units = None
        self._attacking = False
        self._live = True
        self._target = None
        self._angle = 0

    def update(self, units: pygame.sprite.Group):
        self._get_units_by_distance(units)

        if not self._live:
            return self._killing()

        if self._target and self._target.live:
            self._update_attack()
        else:
            self._detect_target()

        self._update_live()
        self._update_position()
        self.update_power_health_bar()

    def _update_position(self):
        self.rect.topleft = self.pos = round(self.x), round(self.y)
        self.image = pygame.transform.rotate(self.image_dict[0], math.degrees(self._angle))

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
                dx, dy = nearest.rect.center[0] - self.rect.x, nearest.rect.center[1] - self.rect.y
                self._angle = math.atan2(dx, dy) - math.pi / 2
                return
            elif distance_to_nearest < self._visible_area:
                dx, dy = nearest.rect.center[0] - self.rect.x, nearest.rect.center[1] - self.rect.y
                self._angle = math.atan2(dx, dy) - math.pi / 2
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
        self._angle = -math.pi / 2 + (math.pi / 2) * self._direction
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


class Warrior(BaseUnit):
    def __init__(self, group, pos, direction, **kwargs):
        super().__init__(group, pos, direction, **kwargs)

    def attack(self):
        self._target.get_damage(self._damage)


class Shooter(BaseUnit):
    def __init__(self, group, pos, direction, **kwargs):
        super().__init__(group, pos, direction, **kwargs)
        self.ammo = pygame.sprite.Group()
        self.image = self.image_dict[0]

    def attack(self):
        Ammo(self.ammo, self.rect.center, self._target.rect.center, self._damage)

    def draw_ammo(self, screen):
        self.ammo.draw(screen)
        self.ammo.update(self._units)


class HeavyShooter(BaseUnit):
    def __init__(self, group, pos, direction, **kwargs):
        super().__init__(group, pos, direction, **kwargs)
        self.ammo = pygame.sprite.Group()

    def attack(self):
        HeavyAmmo(self.ammo, self.rect.center, self._target.rect.center, self._damage)

    def draw_ammo(self, screen):
        self.ammo.update(self._units)
        for a in self.ammo:
            a.draw_line(screen)


class Tower(BaseUnit):
    def __init__(self, group, pos, direction, **kwargs):
        super().__init__(group, pos, direction, **kwargs)
        self.image_dict = self.image_dict = [pygame.transform.smoothscale(pygame.image.load(f'sprites/tower/cat.png'), (50, 50))]
        self._direction = Direction.right
    def attack(self):
        self._angle = 0
        self._target.get_damage(self._damage)


    @property
    def health(self):
        return self._current_health
