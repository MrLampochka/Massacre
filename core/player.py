from enum import Enum, auto
import random

import pygame.sprite

import config
from core.base_unit import Direction, BaseUnit
from core.utils import SimpleTimer


class PlayerSide(Enum):
    left = auto()
    right = auto()


class Player:
    def __init__(self, coins, side=PlayerSide.left):
        self.coins = coins
        self.side = side
        self.pos = config.PLAYER_FIRST_POS if side == PlayerSide.left else config.PLAYER_SECOND_POS
        self.units = pygame.sprite.Group()
        self.health = config.PLAYER_HEALTH
        self.line_surface = pygame.Surface(config.SCREEN_SIZE, pygame.SRCALPHA)
        self.coin_timer = SimpleTimer()
        self.coin_time = 100

    def add_unit(self, id_unit):
        direction = Direction.left if self.side == PlayerSide.right else Direction.right
        x, y = self.pos
        pos = x, y + random.randint(0, config.SPAWN_RANGE)
        try:
            unit = config.units_list[id_unit]
        except IndexError:
            print("Нет такого бойца!")
            return

        if self.coins >= unit["cost"]:
            self.coins -= unit["cost"]
            BaseUnit.add_unit(group=self.units, pos=pos, direction=direction, unit=config.units_list[id_unit])

    def update(self, units):
        if self.coin_timer.is_expired():
            self.coins += 1
            self.coin_timer.start(self.coin_time)
        self.units.update(units)

    def draw(self, screen):
        for u in self.units:
            u.draw_health_bar(screen)
            u.draw_ammo(self.line_surface)

        screen.blit(self.line_surface, (0, 0))





