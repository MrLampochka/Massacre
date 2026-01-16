import pygame as pg

from components.health import Health
from components.transform import Transform
from core.component import Component


class Sprite(Component):
    def __init__(self, image=None, color=(255, 0, 0), size=(32, 32), context=None):
        super().__init__(context)
        if image is None:
            image = pg.Surface(size)  # ширина, высота
            image.fill(color)

        self.image = image
        self.sprite = pg.sprite.Sprite(self.context.get("sprites", ()))
        self.sprite.image = image
        self.sprite.rect = image.get_rect()

    def on_added(self):
        self.sprite.game_object = self.game_object
        self.sprite.get_component = self.get_component

    def update(self, dt):
        if health := self.get_component(Health):
            self.sprite.image.set_alpha(max(0, int(255 * (health.dying_timer.value.ratio()))))

        if transform := self.get_component(Transform):
            self.sprite.rect.center = transform.pos

    def kill(self):
        self.sprite.kill()
