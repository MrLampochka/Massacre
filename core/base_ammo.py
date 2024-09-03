import math

import pygame.sprite


class BaseAmmo(pygame.sprite.Sprite):
    def __init__(self, group, pos, target_pos, damage, color, size):
        super().__init__(group)
        self.pos = self.x, self.y = pos
        self.damage = damage
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(color)
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
