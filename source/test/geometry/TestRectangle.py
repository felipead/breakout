
from breakout.geometry.Rectangle import Rectangle


class TestRectangle:

    def test_width(self):
        rectangle = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        assert rectangle.width == 20

    def test_height(self):
        rectangle = Rectangle(left = -10, bottom = -20, right = 10, top = 20)
        assert rectangle.height == 40
