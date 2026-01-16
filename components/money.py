from typing import Optional

from components.health import Health
from core.component import Component
from core.utils import SimpleTimer


class Money(Component):
    def __init__(self, initial_amount=0, salary=0, coin_time=1.0, context=None):
        super().__init__(context)
        self.amount = initial_amount
        self.salary = salary

        self.health: Optional[Health] = None
        self.coin_timer: Optional[SimpleTimer] = SimpleTimer(coin_time)

    def add(self, amount):
        self.amount += amount

    def spend(self, amount):
        if amount <= self.amount:
            self.amount -= amount
            return True
        return False

    def on_added(self):
        self.coin_timer.start()

    def update(self, dt):
        self.coin_timer.update(dt)
        if self.coin_timer.is_expired:
            self.amount += self.salary
            self.coin_timer.start()

    def set_salary(self, salary):
        self.salary = salary
