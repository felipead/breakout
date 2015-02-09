import math

from breakout.geometry.Vector2d import Vector2d


# noinspection PyMethodMayBeStatic
class TestVector:

    def test_get_coordinates(self):
        x, y = 1, 2
        v = Vector2d(x, y)
        assert v.x == x
        assert v.y == y

    def test_set_coordinates(self):
        v = Vector2d(1, 2)
        new_x, new_y = 3, 4
        v.x = new_x
        v.y = new_y

        assert v.x == new_x
        assert v.y == new_y

    def test_versor_from_non_zero_vector(self):
        v = Vector2d(10, 20)
        versor = v.versor()
        assert versor == v/abs(v)

    def test_versor_from_zero_vector(self):
        v = Vector2d(0, 0)
        versor = v.versor()
        assert versor.x == 0 and versor.y == 0

    def test_norm(self):
        (v1,v2) = (3,4)
        v = Vector2d(v1,v2)
        assert abs(v) == math.sqrt(v1*v1 + v2*v2)

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