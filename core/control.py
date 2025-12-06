import pygame
from pygame import Vector2

from core.units import NotBaseUnit


class SpriteControl:
    def __init__(self, unit: NotBaseUnit, click_1=None, click_2=None):
        self.unit = unit
        self.direction = Vector2()
        self.btn_1_click = click_1
        self.btn_2_click = click_2
        self.btn_1_clicked = False

    def handler(self, event, start, stop):
        if event.type == pygame.QUIT:
            stop()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                stop()
            if event.key == pygame.K_r:
                start()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # левая кнопка
                self.btn_1_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # левая кнопка
                self.btn_1_clicked = False

        keys = pygame.key.get_pressed()
        x = y = 0

        if keys[pygame.K_w]:
            y = -1
        if keys[pygame.K_s]:
            y = 1
        if keys[pygame.K_a]:
            x = -1
        if keys[pygame.K_d]:
            x = 1
        if self.unit.health.alive:
            self.unit.position.move_direction(Vector2(x, y))

    def update(self, dt):
        if self.unit.health.alive:
            if self.btn_1_clicked:
                self.btn_1_click(Vector2(pygame.mouse.get_pos()))

