
class Rectangle(object):

    def __init__(self, left=0.0, bottom=0.0, right=0.0, top=0.0):
       self._left = float(left)
       self._bottom = float(bottom)
       self._right = float(right)
       self._top = float(top)

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
        return "Rectangle {Left: " + str(self.left) + ", Bottom: " + str(self.bottom) + \
               ", Right: " + str(self.right) + ", Top: " + str(self.top) + "}"

    def __eq__(self, other):
        if other is None:
            return False

        if not isinstance(other, Rectangle):
            return False

        return self.left == other.left and self.right == other.right \
               and self.top == other.top and self.bottom == other.bottom

