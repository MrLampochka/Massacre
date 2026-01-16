import pygame as pg

from core.component import Component
from components.sprite import Sprite
from components.health import Health


class Collision(Component):
    def __init__(
        self,
        collision_list=None,
        on_collision=None,
        kill_self: bool = False,
        first_only: bool = False,
        context=None,
    ):
        super().__init__(context)

        self.collision_list = collision_list or []
        self.on_collision = on_collision
        self.kill_self = kill_self
        self.first_only = first_only

    def update(self, dt):
        if not self.on_collision:
            return

        if owner_sprite := self.get_component(Sprite):
            for group in self.collision_list:
                hits = pg.sprite.spritecollide(owner_sprite.sprite, group, False)

                if not hits:
                    continue

                collide = False
                for h in hits:
                    if self.on_collision(h):
                        collide = True
                        if self.first_only:
                            break

                if self.kill_self and collide:
                    self.game_object.kill()

