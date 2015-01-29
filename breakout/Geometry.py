# encoding: utf-8
"""
Copyright (c) 2010 Felipe Augusto Dornelas. All rights reserved.
"""

import math

#===================================================================================================

class Vector(list):

    def __init__(self, arg):
        if len(arg) < 2:
            raise Exception("The vector must have at least two dimensions.")
        list.__init__(self, map(float, arg))

    def _getX(self):
        return self[0]

    def _setX(self, x):
        self[0] = float(x)

    # Syntax sugar for the 1st dimension
    x = property(_getX, _setX)

    def _getY(self):
        return self[1]

    def _setY(self, y):
        self[1] = float(y)

    # Syntax sugar for the 2nd dimension
    y = property(_getY, _setY)

    def _getZ(self):
        if len(self) < 3:
            raise Exception("The vector must have at least three dimensions.")
        return self[2]

    def _setZ(self, z):
        if len(self) < 3:
            raise Exception("The vector must have at least three dimensions.")
        self[2] = float(z)

    # Syntax sugar for the 3rd dimension
    z = property(_getZ, _setZ)

    def versor(self):
        """Returns the versor of this vector, i.e., the directional unitary vector."""
        module = abs(self)
        if module != 0:
            return self/module
        else:
            # Returns the ZERO vector
            zeros = []
            for i in self:
                zeros.append(0)
            return Vector(zeros)

    def module(self):
        module = 0
        for i in self:
            module += i**2
        module = math.sqrt(module)
        return module

    def projection(self, vector):
        return self * (self.scalar(vector) / self.module()**2)

    def scalar(self, vector):
        total = 0
        for i, j in zip(self, vector):
            total += i * j
        return total

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
        new = new / new.module()
        return new

    def __abs__(self):
        return self.module()

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
        return cmp(self.module(), float(arg))

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

#===================================================================================================

class Rectangle:

    def __init__(self, left = 0, bottom = 0, right = 0, top = 0):
       self._left = left
       self._bottom = bottom
       self._right = right
       self._top = top

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    @property
    def bottom(self):
        return self._bottom

    @property
    def top(self):
        return self._top
    
    @property
    def width(self):
        return self._right - self._left
    
    @property
    def height(self):
        return self._top - self._bottom

    def __str__(self):
        return "(" + str(self.left) + "," + str(self.bottom) + "," + \
               str(self.right) + "," + str(self.top) + ")"

#===================================================================================================
