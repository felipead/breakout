import math


class Vector2d(object):

    def __init__(self, x=0.0, y=0.0, copyFrom=None):
        if copyFrom == None:
            self._x = float(x)
            self._y = float(y)
        else:
            self._x = float(copyFrom[0])
            self._y = float(copyFrom[1])

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def coordinates(self):
        return self.x, self.y

    def versor(self):
        """
        The versor of this vector, i.e., the directional unitary vector.
        """
        norm = self.norm()
        if norm != 0:
            return self / norm
        else:
            return Vector2d()

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dotProduct(self, anotherVector):
        return self.x * anotherVector.x + self.y * anotherVector.y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError()

    def __abs__(self):
        return self.norm()

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Vector2d):
            return False

        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Vector2d(-self.x, -self.y)

    def __add__(self, arg):
        return Vector2d(self.x + arg, self.y + arg)

    def __iadd__(self, arg):
        self.x += arg
        self.y += arg
        return self

    def __sub__(self, arg):
        return Vector2d(self.x - arg, self.y - arg)

    def __isub__(self, arg):
        self.x -= arg
        self.y -= arg
        return self

    def __mul__(self, arg):
        return Vector2d(self.x * arg, self.y * arg)

    def __imul__(self, arg):
        self.x *= arg
        self.y *= arg
        return self

    def __div__(self, arg):
        return Vector2d(self.x / arg, self.y / arg)

    def __idiv__(self, arg):
        self.x /= arg
        self.y /= arg
        return self

    def __str__(self):
        return str((self.x, self.y))