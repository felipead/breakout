import pytest

from breakout.game.GameEngine import GameEngine
from breakout.model.Ball import Ball
from breakout.geometry.Vector2d import Vector2d
from breakout.model.collision.CollisionWithObject import CollisionWithObject

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def gameEngine():
    return GameEngine(250, 300)

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def originalSpeed():
    return Vector2d(5.7, -3.2)

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def ball(gameEngine, originalSpeed):
    return Ball(gameEngine, radius=3, position=Vector2d(0, 0), speed=originalSpeed)

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def collisionWithObject():
    collisionWithObject = CollisionWithObject()
    collisionWithObject.hasHorizontalIntersection = True
    collisionWithObject.hasVerticalIntersection = True
    return collisionWithObject


# noinspection PyShadowingNames, PyMethodMayBeStatic
class TestCollisionWithObject(object):

    def test_apply_top_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasTopIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == originalSpeed.x
        assert ball.speed.y == abs(originalSpeed.y)

    def test_apply_bottom_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasBottomIntersection= True

        collisionWithObject.apply(ball)
        assert ball.speed.x == originalSpeed.x
        assert ball.speed.y == -abs(originalSpeed.y)

    def test_apply_right_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasRightIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == abs(originalSpeed.x)
        assert ball.speed.y == originalSpeed.y

    def test_apply_left_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasLeftIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == -abs(originalSpeed.x)
        assert ball.speed.y == originalSpeed.y

    def test_apply_top_right_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasTopIntersection = True
        collisionWithObject.hasRightIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == abs(originalSpeed.x)
        assert ball.speed.y == abs(originalSpeed.y)

    def test_apply_top_left_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasTopIntersection = True
        collisionWithObject.hasLeftIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == -abs(originalSpeed.x)
        assert ball.speed.y == abs(originalSpeed.y)

    def test_apply_bottom_right_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasBottomIntersection = True
        collisionWithObject.hasRightIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == abs(originalSpeed.x)
        assert ball.speed.y == -abs(originalSpeed.y)

    def test_apply_bottom_left_collision_impact_to_moving_object(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasBottomIntersection = True
        collisionWithObject.hasLeftIntersection = True

        collisionWithObject.apply(ball)
        assert ball.speed.x == -abs(originalSpeed.x)
        assert ball.speed.y == -abs(originalSpeed.y)

    def test_choose_random_speed_directions_when_applying_inner_intersection_collisions(self, ball, collisionWithObject, originalSpeed):
        collisionWithObject.hasBottomIntersection = False
        collisionWithObject.hasLeftIntersection = False
        collisionWithObject.hasTopIntersection = False
        collisionWithObject.hasRightIntersection = False

        collisionWithObject.apply(ball)


        assert abs(ball.speed.x) == abs(originalSpeed.x)
        assert abs(ball.speed.y) == abs(originalSpeed.y)

    def test_does_not_apply_collision_if_it_did_not_happened(self, ball, originalSpeed):
        collisionWithObject = CollisionWithObject()

        collisionWithObject.apply(ball)

        assert ball.speed.x == originalSpeed.x
        assert ball.speed.y == originalSpeed.y