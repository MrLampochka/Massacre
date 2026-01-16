from enum import Enum, auto

from pygame import Vector2, Surface
import pygame as pg

from config.prefabs import PREFABS
from config.spawn_positions import SPAWN_POSITIONS
from components.health import Health
from components.money import Money
from core.game_object import GameObject
from entities.prefab_factory import PrefabFactory


class Player(GameObject):
    class Side(Enum):
        LEFT = auto()
        RIGHT = auto()

    def __init__(self, screen: Surface, side: Side):
        super().__init__()
        self.side = side
        self.screen = screen

        self.groups = {
            "towers": pg.sprite.Group(),
            "units": pg.sprite.Group(),
            "projectiles": pg.sprite.Group(),
            "gui": pg.sprite.Group(),
        }

        self.unit_factory = PrefabFactory(
            context={
                "screen": self.screen,
                "sprites": self.groups["units"],
                **self.groups,
            },
            prefabs=PREFABS,
        )

        self.tower_factory = PrefabFactory(
            context={
                "screen": self.screen,
                "sprites": self.groups["towers"],
                **self.groups,
            },
            prefabs=PREFABS,
        )

        self.enemies = []

    def _set_enemies(self, players):
        self.enemies = [p for p in players if isinstance(p, Player) and p is not self]
        self.collision_list = [
            group
            for e in self.enemies
            for group in [e.groups.get("towers"), e.groups.get("units")]
            if group is not None
        ]
        self.targets_list = [
            [e.groups["units"] for e in self.enemies],
            [e.groups["towers"] for e in self.enemies],
        ]

    def buy_unit(self, unit_name: str):
        money: Money = self.get_component(Money)
        cost = self.unit_factory.prefabs[unit_name].get("cost", float("inf"))

        if not (money and money.spend(cost)):
            return

        self.add_child(
            self.unit_factory.spawn(
                name=unit_name,
                components={
                    "weapon": {"collision_list": self.collision_list},
                    "transform": {"pos": Vector2(SPAWN_POSITIONS[self.side.name]["unit"].get_random())},
                    "ai_control": {
                        "targets_list": self.targets_list,
                        "default_direction": (
                            Vector2(1, 0)
                            if self.side == Player.Side.LEFT
                            else Vector2(-1, 0)
                        ),
                    },
                },
            )
        )


class ControlledPlayer(Player):
    def __init__(self, screen: Surface, side, health):
        super().__init__(screen, side)
        self.add_component(Money(100, salary=1, coin_time=0.1))
        self.add_component(Health(health))

    def set(self, players: list["Player"]):
        self._set_enemies(players)
        self._set_towers()
        self._set_unit()

    def _set_towers(self):
        tower_positions = SPAWN_POSITIONS[self.side.name]["tower"].points or []
        if health := self.get_component(Health):
            for pos in tower_positions:
                self.add_child(
                    self.tower_factory.spawn(
                        name="tower",
                        components={
                            "weapon": {"collision_list": self.collision_list},
                            "transform": {"pos": Vector2(pos)},
                            "health": {"value": health.get_value()},
                            "ai_control": {
                                "targets_list": self.targets_list,
                            },
                        },
                    )
                )

    def _set_unit(self):
        if health := self.get_component(Health):
            unit_position = SPAWN_POSITIONS[self.side.name]["unit"].get_random()

            self.add_child(
                self.unit_factory.spawn(
                    "default",
                    components={
                        "weapon": {"collision_list": self.collision_list},
                        "transform": {"pos": unit_position},
                        "health": {"value": health.get_value()},
                    },
                )
            )


class AIPlayer(Player):
    def __init__(self, screen: Surface, side, health):
        super().__init__(screen, side)
        self.add_component(Money(100, salary=1, coin_time=0.1))
        self.add_component(Health(health))

    def set(self, players: list["Player"]):
        self._set_enemies(players)
        self._set_towers()

    def _set_towers(self):
        tower_positions = SPAWN_POSITIONS[self.side.name]["tower"].points or []
        if health := self.get_component(Health):
            for pos in tower_positions:
                self.add_child(
                    self.tower_factory.spawn(
                        name="tower",
                        components={
                            "weapon": {"collision_list": self.collision_list},
                            "transform": {"pos": Vector2(pos)},
                            "health": {"value": health.get_value()},
                            "ai_control": {
                                "targets_list": self.targets_list,
                            },
                        },
                    )
                )
