
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
