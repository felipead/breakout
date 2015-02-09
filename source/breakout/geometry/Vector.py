import math

class Vector(list):

    # noinspection PyTypeChecker
    def __init__(self, arg=()):
        list.__init__(self, map(float, arg))

    def _getX(self):
        return self[0]

    def _setX(self, x):
        self[0] = float(x)

    x = property(_getX, _setX)

    def _getY(self):
        return self[1]

    def _setY(self, y):
        self[1] = float(y)

    y = property(_getY, _setY)

    def _getZ(self):
        if len(self) < 3:
            raise Exception("Vector must have at least three dimensions.")
        return self[2]

    def _setZ(self, z):
        if len(self) < 3:
            raise Exception("Vector must have at least three dimensions.")
        self[2] = float(z)

    z = property(_getZ, _setZ)

    def versor(self):
        """Returns the versor of this vector, i.e., the directional unitary vector."""
        norm = abs(self)
        if norm != 0:
            return self/norm
        else:
            # Returns the ZERO vector
            zeros = []
            for i in self:
                zeros.append(0)
            return Vector(zeros)

    def norm(self):
        norm = 0
        for i in self:
            norm += i**2
        norm = math.sqrt(norm)
        return norm

    def dotProduct(self, vector):
        total = 0
        for i, j in zip(self, vector):
            total += i * j
        return total

    def projection(self, vector):
        return self * (self.dotProduct(vector) / self.norm()**2)

    def perpendicular(self):
        if not len(self) == 2:
            raise Exception("This operation is only supported on 2-dimension vectors")

        perpendicular = Vector()
        if self.x == 0:
            if self.y == 0:
                return Vector()
            perpendicular.x = 1
            perpendicular.y = -self.x / self.y
        else:
            perpendicular.y = 1
            perpendicular.x = -self.y / self.x
        perpendicular /= perpendicular.norm()
        return perpendicular

    def __abs__(self):
        return self.norm()

    def __neg__(self):
        new = []
        for i in self:
            new.append(-i)
        return Vector(new)

    def __add__(self, arg):
        new = []
        for i, j in zip(self, arg):
            new.append(i + j)
        return Vector(new)

    def __sub__(self, arg):
        new = []
        for i, j in zip(self, arg):
            new.append(i - j)
        return Vector(new)

    def __mul__(self, arg):
        new = []
        for i in self:
            new.append(i * arg)
        return Vector(new)

    def __div__(self, arg):
        new = []
        for i in self:
            new.append(i / arg)
        return Vector(new)

    def __cmp__(self, arg):
        return cmp(self.norm(), float(arg))

    def __rmul__(self, arg):
        return self.__mul__(arg)

    def __radd__(self, arg):
        return self.__add__(arg)

    def __rsub__(self, arg):
        return self.__sub__(arg)

    def __iadd__(self, arg):
        for i in xrange(len(self)):
            self[i] += arg[i]
        return Vector(self)

    def __isub__(self, arg):
        for i in xrange(len(self)):
            self[i] -= arg[i]
        return Vector(self)

    def __imul__(self, arg):
        for i in xrange(len(self)):
            self[i] *= arg
        return Vector(self)

    def __idiv__(self, arg):
        for i in xrange(len(self)):
            self[i] /= arg
        return Vector(self)
        
    def __str__(self):
        s = "("
        for i in xrange(len(self) - 1):
            s += str(self[i]) + ","
        s += str(self[len(self) - 1]) + ")"
        return s
