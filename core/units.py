import math

import pygame.sprite

import config
from core.base_ammo import BaseAmmo
from core.base_unit import BaseUnit
from core.utils import SimpleTimer


class Warrior(BaseUnit):
    def __init__(self, group, pos, direction, **kwargs):
        super().__init__(group, pos, direction, **kwargs)

    def attack(self):
        self._target.get_damage(self._damage)


class Ammo(BaseAmmo):
    def __init__(self, group, pos, target_pos, damage):
        super().__init__(group, pos, target_pos, damage, "black", config.AMMO_SIZE)


class HeavyAmmo(BaseAmmo):
    def __init__(self, group, start_pos, target_pos, damage):
        super().__init__(group, start_pos, target_pos, damage, (100, 100, 100, 255), (3, 3))
        self.x, self.y = self._start_pos = start_pos
        self._length = math.hypot(*config.SCREEN_SIZE)
        self._width, self._height = config.AMMO_SIZE

        self._angle = math.atan2(target_pos[0] - self.x, target_pos[1] - self.y)
        self._end_pos = self.x + self._length * math.sin(self._angle), self.y + self._length * math.cos(self._angle)

        self._live = True
        self._killing_time = config.AMMO_KILLING_TIME

        self._color = (100, 100, 100)
        self._killing_timer = SimpleTimer()

    def update(self, units):
        if self._live:
            for u in units:
                if u.rect.clipline(self._start_pos, self._end_pos):
                    if (health := u.get_damage(self.damage)) < 0:
                        self.damage = health * -1
                    else:
                        self._end_pos = u.rect.center
                        break

            self._live = False
            self._killing_timer.start(self._killing_time)
        else:
            self._killing()

    def _killing(self):
        if self._killing_timer.is_expired():
            self.kill()
        else:
            self._color = self._color[:3] + (max(0, 255 - int(255 * self._killing_timer.ratio)),)

    def draw_line(self, screen):
        pygame.draw.line(screen, self._color, self._start_pos, self._end_pos, self._width)


class Shooter(BaseUnit):
    def __init__(self, group, pos, direction, **kwargs):
        super().__init__(group, pos, direction, **kwargs)
        self.ammo = pygame.sprite.Group()
        self.sprite_images_run = [pygame.image.load(f'sprites/rifle/move/survivor-move_rifle_{i}.png') for i in range(0, 19)]

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






