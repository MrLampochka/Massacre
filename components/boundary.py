import pygame as pg
from pygame import Vector2

from components.transform import Transform
from core.component import Component


class BoundaryKill(Component):
    def __init__(self, rect: pg.Rect = None, padding=0, context=None):
        super().__init__(context)
        self.rect = rect or (context.get("screen").get_rect() if context.get("screen") else None)
        self.rect = self.rect.inflate(padding * 2, padding * 2) if self.rect else None

    def update(self, dt):
        tr = self.get_component(Transform)
        if self.rect and tr and not self.rect.collidepoint(tr.pos):
            self.game_object.kill()


class BoundaryClamp(Component):
    def __init__(self, rect: pg.Rect = None, padding=0, context=None):
        super().__init__(context)
        self.rect = rect or (context.get("screen").get_rect() if context.get("screen") else None)
        self.rect = self.rect.inflate(padding * 2, padding * 2) if self.rect else None

    def update(self, dt):
        tr = self.get_component(Transform)
        if self.rect and tr:
            clamped_x = min(max(tr.pos.x, self.rect.left), self.rect.right)
            clamped_y = min(max(tr.pos.y, self.rect.top), self.rect.bottom)
            if clamped_x != tr.pos.x or clamped_y != tr.pos.y:
                tr.pos = Vector2(clamped_x, clamped_y)
