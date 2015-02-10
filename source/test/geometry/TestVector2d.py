import math

from breakout.geometry.Vector2d import Vector2d


# noinspection PyMethodMayBeStatic
class TestVector2d(object):

    def test_get_coordinates(self):
        x, y = 1, 2
        v = Vector2d(x, y)
        assert v.x == x == v[0] == v.coordinates[0]
        assert v.y == y == v[1] == v.coordinates[1]

    def test_set_coordinates(self):
        v = Vector2d(1, 2)
        new_x, new_y = 3, 4
        v.x = new_x
        v.y = new_y

        assert v.x == new_x
        assert v.y == new_y

    def test_negative(self):
        v1 = Vector2d(3, 5)
        v2 = -v1
        assert v2.x == -v1.x and v2.y == -v1.y

    def test_add_scalar(self):
        v1 = Vector2d(3, 5)
        s = 3
        v2 = v1 + s
        assert v2.x == v1.x + s and v2.y == v1.y + s

    def test_add_scalar_inplace(self):
        x, y = 3, 5
        s = 3
        v = Vector2d(x, y)
        v += s
        assert v.x == x + s and v.y == y + s

    def test_subtract_by_scalar(self):
        v1 = Vector2d(3, 5)
        s = 3
        v2 = v1 - s
        assert v2.x == v1.x - s and v2.y == v1.y - s

    def test_subtract_scalar_inplace(self):
        x, y = 3, 5
        s = 3
        v = Vector2d(x, y)
        v += s
        assert v.x == x + s and v.y == y + s

    def test_multiply_by_scalar(self):
        v1 = Vector2d(3, 5)
        s = 3
        v2 = v1 * s
        assert v2.x == v1.x * s and v2.y == v1.y * s

    def test_multiply_by_scalar_inplace(self):
        x, y = 3, 5
        s = 3
        v = Vector2d(x, y)
        v *= s
        assert v.x == x * s and v.y == y * s

    def test_divide_by_scalar(self):
        v1 = Vector2d(3, 6)
        s = 3
        v2 = v1 / s
        assert v2.x == v1.x / s and v2.y == v1.y / s

    def test_divide_by_scalar_inplace(self):
        x, y = 3, 6
        s = 3
        v = Vector2d(x, y)
        v /= s
        assert v.x == x / s and v.y == y / s

    def test_not_equal_to_none(self):
        v = Vector2d(2,3)
        assert not v.__eq__(None)

    def test_not_equal_to_different_type(self):
        v = Vector2d(2,3)
        assert not (v == (2,3))

    def test_not_equal_to_slightly_different_coordinates(self):
        v1 = Vector2d(2,3)
        v2 = Vector2d(2,3.1)
        assert not (v1 == v2)

    def test_not_equal_to_very_different_coordinates(self):
        v1 = Vector2d(5,-35)
        v2 = Vector2d(2,3.1)
        assert not (v1 == v2)

    def test_equal_if_coordinates_are_equal(self):
        v1 = Vector2d(2,3.1)
        v2 = Vector2d(2,3.1)
        assert v1 == v2

    def test_versor_from_non_zero_vector(self):
        v = Vector2d(10, 20)
        versor = v.versor()
        assert versor == v / abs(v)

    def test_versor_from_zero_vector(self):
        v = Vector2d(0, 0)
        versor = v.versor()
        assert versor.x == 0 and versor.y == 0

    def test_norm(self):
        (v1,v2) = (3,4)
        v = Vector2d(v1,v2)
        assert abs(v) == v.norm() == math.sqrt(v1*v1 + v2*v2)

    def test_dot_product(self):
        (v1,v2) = (3,4.23)
        v = Vector2d(v1,v2)
        (w1,w2) = (8.65,3.5)
        w = Vector2d(w1,w2)

        assert v.dotProduct(w) == v1*w1 + v2*w2

    def test_dot_product_between_two_vectors_90_degrees_away_is_zero(self):
        v1 = Vector2d(0,50)
        v2 = Vector2d(100,0)
        assert v1.dotProduct(v2) == 0
        assert v2.dotProduct(v1) == 0

    def test_projection(self):
        v1 = Vector2d(0,50)
        v2 = Vector2d(1,23)

    def test_to_string(self):
        v = Vector2d(1.5,50.3)
        assert str(v) == "(1.5, 50.3)"