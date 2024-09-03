import math

import pygame.sprite


def get_distance(from_pos, to_pos):
    dx = from_pos[0] - to_pos[0]
    dy = from_pos[1] - to_pos[1]
    return math.hypot(dx, dy)

    # if distance < (circle1_radius + circle2_radius):


class SimpleTimer:
    def __init__(self):
        self.time = None
        self.start_time = pygame.time.get_ticks()

    def __call__(self):
        return pygame.time.get_ticks() - self.start_time

    def start(self, msec):
        self.start_time = pygame.time.get_ticks()
        self.time = msec

    @property
    def ratio(self):
        if self.time == 0:
            return 1

        return max(0, min((1, (pygame.time.get_ticks() - self.start_time) / self.time))) if self.time else 0

    def is_expired(self):
        if not self.time:
            return True
        return True if (pygame.time.get_ticks() >= (self.start_time + self.time)) else False

    def stop(self):
        self.__init__()

