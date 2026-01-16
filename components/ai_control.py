from pygame import Vector2
import numpy as np

from components.movement import Movement
from components.transform import Transform
from components.weapon import Weapon
from components.health import Health
from core.component import Component
from core.utils import SimpleTimer


class AIControl(Component):
    def __init__(
        self,
        targets_list=None,
        detect_radius: float = 100,
        attack_radius: float = 100,
        search_time: float = 0.2,
        default_direction: Vector2 = Vector2(0, 0),
        context=None,
    ):
        super().__init__(context)
        self.detect_radius = detect_radius
        self.attack_radius = attack_radius
        self.targets_list = targets_list
        self.search_timer = SimpleTimer(search_time)
        self.default_direction = default_direction

        self.current_target = None

        self.transform = None
        self.movement = None
        self.weapon = None

    def update(self, dt):
        # ленивое получение компонентов
        if self.transform is None:
            self.transform = self.get_component(Transform)
        if self.movement is None:
            self.movement = self.get_component(Movement)
        if self.weapon is None:
            self.weapon = self.get_component(Weapon)

        # без transform — ничего сделать нельзя (нет позиции для прицеливания)
        if not self.transform:
            return

        # нет целей — просто дефолтное движение (если есть movement)
        if not self.targets_list:
            self._move_default()
            return

        detect = self.detect_radius if self.detect_radius is not None else float("inf")

        self.search_timer.update(dt)
        if self.search_timer.is_expired:
            self._pick_target(detect)
            self.search_timer.start()

        target = self.current_target
        if target:
            target_transform = target.get_component(Transform)
            if not target_transform:
                self.current_target = None
                return

            direction = Vector2(target_transform.pos) - Vector2(self.transform.pos)
            distance_sq = direction.length_squared()

            if distance_sq > (detect ** 2):
                self.current_target = None
                if self.movement:
                    self.movement.stop()
                return

            attack_r = self._attack_radius(detect)
            if distance_sq <= (attack_r ** 2) and self.weapon:
                self.weapon.shot(target_transform.pos)
                if self.movement:
                    self.movement.stop()
            elif self.movement:
                self.movement.to_direction(direction)
        else:
            self._move_default()

    def _move_default(self):
        if not self.movement:
            return
        if self.default_direction.length_squared() > 0:
            self.movement.to_direction(self.default_direction)
        else:
            self.movement.stop()

    def _pick_target(self, detect_radius):
        self.current_target = None
        if not self.targets_list:
            return

        # порядок в targets_list задает приоритет (например, сначала юниты, потом башни)
        for targets in self.targets_list:
            for t in targets:
                if not t:
                    continue
                candidate = self._nearest_in_radius(t, detect_radius)
                if candidate is not None:
                    self.current_target = candidate
                    return

    def _nearest_in_radius(self, targets, detect_radius):
        live = [t for t in targets if getattr(t.get_component(Transform), "pos", None) is not None and t.get_component(Health).alive]
        if not live:
            return None

        self_pos = np.array(self.transform.pos, float)
        positions = np.array([t.get_component(Transform).pos for t in live], float)
        distances = np.linalg.norm(positions - self_pos, axis=1)
        mask = distances <= detect_radius
        if not np.any(mask):
            return None
        idx = np.argmin(distances[mask])
        return np.array(live)[mask][idx]

    def _attack_radius(self, fallback_detect: float) -> float:
        if self.attack_radius is not None:
            return self.attack_radius
        if self.weapon and hasattr(self.weapon, "attack_radius"):
            return float(self.weapon.attack_radius)
        return fallback_detect
