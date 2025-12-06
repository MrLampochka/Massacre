from pygame import Vector2
import pygame as pg

from core.components import BarComponent, HealthComponent, PositionComponent, BotMovementComponent, TargetingComponent, \
    WeaponComponent
from core.utils import SV


class BaseUnit(pg.sprite.Sprite):
    def __init__( self, pos, radius, color=(0, 255, 0)):
        super().__init__()
        self.radius = radius
        self.image = pg.Surface((2 * self.radius,) * 2, pg.SRCALPHA)
        pg.draw.circle(self.image, color, (self.radius,) * 2, self.radius)
        self.rect = self.image.get_rect(center=pos)

        self.components = []

    def update(self, dt):
        for component in self.components:
            component.update(dt)


class NotBaseUnit(pg.sprite.Sprite):
    def __init__(
        self,
        pos,
        radius=40,
        speed=10,
        color=(0, 255, 0),
        health=None,
        targets_list=None,
        bars=None,
        projectiles=None,
        projectile_speed=1000,
        reload_time=1.0,
        damage=10,
        default_direction=None,
        attack_radius=300,
        targeting_radius=400,
    ):
        super().__init__()
        self.radius = radius
        self.image = pg.Surface((2 * self.radius,) * 2, pg.SRCALPHA)
        pg.draw.circle(self.image, color, (self.radius,) * 2, self.radius)
        self.rect = self.image.get_rect(center=pos)


        self.position = PositionComponent(self, speed)
        self.health = HealthComponent(self, health, 1)
        self.targeting = TargetingComponent(self, targets_list, targeting_radius)
        self.bot_movement = BotMovementComponent(self, default_direction) if default_direction else None
        self.weapon = WeaponComponent(self, damage, reload_time, projectiles, projectile_speed, attack_radius)
        # self.ai = AIComponent(self, default_direction)
        self.health_bar = BarComponent(self, bars, self.health.value, (255, 0, 0), Vector2(0, -15))
        self.reload_bar = BarComponent(self, bars, self.weapon.value, (255, 128, 0), Vector2(0, -10))

        self.components = [
            self.targeting,
            self.health,
            self.position,
            self.weapon,
            self.bot_movement,
            self.health_bar,
            self.reload_bar
        ]

    def update(self, dt):
        # for component in self.components:
        #     component.update(dt)

        self.targeting.update(dt)
        self.health.update(dt)
        self.position.update(dt)
        self.weapon.update(dt)

        if self.bot_movement:
            self.bot_movement.update(dt)


class Tower(NotBaseUnit):
    def __init__(
        self,
        pos,
        radius=50,
        color=(100, 100, 255),
        health=SV(300),
        **kwargs
    ):
        super().__init__(
            pos,
            radius=radius,
            speed=0,
            color=color,
            health=health,
            attack_radius=600,
            targeting_radius=600,
            **kwargs,
        )


