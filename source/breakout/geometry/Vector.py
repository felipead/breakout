
import math

class Vector(list):

    def __init__(self, arg=()):
        list.__init__(self, map(float, arg))


    def _get_x(self):
        return self[0]

    def _set_x(self, x):
        self[0] = float(x)

    x = property(_get_x, _set_x)


    def _get_y(self):
        return self[1]

    def _set_y(self, y):
        self[1] = float(y)

    y = property(_get_y, _set_y)


    def _get_z(self):
        if len(self) < 3:
            raise Exception("Vector must have at least three dimensions.")
        return self[2]

    def _set_z(self, z):
        if len(self) < 3:
            raise Exception("Vector must have at least three dimensions.")
        self[2] = float(z)

    z = property(_get_z, _set_z)


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

    def dot_product(self, vector):
        total = 0
        for i, j in zip(self, vector):
            total += i * j
        return total

    def projection(self, vector):
        return self * (self.dot_product(vector) / self.norm()**2)

    def perpendicular(self):
        if not len(self) == 2:
            raise Exception("This operation is only supported on 2-dimension vectors")

        new = Vector()
        if self.x == 0:
            if self.y == 0:
                return Vector()
            new.x = 1
            new.y = -self.x / self.y
        else:
            new.y = 1
            new.x = -self.y / self.x
        new = new / new.norm()
        return new

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
