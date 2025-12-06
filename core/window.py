import pygame as pg
from typing import Union, Tuple


class Window:
    def __init__(self, size: Tuple[int, int] = (600, 400), caption: str = "", FPS: int = 30, vsync=0, flags=0):
        self._screen = None
        self._caption = caption
        self._FPS = FPS
        self._default_width, self._default_height = size
        self._size = self._width, self._height = size
        self._flags = flags
        self._vsync = vsync

        self.update()


    def __call__(self, *args, **kwargs):
        return self.scale(*args, **kwargs)

    @property
    def scale_x(self):
        return self._width / self._default_width

    @property
    def scale_y(self):
        return self._height / self._default_height

    def scale(self, value: Union[pg.Rect, float] = None, x: float = None, y: float = None):
        if isinstance(value, pg.Rect):
            return self.scale_rect(value)
        if value is not None:
            return self.scale_uniform(value)
        if x is not None and y is not None:
            return x * self.scale_x, y * self.scale_y
        if x is not None:
            return x * self.scale_x
        if y is not None:
            return y * self.scale_y

    def scale_uniform(self, v: float) -> float:
        return v * ((self.scale_x + self.scale_y) / 2)

    def scale_rect(self, rect: pg.Rect) -> pg.Rect:
        x, y = self.scale(rect.x, rect.y)
        w, h = self.scale(rect.width, rect.height)
        return pg.Rect(int(x), int(y), int(w), int(h))

    # свойства
    @property
    def FPS(self):
        return self._FPS

    @property
    def caption(self):
        return self._caption

    @property
    def screen(self) -> pg.Surface:
        return self._screen

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Tuple[int, int]):
        self._width, self._height = size
        self._size = size
        self.update()

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width: int):
        self.size = (width, self._height)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int):
        self.size = (self._width, height)  # только высота меняется, ширина остаётся

    def update(self):
        self._screen = pg.display.set_mode(self._size, self._flags, vsync=self._vsync)
        pg.display.set_caption(self._caption)

    def resize(self, size):
        self.size = size