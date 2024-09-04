from enum import Enum, auto
import random

import pygame.sprite

import config
from core.unit import Direction, BaseUnit, Tower
from core.utils import SimpleTimer


class PlayerSide(Enum):
    left = auto()
    right = auto()


class Player:
    def __init__(self, side, coins, coin_time):
        self.side = side
        self.coins = coins
        self.coin_time = coin_time
        self.direction = Direction.left if self.side == PlayerSide.right else Direction.right
        self.pos = config.PLAYER_FIRST_POS if side == PlayerSide.left else config.PLAYER_SECOND_POS
        self.units = pygame.sprite.Group()
        self.health = self.max_health = config.PLAYER_HEALTH
        self.line_surface = pygame.Surface(config.SCREEN_SIZE, pygame.SRCALPHA)
        self.coin_timer = SimpleTimer()
        self.x, self.y = self.pos

        self.tower = Tower(self.units, (self.x, self.y + 200), self.direction,
                           size=(100, 100),
                           damage=10,
                           health=self.health,
                           reload_time=1000,
                           speed=0,
                           attack_radius=1000,
                           visible_radius=config.VISIBLE_RADIUS,
                           sound=config.PUNCH_SOUND,
                           )
    def add_unit(self, id_unit):

        x, y = self.pos
        pos = x, y + random.randint(0, config.SPAWN_RANGE)
        try:
            unit = config.units_list[id_unit]
        except IndexError:
            print("Нет такого бойца!")
            return

        if self.coins >= unit["cost"]:
            self.coins -= unit["cost"]
            BaseUnit.add_unit(group=self.units, pos=pos, direction=self.direction, unit=config.units_list[id_unit])

    def update(self, units):
        self.health = self.tower.health
        self.update_coin()
        self.units.update(units)

    def update_coin(self):
        if self.coin_timer.is_expired():
            self.coins += 1
            self.coin_timer.start(self.coin_time)


    def draw(self, screen):
        for u in self.units:
            u.draw_health_bar(screen)
            u.draw_ammo(self.line_surface)

        screen.blit(self.line_surface, (0, 0))





