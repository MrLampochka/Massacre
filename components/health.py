from pygame import Vector2

from core.component import Component
from core.utils import SV, Timer


class Health(Component):
    def __init__(self, value: int | SV, dying_time=1, dying_speed=2, dying_direction=Vector2(0, -1), context=None):
        super().__init__(context)
        self.value = value if isinstance(value, SV) else SV(value)
        self.alive = True
        self.dying_timer = Timer(dying_time) if dying_time else None
        self.dying_speed = dying_speed
        self.dying_direction = dying_direction

    def update(self, dt):
        if self.dying_timer:
            self.dying_timer.update(dt)

        if not self.alive:
            if self.dying_timer.is_expired:
                self.game_object.kill()

        elif self.value.current <= 0:
            self.alive = False
            if self.dying_timer:
                self.dying_timer.start()


    def take_damage(self, amount):
        if self.alive:
            self.value.current = max(0, self.value.current - amount)
            return True
        return False

    def get_value(self):
        return self.value
