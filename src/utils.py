import numpy as np


class Vector2:
    EPS = 1e-10  # numerical zero

    def __init__(self, x=0., y=0.):
        self._data = np.array([x, y])

    # Get and set x, y

    @property
    def x(self):
        return self._data[0]

    @x.setter
    def set_x(self, x):
        self._data[0] = x

    @property
    def y(self):
        return self._data[1]

    @y.setter
    def set_y(self, y):
        self._data[1] = y

    #
    # Arithematical operations: +, -, *, /
    #

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self = self.__add__(other)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            raise TypeError('Cannot multiply two Vector2. '
                            'For dot product, use: x | y '
                            'For cross product, use: x ^ y ')
        return Vector2(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            raise TypeError('Cannot divide two Vector2.')
        return Vector2(self.x / other, self.y / other)

    def __abs__(self):
        return np.sqrt(self._data**2)

    def __bool__(self):
        return len(self) < Vector2.EPS

    def __or__(self, other):
        # dot product
        return self.x * other.x + self.y * other.y

    def __xor__(self, other):
        # cross product
        return self.x * other.y - self.y * other.x
