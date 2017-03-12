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
        try:
            return Vector2(self.x + other.x, self.y + other.y)
        except AttributeError:
            raise TypeError(
                'Cannot add non-Vector2 to Vector2: {}'.format(other))

    def __sub__(self, other):
        try:
            return Vector2(self.x - other.x, self.y - other.y)
        except AttributeError:
            raise TypeError(
                'Cannot subtract non-Vector2 from Vector2: {}'.format(other))

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            raise TypeError('Cannot multiply two Vector2. '
                            'For dot product, use: x | y '
                            'For cross product, use: x ^ y ')
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Vector2):
            raise TypeError('Division of two Vector2 is undefined.')
        return Vector2(self.x / other, self.y / other)

    def __or__(self, other):
        # dot product
        try:
            return self.x * other.x + self.y * other.y
        except AttributeError:
            raise TypeError(
                'Cannot dot non-Vector2 and Vector2: {}'.format(other))

    def __xor__(self, other):
        # cross product
        try:
            return self.x * other.y - self.y * other.x
        except AttributeError:
            raise TypeError(
                'Cannot cross non-Vector2 and Vector2: {}'.format(other))

    def __abs__(self):
        return np.sqrt(self | self)

    def __bool__(self):
        return bool(abs(self) > Vector2.EPS)

    def dist(self, other):
        return abs(self - other)

    def dist2(self, other):
        return (self - other) | (self - other)
