import math


class Vector2d(object):

    def __init__(self, x=0.0, y=0.0):
        self._x = float(x)
        self._y = float(y)

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

    def versor(self):
        """
        The versor of this vector, i.e., the directional unitary vector.
        """
        norm = self.norm()
        if norm != 0:
            return Vector2d(self.x/norm, self.y/norm)
        else:
            return Vector2d()

    def norm(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def dotProduct(self, anotherVector):
        return self.x * anotherVector.x + self.y * anotherVector.y

    def projection(self, anotherVector):
        return self * (self.dotProduct(anotherVector) / (self.norm() ** 2))

    def perpendicular(self):
        perpendicular = Vector2d()
        if self.x == 0:
            if self.y == 0:
                return Vector2d()
            perpendicular.x = 1
            perpendicular.y = -self.x / self.y
        else:
            perpendicular.y = 1
            perpendicular.x = -self.y / self.x

        perpendicular /= perpendicular.norm()

        return perpendicular

    def __len__(self):
        return 2

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

    def __sub__(self, arg):
        return Vector2d(self.x - arg, self.y - arg)

    def __isub__(self, arg):
        self.x -= arg
        self.y -= arg

    def __mul__(self, arg):
        return Vector2d(self.x * arg, self.y * arg)

    def __imul__(self, arg):
        self.x *= arg
        self.y *= arg

    def __div__(self, arg):
        return Vector2d(self.x / arg, self.y / arg)

    def __idiv__(self, arg):
        self.x /= arg
        self.y /= arg

    def __str__(self):
        return "Vector(" + self.x + ", " + self.y + ")"