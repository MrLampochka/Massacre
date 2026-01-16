from random import random, randint
from typing import overload

import pygame
from pygame.math import Vector2

from core.utils import SmoothMovementMixin


class Ball(pygame.sprite.Sprite, SmoothMovementMixin):
    def __init__(self, pos, radius):
        super().__init__()
        self.radius = radius
        self.pos = pos
        self.image = pygame.Surface((2*self.radius,) * 2, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

        pygame.draw.circle(self.image, (255, 200, 0), (self.radius, self.radius), self.radius)
        self.k_friction = 0.9
        self.dragging = False
        self.speed = 5.0
        self.velocity = Vector2(0, 0)


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.dragging = True
                self.pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.pos = event.pos
                v = Vector2(self.pos) - Vector2(self.rect.centerx, self.rect.centery)
                n = v.normalize() if v.length() > 0 else Vector2(0, 1)
                self.velocity = n * self.speed * v.length()

    def update(self, screen_rect, dt):

        if not self.dragging:
            self.pos += self.velocity * dt * self.speed

        if self.x - self.radius < 0:  # левая граница
            self.x = self.radius
            self.velocity.x *= -1
        elif self.x + self.radius > screen_rect.width:  # правая граница
            self.x = screen_rect.width - self.radius
            self.velocity.x *= -1

        if self.y - self.radius < 0:  # верхняя граница
            self.y = self.radius
            self.velocity.y *= -1
        elif self.y + self.radius > screen_rect.height:  # нижняя граница
            self.y = screen_rect.height - self.radius
            self.velocity.y *= -1

        if self.velocity.length() > 1.0:
            self.velocity *= self.k_friction ** dt
        else:
            self.velocity = Vector2(0, 0)

        self.rect.center = self.pos

    @staticmethod
    def resolve_collision(dt, ball1, ball2):
        if ball1 == ball2:
            return False

        if not pygame.sprite.collide_circle(ball1, ball2):
            return False
        if hasattr(ball1, "health") and hasattr(ball2, "health"):
            if not (ball1.health.alive and ball2.health.alive):
                return False

        delta = Vector2(ball2.rect.center) - Vector2(ball1.rect.center)
        distance = delta.length()

        if distance == 0:
            # if hasattr(ball1, "movement"):
            #     ball1.movement.pos -= Vector2(0,randint(0, 2))
            # else:
            #     ball1.pos -= Vector2(0, randint(0, 2))
            # if hasattr(ball2, "movement"):
            #     ball2.movement.pos += Vector2(0,randint(0, 2))
            # else:
            #     ball2.pos += Vector2(0,randint(0, 2))
            delta = Vector2(0.1, 0.1)
            distance = delta.length()


        # Нормализованный вектор направления столкновения
        n = delta / distance
        if hasattr(ball1, "velocity") and hasattr(ball2, "velocity"):
            # Проекция скоростей на нормаль
            v1n = ball1.velocity.dot(n)
            v2n = ball2.velocity.dot(n)

            # Обновляем скорости по нормали (упругое столкновение)
            # ball1.velocity += (v2n - v1n) * n
            # ball2.velocity += (v1n - v2n) * n

            # Абсолютно неупругое направление
            v_common = (v1n + v2n) / 2
            restitution = 0.5
            ball1.velocity += ((v2n - v1n) * restitution + (v_common - v1n) * (1 - restitution)) * n
            ball2.velocity += ((v1n - v2n) * restitution + (v_common - v2n) * (1 - restitution)) * n

        # Раздвигаем шары, чтобы не залипли
        overlap = (ball1.radius + ball2.radius - distance) / 2
        max_push = 3  # максимально сдвиг за кадр
        push = min(overlap, max_push)
        if overlap > 1:
            if hasattr(ball1, "position"):
                ball1.position.pos -= n * push * dt
                # ball1.position.velocity -= n * overlap * 1
            else:
                ball1.pos -= n * push * 0.6

            # if hasattr(ball2, "position"):
            #     ball2.position.pos += n * push
            # else:
            #     ball2.pos += n * push

        return True


class Hole(pygame.sprite.Sprite):
    def __init__(self, pos, radius=20):
        super().__init__()
        self.radius = radius

        # Create circular surface with transparency
        diameter = radius * 2
        self.image = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 0, 0), (radius, radius), radius)

        self.rect = self.image.get_rect(center=pos)

    def is_ball_inside(self, ball):
        # Checks if ball center is inside the hole circle
        hole_center = pygame.math.Vector2(self.rect.center)
        ball_center = pygame.math.Vector2(ball.rect.center)

        return hole_center.distance_to(ball_center) < self.radius
