from enum import Enum

import numpy as np
import pygame as pg
from pygame import Vector2

from components.health import Health
from components.transform import Transform
from config.prefabs import PREFABS
from core.component import Component
from core.game_object import GameObject
from core.utils import Timer


class Weapon(Component):
    def __init__(self, reload_time=1, collision_list=None, attack=None, context=None):
        super().__init__(context)
        self.gun: GameObject | None = None
        self.reload_timer = Timer(reload_time)
        self.attacking = False
        self.attack = build_attack(context=self.context, **(attack or {}), collision_list=collision_list)

    def on_added(self):
        self.gun: GameObject = self.game_object

    def shot(self, target_pos: Vector2):
        if self.gun is None or not self.get_component(Health).alive:
            return
        self.attacking = True
        if self.reload_timer.is_expired and self.attack and callable(self.attack):
            self.attack(self, target_pos)

        if not self.reload_timer.running:
            self.reload_timer.start()

    def update(self, dt):
        self.reload_timer.update(dt)

        if self.attack and hasattr(self.attack, "update"):
            self.attack.update(dt)

        if not self.attacking:
            self.reload_timer.stop()

        self.attacking = False

    def draw(self, screen):
        if self.attack and hasattr(self.attack, "draw"):
            self.attack.draw(screen)

    def get_value(self):
        return self.reload_timer.value


def _iter_targets(collision_list):
    if not collision_list:
        return
    for group in collision_list:
        for sprite in group:
            target = getattr(sprite, "game_object", None)
            if not target:
                continue
            th = target.get_component(Health)
            tt = target.get_component(Transform)
            if th and th.alive and tt:
                yield th, tt


def _spread_direction(spread: float, direction: Vector2) -> Vector2:
    if spread and direction.length_squared() > 0:
        spread_angle = np.radians(np.random.uniform(-spread, spread))
        return direction.rotate_rad(spread_angle).normalize()
    return direction


class AttackType(Enum):
    MELEE = "melee"
    PROJECTILE = "projectile"
    EXPLOSIVE = "explosive"
    RAY = "ray"


class AttackBase:
    weapon = None  # will be injected by Weapon

    def __call__(self, weapon, target_pos: Vector2):
        raise NotImplementedError

    def update(self, dt):
        pass

    def draw(self, screen):
        pass


class MeleeAttack(AttackBase):
    def __init__(self, collision_list, damage, attack_radius):
        self.collision_list = collision_list
        self.damage = damage
        self.attack_radius = attack_radius

    def __call__(self, weapon, target_pos: Vector2):
        if self.attack_radius is None or not weapon or not weapon.gun:
            return

        gun_transform = weapon.gun.get_component(Transform)
        if not gun_transform:
            return
        # TODO: add optimize find nearest target via numpy and matrix
        best = None
        best_dist_sq = float(self.attack_radius) ** 2
        for th, tt in _iter_targets(self.collision_list):
            dist_sq = (tt.pos - gun_transform.pos).length_squared()
            if dist_sq <= best_dist_sq:
                best_dist_sq = dist_sq
                best = th
        if best:
            best.take_damage(self.damage)


class ProjectileAttack(AttackBase):
    def __init__(self, bullet_name, group, screen, collision_list, spread, damage):
        self.bullet_name = bullet_name
        self.group = group
        self.screen = screen
        self.collision_list = collision_list
        self.spread = spread
        self.damage = damage

    def __call__(self, weapon, target_pos: Vector2):

        if not weapon or not weapon.gun:
            return

        gun_transform = weapon.gun.get_component(Transform)
        if not gun_transform:
            return

        # lazy import to avoid circular dependency with Weapon
        from entities.prefab_factory import PrefabFactory

        direction = _spread_direction(self.spread, target_pos - gun_transform.pos)
        bullet = PrefabFactory(context={"screen": self.screen, "sprites": self.group}, prefabs=PREFABS).spawn(
            name=self.bullet_name,
            components={
                "transform": {"pos": gun_transform.pos},
                "movement": {"direction": direction},
                "collision": {
                    "collision_list": self.collision_list,
                    "on_collision": self._collision_callback(),
                },
            },
        )
        weapon.gun.add_child(bullet)

    def _collision_callback(self):
        return lambda hit: self._direct_damage(hit)

    def _direct_damage(self, hit):
        target = getattr(hit, "game_object", None)
        if not target:
            return False
        if health := target.get_component(Health):
            return health.take_damage(self.damage)
        return False


class ExplosiveProjectileAttack(ProjectileAttack):
    def __init__(
        self,
        bullet_name,
        group,
        screen,
        collision_list,
        spread,
        damage,
        explosion_radius=None,
        explosion_damage=None,
    ):
        super().__init__(bullet_name, group, screen, collision_list, spread, damage)
        self.explosion_radius = explosion_radius
        self.explosion_damage = explosion_damage or damage

    def _collision_callback(self):
        return lambda hit: self._explode_at(self._hit_position(hit))

    @staticmethod
    def _hit_position(hit):
        target = getattr(hit, "game_object", None)
        if target and (transform := target.get_component(Transform)):
            return Vector2(transform.pos)
        if hasattr(hit, "rect"):
            return Vector2(hit.rect.center)
        return Vector2()

    def _explode_at(self, center: Vector2):
        if self.explosion_radius is None or not self.collision_list:
            return True

        radius_sq = float(self.explosion_radius) ** 2
        damaged = False
        for th, tt in _iter_targets(self.collision_list):
            if (Vector2(tt.pos) - center).length_squared() <= radius_sq:
                if th.take_damage(self.explosion_damage):
                    damaged = True
        return damaged


class RayAttack(AttackBase):
    def __init__(
        self,
        collision_list,
        damage,
        ray_length=400,
        ray_width=4,
        ray_draw_time=0.08,
        ray_color=(255, 0, 0),
        spread=0,
    ):
        self.collision_list = collision_list
        self.damage = damage
        self.ray_length = ray_length
        self.ray_width = ray_width
        self.ray_color = ray_color
        self.ray_timer = Timer(ray_draw_time)

        self.last_ray = None
        self.spread = spread

    def __call__(self, weapon, target_pos: Vector2):
        if not weapon or not weapon.gun:
            return

        gun_transform = weapon.gun.get_component(Transform)
        if not gun_transform:
            return

        start = Vector2(gun_transform.pos)
        direction = Vector2(target_pos) - start
        if direction.length_squared() == 0:
            return

        max_len = float(self.ray_length)
        direction_norm = direction.normalize()
        default_end = start + direction_norm * min(max_len, direction.length())

        hits = []
        radius_tol = self.ray_width * 0.5
        for th, tt in _iter_targets(self.collision_list):
            to_target = Vector2(tt.pos) - start
            proj = to_target.dot(direction_norm)
            if proj < 0 or proj > max_len:
                continue
            per = to_target - direction_norm * proj
            if per.length() <= radius_tol:
                hits.append((proj, th, Vector2(tt.pos)))

        hits.sort(key=lambda h: h[0])
        if not hits:
            self._store_ray(start, default_end)
            return

        damage_left = self.damage
        end_pos = start + direction_norm * max_len
        for _, health, pos in hits:
            if damage_left <= 0:
                end_pos = pos
                break
            dealt = min(damage_left, health.value.current)
            if health.take_damage(dealt):
                damage_left -= dealt
            end_pos = pos
            if damage_left <= 0:
                break

        self._store_ray(start, end_pos)

    def _store_ray(self, start, end):
        self.last_ray = (Vector2(start), Vector2(end))
        if self.ray_timer:
            self.ray_timer.start()

    def update(self, dt):
        if self.ray_timer:
            self.ray_timer.update(dt)
            if self.ray_timer.is_expired:
                self.last_ray = None

    def draw(self, screen):
        if self.last_ray and self.ray_timer and not self.ray_timer.is_expired:
            start, end = self.last_ray
            alpha_ratio = self.ray_timer.value.ratio() if self.ray_timer.value else 0
            if alpha_ratio <= 0:
                return
            color = (*self.ray_color[:3], int(255 * alpha_ratio))
            surface = pg.Surface(screen.get_size(), pg.SRCALPHA)
            pg.draw.line(surface, color, start, end, self.ray_width)
            screen.blit(surface, (0, 0))


def build_attack(context, **kwargs):
    """Factory to keep backward compatibility with config dicts."""
    if not kwargs:
        return None

    damage = kwargs.get("damage", 0)
    spread = kwargs.get("spread", 0)
    collision_list = kwargs.get("collision_list", [])
    attack_type = kwargs.get("type")

    if attack_type == AttackType.RAY.value:
        return RayAttack(
            collision_list=collision_list,
            damage=damage,
            ray_length=kwargs.get("ray_length", 400),
            ray_width=kwargs.get("ray_width", 4),
            ray_draw_time=kwargs.get("ray_draw_time", 0.08),
            ray_color=kwargs.get("ray_color", (255, 0, 0)),
        )
    elif attack_type == AttackType.MELEE.value:
        return MeleeAttack(
            collision_list=collision_list,
            damage=damage,
            attack_radius=kwargs.get("attack_radius"),
        )
    elif attack_type == AttackType.EXPLOSIVE.value:
        return ExplosiveProjectileAttack(
            bullet_name=kwargs.get("bullet_name"),
            group=context.get("projectiles", None),
            screen=context.get("screen", None),
            collision_list=collision_list,
            spread=spread,
            damage=damage,
            explosion_radius=kwargs.get("explosion_radius"),
            explosion_damage=kwargs.get("explosion_damage"),
        )
    elif attack_type == AttackType.PROJECTILE.value:
        return ProjectileAttack(
            bullet_name=kwargs.get("bullet_name"),
            group=context.get("projectiles", None),
            screen=context.get("screen", None),
            collision_list=collision_list,
            spread=spread,
            damage=damage,
        )
    else:
        return None
