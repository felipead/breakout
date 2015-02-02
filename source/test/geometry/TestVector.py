import math

from breakout.geometry.Vector import Vector


class TestVector:

    def test_get_coordinates(self):
        x, y, z = 1, 2, 3
        v = Vector((x, y, z))
        assert v.x == x
        assert v.y == y
        assert v.z == z

    def test_set_coordinates(self):
        v = Vector((1, 2, 3))
        new_x, new_y, new_z = 5, 6, 7
        v.x = new_x
        v.y = new_y
        v.z = new_z

        assert v.x == new_x
        assert v.y == new_y
        assert v.z == new_z

    def test_versor_from_non_zero_vector(self):
        v = Vector((10, 20))
        versor = v.versor()
        assert versor == v/abs(v)

    def test_versor_from_zero_vector(self):
        v = Vector((0, 0))
        versor = v.versor()
        assert versor.x == 0 and versor.y == 0

    def test_norm_of_2d_vector(self):
        (v1,v2) = (3,4)
        v = Vector((v1,v2))
        assert abs(v)== math.sqrt(v1*v1 + v2*v2)

    def test_norm_of_3d_vector(self):
        (v1,v2,v3) = (3,4,5)
        v = Vector((v1,v2,v3))
        assert abs(v) == math.sqrt(v1*v1 + v2*v2 + v3*v3)

    def test_dot_product_between_2d_vectors(self):
        (v1,v2) = (3,4.23)
        v = Vector((v1,v2))
        (w1,w2) = (8.65,3.5)
        w = Vector((w1,w2))

        assert v.dotProduct(w) == v1*w1 + v2*w2

    def test_dot_product_between_3d_vectors(self):
        (v1,v2,v3) = (3,4.23,8)
        v = Vector((v1,v2,v3))
        (w1,w2,w3) = (8.65,3.5,13.9)
        w = Vector((w1,w2,w3))

        assert v.dotProduct(w) == v1*w1 + v2*w2 + v3*w3

    def test_dot_product_between_2d_and_3d_vectors(self):
        (v1,v2) = (3,4.23)
        v = Vector((v1,v2))

        (w1,w2,w3) = (8.65,3.5,13.9)
        w = Vector((w1,w2,w3))

        assert v.dotProduct(w) == v1*w1 + v2*w2

    def test_dot_product_between_two_vectors_90_degrees_away_is_zero(self):
        v1 = Vector((0,50))
        v2 = Vector((100,0))
        assert v1.dotProduct(v2) == 0
        assert v2.dotProduct(v1) == 0
