from breakout.geometry.Rectangle import Rectangle


# noinspection PyMethodMayBeStatic
class TestRectangle(object):

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

    def test_to_string(self):
        assert str(Rectangle(-10, -10, 10, 10)) == "Rectangle {Left: -10.0, Bottom: -10.0, Right: 10.0, Top: 10.0}"

    def test_not_equal_to_none(self):
        r = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        assert not r.__eq__(None)

    def test_not_equal_to_different_type(self):
        r = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        assert not (r == 5)

    def test_not_equal_to_slightly_different_rectangle(self):
        r1 = Rectangle(left = -10, bottom = -10, right = 10.5, top = 10)
        r2 = Rectangle(left = -10, bottom = -10.1, right = 10, top = 10)
        assert not (r1 == r2)

    def test_not_equal_to_very_different_rectangle(self):
        r1 = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        r2 = Rectangle(left = -50, bottom = -10, right = 50, top = 50)
        assert not (r1 == r2)

    def test_equal_if_rectangle_is_exactly_equal(self):
        r1 = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        r2 = Rectangle(left = -10, bottom = -10, right = 10, top = 10)
        assert r1 == r2