from pygame import Vector2
from core.component import Component


class Transform(Component):
    def __init__(
        self,
        x=0.0,
        y=0.0,
        rotation=0.0,
        scale_x=1.0,
        scale_y=1.0,
        scale=None,
        pos=None,
        context=None,
    ):
        """
        Компонент трансформации: позиция, поворот, масштаб.
        :param x: Координата X
        :param y: Координата Y
        :param rotation: Угол поворота (градусы)
        :param scale_x: Масштаб по x (1.0 — без изменений)
        :param scale_y: Масштаб по y (1.0 — без изменений)
        """
        super().__init__(context)
        self.rotation = rotation

        self._x, self._y = x, y
        self.pos = pos or Vector2(x, y)

        self.scale_x, self.scale_y = scale_x, scale_y
        self.scale = scale or Vector2(scale_x, scale_y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def pos(self) -> Vector2:
        """Возвращает позицию как Vector2"""
        return Vector2(self.x, self.y)

    @pos.setter
    def pos(self, value):
        """Устанавливает позицию через Vector2"""
        self.x = value.x
        self.y = value.y

    @property
    def angle(self) -> float:
        """Возвращает угол поворота (градусы)"""
        return self.rotation

    @angle.setter
    def angle(self, value: float):
        """Устанавливает угол поворота (градусы)"""
        self.rotation = value

    @property
    def scale(self) -> Vector2:
        """Возвращает масштаб по осям как Vector2"""
        return Vector2(self.scale_x, self.scale_y)

    @scale.setter
    def scale(self, value: Vector2):
        self.scale_x = value.x
        self.scale_y = value.y
