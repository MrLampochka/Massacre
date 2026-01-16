from pygame import Vector2

from components.health import Health
from components.transform import Transform
from core.component import Component


class Movement(Component):
    def __init__(self, speed=1, direction=None, velocity=None, context=None):
        super().__init__(context)
        self.speed = speed
        self.velocity = velocity or Vector2()
        self.direction = direction or Vector2()

    def update(self, dt):
        if (health := self.get_component(Health)) and not health.alive:
            self.to_direction(health.dying_direction, health.dying_speed)

        if transform := self.get_component(Transform):
            if self.direction.length_squared() > 0:
                self.velocity = self.direction.normalize() * self.speed
                transform.pos += self.velocity * dt
            else:
                self.stop()

    def to_direction(self, direction: Vector2, speed=None):
        if speed:
            self.speed = speed

        self.direction = direction

    def to_target(self, target, speed=None):
        if speed:
            self.speed = speed

        if transform := self.get_component(Transform):
            self.direction = Vector2(target.position.pos) - Vector2(transform.pos)

    def stop(self):
        self.direction = Vector2(0, 0)
        self.velocity.update(0, 0)
