from abc import ABC, abstractmethod

import numpy as np
import pygame as pg
from pygame import Vector2
from pygame.sprite import Sprite

from core.utils import SV, SimpleTimer, SmoothMovementMixin

class Component(ABC):
    def __init__(self, unit):
        self.unit = unit

    @abstractmethod
    def update(self, dt):
        pass

class BarComponent(Component, pg.sprite.Sprite):
    def __init__(self, unit, bars, value: SV, color, offset: Vector2, size=(20, 5)):
        Component.__init__(self, unit)
        pg.sprite.Sprite.__init__(self)
        if bars is not None:
            bars.add(self)

        self.image = pg.Surface(size, pg.SRCALPHA)
        self.rect = self.image.get_rect()
        self.value = value
        self.color = color
        self.offset = offset

    def update(self, dt):
        if not self.unit.health.alive:
            self.kill()

        self.image.fill((0, 0, 0))
        w, h = self.image.get_size()
        pg.draw.rect(self.image, self.color, (0, 0, w * self.value.ratio, h))
        self.rect.midbottom = self.unit.rect.midtop + self.offset


class HealthComponent(Component):
    def __init__(self, unit, health, dying_time=1, dying_speed=2):
        super().__init__(unit)

        self.value = health if isinstance(health, SV) else SV(health)
        self.alive = True
        self._dying_timer = SimpleTimer(dying_time) if dying_time else None
        self.dying_speed = dying_speed

    def update(self, dt):
        if not self.alive:
            if self.unit:
                if not self._dying_timer.is_expired:
                    self._dying_timer.update(dt)
                    self.unit.image.set_alpha(
                        max(0, int(255 * (1 - self._dying_timer.ratio)))
                    )
                    self.unit.position.pos += Vector2(0, -self.dying_speed / 10)
                    return
                self.unit.kill()

        elif self.value.current == 0:
            self.alive = False
            self.unit.position.stop_move()
            if self._dying_timer:
                self._dying_timer.start()

    def take_damage(self, amount):
        if not self.alive:
            return
        self.value.current = max(0, self.value.current - amount)


class PositionComponent(Component, SmoothMovementMixin):
    def __init__(self, unit, speed):
        Component.__init__(self, unit)
        SmoothMovementMixin.__init__(self, unit.rect.center)
        self.rect = unit.rect
        self.speed = speed
        self.velocity = Vector2()
        self.unit = unit

    def move_direction(self, direction: Vector2):
        if direction.length_squared() > 0:  # предотвращаем деление на ноль
            self.velocity = direction.normalize() * self.speed
        else:
            self.stop_move()

    def move_to_target(self, target):
        direction = Vector2(target.position.pos) - Vector2(self.unit.position.pos)
        self.move_direction(direction)

    def stop_move(self):
        self.velocity = Vector2(0, 0)

    def update(self, dt):
        self.rect.center = self.pos = self.pos + self.velocity * dt


class AIComponent(Component):
    def __init__(self, unit):
        super().__init__(unit)
        self.default_direction = Vector2(-1, 1)

    def update(self, dt):
        if hasattr(self.unit, "health"):
            if not self.unit.health.alive:
                return

        if hasattr(self.unit, "targeting"):
            if target := self.unit.targeting.current_target:
                if self.unit.weapon.shooting:
                    self.unit.position.stop_move()
                else:
                    self.unit.position.move_to_target(target)
            else:
                self.unit.position.move_direction(self.default_direction)

            direction = Vector2(target.position.pos) - Vector2(self.unit.position.pos)
            if direction.length_squared() < self.unit.weapon.radius ** 2:
                return


class BotMovementComponent(Component):
    def __init__(self, unit, default_direction):
        super().__init__(unit)
        self.default_direction = default_direction

    def update(self, dt):
        if hasattr(self.unit, "health"):
            if not self.unit.health.alive:
                return

        if hasattr(self.unit, "targeting"):
            if target := self.unit.targeting.current_target:
                if self.unit.weapon.shooting:
                    self.unit.position.stop_move()
                else:
                    self.unit.position.move_to_target(target)
            else:
                self.unit.position.move_direction(self.default_direction)


class TargetingComponent:
    def __init__(self, unit, targets_list, radius, search_time=0.1):
        self.current_target = None
        self.unit = unit
        self.targets_list = targets_list
        self.radius = radius
        self.search_time = search_time
        self.search_timer = SimpleTimer(self.search_time)

    def update(self, dt):
        if not self.targets_list:
            return

        self.search_timer.update(dt)
        if not self.search_timer.is_expired:
            return

        for targets in self.targets_list:
            found = self._get_alive_targets_in_radius(targets)

            if found is not None:
                if self.current_target and self.current_target in found:
                    break

                self.current_target = self._get_alive_target_in_radius(found)
                break
        else:
            self.current_target = None

        self.search_timer.start(self.search_time)


    def _get_alive_target_in_radius(self, targets):
        if targets is None or len(targets) == 0:
            return None

        unit_pos = np.array(self.unit.rect.center, float)
        positions = np.array([t.rect.center for t in targets], float)
        distances = np.linalg.norm(positions - unit_pos, axis=1)

        nearest_index = np.argmin(distances)
        return targets[nearest_index]

    def _get_alive_targets_in_radius(self, targets):
        if not targets:
            return None

        live = [t for t in targets if t.health.alive]
        if not live:
            return None

        unit_pos = np.array(self.unit.rect.center, float)
        positions = np.array([t.rect.center for t in live], float)
        distances = np.linalg.norm(positions - unit_pos, axis=1)
        mask = distances <= self.radius

        return np.array(live)[mask] if np.any(mask) else None


class WeaponNewComponent:
    def __init__(
        self,
        unit,
        damage,
        reload_time,
        projectiles,
        projectile_speed,
        radius,
    ):
        self.damage = damage
        self.reload_time = reload_time
        self.reload_timer = SimpleTimer(reload_time)
        self.value = SV(0)
        self.unit = unit
        self.projectiles = projectiles
        self.projectile_speed = projectile_speed
        self.shooting = False
        self.radius = radius

    def shot(self, target_pos):
        if target_pos is None:
            return

        if not self.reload_timer.running:
            self.reload_timer.start(self.reload_time)

        if self.reload_timer.is_expired:
            self.projectiles.add(
                Projectile(
                    unit=self.unit,
                    projectiles=self.projectiles,
                    damage=self.damage,
                    target_pos=target_pos,
                    speed=self.projectile_speed,
                    targets_list=self.unit.targeting.targets_list

                )
            )
            self.reload_timer.stop()

    def update(self, dt):
        self.value.assign(self.reload_timer.ratio, 1)
        self.reload_timer.update(dt)


class WeaponComponent:
    def __init__(
        self,
        unit,
        damage,
        reload_time,
        projectiles,
        projectile_speed,
        radius,
    ):
        self.damage = damage
        self.reload_time = reload_time
        self.reload_timer = SimpleTimer(reload_time)
        self.value = SV(0)
        self.unit = unit
        self.projectiles = projectiles
        self.projectile_speed = projectile_speed
        self.shooting = False
        self.radius = radius
        self.spread = 3

    def shot(self, target_pos):
        if target_pos is None:
            return

        # spread
        direction = target_pos - self.unit.position.pos
        if direction.length_squared() > 0:
            spread_angle = np.radians(np.random.uniform(-self.spread, self.spread))
            direction = direction.rotate_rad(spread_angle).normalize()
        else:
            direction = Vector2()



        self.projectiles.add(
            Projectile(
                unit=self.unit,
                projectiles=self.projectiles,
                damage=self.damage,
                direction=direction,
                speed=self.projectile_speed,
                targets_list=self.unit.targeting.targets_list

            )
        )

    def update(self, dt):
        self.value.assign(self.reload_timer.ratio, 1)

        if not (target := self.unit.targeting.current_target):
            self.reload_timer.stop(self.reload_time)
            self.shooting = False
            return

        direction = Vector2(target.position.pos) - Vector2(self.unit.position.pos)
        if not direction.length_squared() < self.radius ** 2:
            self.reload_timer.stop(self.reload_time)
            self.shooting = False
            return

        if not self.reload_timer.running:
            self.reload_timer.start(self.reload_time)

        self.reload_timer.update(dt)

        if self.reload_timer.is_expired:
            self.shot(target.position.pos)
            self.reload_timer.start(self.reload_time)

        self.shooting = True


class Projectile(Component, pg.sprite.Sprite, SmoothMovementMixin):
    def __init__(
        self,
        unit,
        projectiles,
        damage=10,
        field_rect=None,
        direction=None,
        target_pos=None,
        targets_list=None,
        radius=3,
        speed=5,
    ):
        Sprite.__init__(self, projectiles)
        Component.__init__(self, unit)
        SmoothMovementMixin.__init__(self, unit.position.pos)
        self.radius = radius
        self.damage = damage
        self.field_rect = field_rect
        self.speed = speed
        self.pos = unit.position.pos
        self.direction = direction or self._get_direction(target_pos)
        self.velocity = self.direction * self.speed
        self.image = pg.Surface((2 * self.radius,) * 2, pg.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        self.targets_list = targets_list
        # TODO: example image on sprite
        pg.draw.circle(self.image, (0, 0, 0), (self.radius,) * 2, self.radius)
        # a = pg.transform.smoothscale(pg.image.load("/Users/lampochka/Downloads/spinmaster-NEO-GEO.png").convert_alpha(), (self.radius * 2, ) * 2)
        # self.image = pg.transform.rotate(a, -self.direction.angle + 180)


    def update(self, dt):
        if self.field_rect and not self.field_rect.colliderect(self.rect):
            self.kill()

        if self.targets_list:
            for targets in self.targets_list:
                if collide_target := pg.sprite.spritecollide(
                    self, targets, False, lambda a, b: pg.sprite.collide_circle(a, b)
                ):
                    for target in collide_target:
                        if target.health.alive:
                            target.health.take_damage(self.damage)
                            self.kill()
                            break

        self.pos += self.velocity * dt
        self.rect.center = self.pos

    def _get_direction(self, target_pos):
        if target_pos and pg.Vector2(target_pos) != self.pos:
            return (pg.Vector2(target_pos) - self.pos).normalize()
        else:
            return pg.Vector2()


class LineProjectile(pg.sprite.Sprite):
    def __init__(self, start_pos, target_pos, damage, speed=20):
        super().__init__()
        self.pos = pg.Vector2(start_pos)
        self.target_pos = pg.Vector2(target_pos)
        self.damage = damage
        self.speed = speed
        self.direction = (self.target_pos - self.pos).normalize()
        self.image = pg.Surface((4, 4), pg.SRCALPHA)
        pg.draw.circle(self.image, (0, 255, 0), (2, 2), 2)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

        # убиваем, если долетели до цели
        if self.pos.distance_to(self.target_pos) < 5:
            self.kill()
