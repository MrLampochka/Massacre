import random
from enum import Enum, auto
from typing import Any

import pygame.sprite
from pygame import Vector2, Surface
from pygame.sprite import Group, Sprite

import config
from core.components import HealthComponent, Projectile

from core.units import NotBaseUnit, Tower, BaseUnit
from core.utils import SimpleTimer


class BasePlayer:
    class Side(Enum):
        LEFT = auto()
        RIGHT = auto()

    def __init__(
        self,
        side: Side,
        health=100000,
        units=None,
        towers=None,
        projectiles=None,
        field_rect=None,
        coin_time=0.5,
        start_coin=100,
        enemy: "BasePlayer" = None,
    ):
        self.side = side

        self.health = HealthComponent(None, health)
        self.bars = pygame.sprite.Group()
        self.units = units or pygame.sprite.Group()
        self.towers = towers or pygame.sprite.Group()
        self.projectiles = projectiles or pygame.sprite.Group()

        self.field_rect = field_rect

        self.coins = start_coin
        self.coin_timer = SimpleTimer(coin_time).start()

        self.enemy = enemy

    def set(self, screen: Surface):
        if self.side == self.Side.LEFT:
            positions = [200, 325, 450]
            x = 70 + config.GUI_PADDING
        elif self.side == self.Side.RIGHT:
            positions = [200, 325, 450]
            x = screen.get_rect().width - 70 - config.GUI_PADDING
        else:
            return  # на всякий случай

        # создаём башни и присваиваем health
        for y in positions:
            tower = Tower((x, y), 30, targets_list=self.enemy.targets_list, projectiles=self.projectiles, damage= 5, reload_time=0.05)
            tower.health = HealthComponent(tower, self.health.value, dying_time=1)
            self.towers.add(tower)


    def update(self, dt):
        self._update_coin(dt)
        self.units.update(dt)
        self.health.update(dt)
        self.towers.update(dt)
        self.projectiles.update(dt)
        self.bars.update(dt)

    def draw(self, screen):
        self.towers.draw(screen)
        self.units.draw(screen)
        self.projectiles.draw(screen)
        self.bars.draw(screen)

    def _update_coin(self, dt):
        if self.health.alive:
            self.coin_timer.update(dt)
            if self.coin_timer.is_expired:
                self.coins += 1
                self.coin_timer.start()

    @property
    def targets_list(self) -> list[Group[Sprite | Any] | Any]:
        return [self.units, self.towers]

    @staticmethod
    def shot(unit, target_pos, player: "BasePlayer", field_rect=None):
        Projectile(
            unit=unit,
            projectiles=player.projectiles,
            damage=3,
            target_pos=target_pos,
            targets_list=player.enemy.targets_list,
            field_rect=field_rect,
            speed=500,
        )


class HumanPlayer(BasePlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set(self, screen: Surface):
        super().set(screen)
        self.units.add(
            NotBaseUnit(
                (400, 400),
                10,
                1000,
                health=100,
                bars=self.bars,
                targets_list=self.enemy.targets_list,
                projectiles=self.projectiles,
            )
        )
        self.units.add(
            NotBaseUnit(
                (500, 400),
                10,
                100,
                damage=25,
                health=100,
                bars=self.bars,
                targets_list=self.enemy.targets_list,
                projectiles=self.projectiles,
                default_direction=Vector2(1,0)
            )
        )

        # self.units.add(
        #     BaseUnit(
        #         (500, 400),
        #         10,
        #         (50, 100, 200),
        #     )
        # )


    def update(self, dt):
        super().update(dt)


class BotPlayer(BasePlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auto_gen_timer = SimpleTimer(1).start()

    def update(self, dt):
        super().update(dt)
        if self.auto_gen_timer and self.health.alive:
            self.auto_gen_timer.update(dt)

            if self.auto_gen_timer.is_expired:
                unit = NotBaseUnit(
                    (random.randint(500, 700), random.randint(300, 400)),
                    10,
                    100,
                    bars=self.bars,
                    health=100,
                    damage=25,
                    targets_list=self.enemy.targets_list,
                    default_direction=Vector2(-1, 0),
                    projectiles=self.projectiles,
                )
                self.units.add(unit)
                self.auto_gen_timer.start(random.random()/3)

    # def set(self):
    #     for i in range(0, 1):
    #         unit = BaseUnit(
    #             (random.randint(500, 700), random.randint(300, 400)),
    #             10,
    #             100,
    #             bars=self.bars,
    #             health=100,
    #             damage=25,
    #             targets_list=self.enemy.targets_list,
    #             default_direction=Vector2(-1, 0),
    #             projectiles=self.projectiles,
    #         )
    #         self.units.add(unit)
