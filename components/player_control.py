from typing import Optional

import pygame as pg
from pygame import Vector2

from components.weapon import Weapon
from components.movement import Movement
from core.component import Component


class PlayerControl(Component):
    def __init__(
        self,
        left_btn_cb=None,
        right_btn_cb=None,
        left_btn_hold_cb=None,
        right_btn_hold_cb=None,
        context=None,
    ):
        super().__init__(context)
        self.direction = Vector2()

        self.left_btn_cb = left_btn_cb
        self.left_btn_hold_cb = left_btn_hold_cb
        self.left_btn_pressed = False

        self.right_btn_cb = right_btn_cb
        self.right_btn_hold_cb = right_btn_hold_cb
        self.right_btn_pressed = False

        self.start_pos: Optional[Vector2] = None
        self.screen = self.context.get("screen", None)

    def event_handler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.start_pos = Vector2(event.pos) - self.screen.get_offset()
            if self.screen.get_rect().collidepoint(self.start_pos):
                if event.button == 1:  # левая кнопка
                    self.left_btn_pressed = True

                    if self.left_btn_cb:
                        self.left_btn_cb(Vector2(event.pos) - self.screen.get_offset())

                elif event.button == 3:  # правая кнопка
                    self.right_btn_pressed = True

                    if self.right_btn_cb:
                        self.right_btn_cb(Vector2(event.pos) - self.screen.get_offset())

        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:  # левая кнопка
                self.left_btn_pressed = False

            elif event.button == 3:  # правая кнопка
                self.right_btn_pressed = False

            self.start_pos = None

        keys = pg.key.get_pressed()
        x = y = 0
        if keys[pg.K_w] or keys[pg.K_UP]:
            y = -1
        if keys[pg.K_s] or keys[pg.K_DOWN]:
            y = 1
        if keys[pg.K_a] or keys[pg.K_LEFT]:
            x = -1
        if keys[pg.K_d] or keys[pg.K_RIGHT]:
            x = 1

        if movement := self.get_component(Movement):
            movement.to_direction(Vector2(x, y))

    def update(self, dt):
        if self.left_btn_pressed:
            if callback := self.left_btn_hold_cb or self.get_component(Weapon).shot:
                callback(Vector2(pg.mouse.get_pos()) - self.screen.get_offset())

        if self.right_btn_hold_cb and self.right_btn_pressed:
            self.right_btn_hold_cb(Vector2(pg.mouse.get_pos()) - self.screen.get_offset())

    def draw(self, screen):
        if self.right_btn_pressed:
            mouse_pos = Vector2(pg.mouse.get_pos()) - self.screen.get_offset()
            x1, y1 = self.start_pos
            x2, y2 = mouse_pos
            rect = pg.Rect(
                Vector2(min(x1, x2), min(y1, y2)), Vector2(abs(x2 - x1), abs(y2 - y1))
            )
            pg.draw.rect(screen, (0, 255, 0), rect, 1)
