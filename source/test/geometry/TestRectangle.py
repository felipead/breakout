
from breakout.geometry.Rectangle import Rectangle


# noinspection PyMethodMayBeStatic
class TestRectangle:

    def test_get_coordinates(self):
        left, bottom, right, top = -10, -10, 10, 10
        rectangle = Rectangle(left = left, bottom = bottom, right = right, top = top)
        assert rectangle.left == left
        assert rectangle.right == right
        assert rectangle.bottom == bottom
        assert rectangle.top == top

    def test_width(self):
        rectangle = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        assert rectangle.width == 20

    def test_height(self):
        rectangle = Rectangle(left = -10, bottom = -20, right = 10, top = 20)
        assert rectangle.height == 40
