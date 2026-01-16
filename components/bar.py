import pygame as pg
from pygame import Vector2

from components.health import Health
from components.transform import Transform
from core.component import Component


class Bar(Component):
    def __init__(
        self,
        source=None,
        color=(128, 128, 128),
        offset: Vector2 = Vector2(0, 0),
        size=(20, 5),
        bg_color=(64, 64, 64),
        rev=False,
        context=None,
    ):
        super().__init__(context)
        image = pg.Surface(size, pg.SRCALPHA)
        image.fill(color)

        self.image = image
        self.sprite = pg.sprite.Sprite(self.context.get("gui", None))
        self.sprite.image = self.image
        self.sprite.rect = self.image.get_rect()
        self.source = source

        self.color = color
        self.bg_color = bg_color
        self.offset = offset
        self.rev = rev

    def on_added(self):
        self.sprite.game_object = self.game_object
        self.sprite.get_component = self.get_component


    def update(self, dt):
        if health := self.get_component(Health):
            if not health.alive:
                self.sprite.image.set_alpha(max(0, int(255 * (health.dying_timer.value.ratio()))))

        if source := self.get_component_by_name(self.source):
            if transform := self.get_component(Transform):
                if value := getattr(source, "get_value", None):
                    value = value()
                    self.sprite.image.fill(self.bg_color)
                    w, h = self.image.get_size()
                    pg.draw.rect(
                        self.image, self.color, (0, 0, w * value.ratio(self.rev), h)
                    )
                    self.sprite.rect.midbottom = transform.pos + self.offset



    def kill(self):
        self.sprite.kill()
