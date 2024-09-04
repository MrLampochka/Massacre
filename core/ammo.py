import math

import pygame.draw
import pygame.sprite

import config
from core.utils import SimpleTimer


class BaseAmmo(pygame.sprite.Sprite):
    def __init__(self, group, pos, target_pos, damage, color, size):
        super().__init__(group)
        self.pos = self.x, self.y = pos
        self.damage = damage
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        # self.image.fill(color)
        pygame.draw.circle(self.image, color, (size[0]/2, size[0]/2), size[0]/2)  # Рисуем круг
        self.rect = self.image.get_rect(center=pos)
        self.target_pos = target_pos
        self._speed = 10
        self._angle = math.atan2(target_pos[0] - self.x, target_pos[1] - self.y)

    def update(self, targets):
        for target in targets:
            if self.rect.colliderect(target.rect) and target.alive:
                target.get_damage(self.damage)
                self.kill()
                return

        self.move_towards_target()

    def move_towards_target(self):
        dx, dy = self.target_pos[0] - self.rect.x, self.target_pos[1] - self.rect.y
        distance = math.hypot(dx, dy)

        if distance < 5000:
            self.x += math.sin(self._angle) * self._speed
            self.y += math.cos(self._angle) * self._speed
            self._update_position()
        else:
            self.kill()

    def _update_position(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)


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
