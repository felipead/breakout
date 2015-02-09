
class Rectangle(object):

    def __init__(self, left=0, bottom=0, right=0, top=0):
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
        return str((self.left, self.bottom, self.right, self.top))

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Rectangle):
            return False

        return self.left == other.left and self.right == other.right \
               and self.top == other.top and self.bottom == other.bottom

