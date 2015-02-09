import pytest
from breakout.game.GameEngine import GameEngine
from breakout.geometry.Vector2d import Vector2d
from breakout.model.Ball import Ball
from breakout.model.collision.BoundaryEdgeType import BoundaryEdgeType
from breakout.model.collision.CollisionWithBoundaryEdge import CollisionWithBoundaryEdge

# noinspection PyUnresolvedReferences
@pytest.fixture
def gameEngine():
    return GameEngine(250, 300)

# noinspection PyUnresolvedReferences
@pytest.fixture
def originalSpeed():
    return Vector2d(-2.5, 3.8)

# noinspection PyUnresolvedReferences,PyShadowingNames
@pytest.fixture
def ball(gameEngine, originalSpeed):
    return Ball(gameEngine, radius=2.5, speed=originalSpeed)


# noinspection PyShadowingNames,PyMethodMayBeStatic
class TestCollisionWithBoundaryEdge(object):

    def test_apply_collision_impact_with_top_boundary_edge(self, ball, originalSpeed):
        collisionWithBoundaryEdge = CollisionWithBoundaryEdge()
        collisionWithBoundaryEdge.type = BoundaryEdgeType.TOP

        assert collisionWithBoundaryEdge.happened

        collisionWithBoundaryEdge.apply(ball)
        assert ball.speed.x == originalSpeed.x
        assert ball.speed.y == -abs(originalSpeed.y)

    def test_apply_collision_impact_with_bottom_boundary_edge(self, ball, originalSpeed):
        collisionWithBoundaryEdge = CollisionWithBoundaryEdge()
        collisionWithBoundaryEdge.type = BoundaryEdgeType.BOTTOM

        assert collisionWithBoundaryEdge.happened

        collisionWithBoundaryEdge.apply(ball)
        assert ball.speed.x == originalSpeed.x
        assert ball.speed.y == abs(originalSpeed.y)

    def test_apply_collision_impact_with_left_boundary_edge(self, ball, originalSpeed):
        collisionWithBoundaryEdge = CollisionWithBoundaryEdge()
        collisionWithBoundaryEdge.type = BoundaryEdgeType.LEFT

        assert collisionWithBoundaryEdge.happened

        collisionWithBoundaryEdge.apply(ball)
        assert ball.speed.x == abs(originalSpeed.x)
        assert ball.speed.y == originalSpeed.y

    def test_apply_collision_impact_with_right_boundary_edge(self, ball, originalSpeed):
        collisionWithBoundaryEdge = CollisionWithBoundaryEdge()
        collisionWithBoundaryEdge.type = BoundaryEdgeType.RIGHT

        assert collisionWithBoundaryEdge.happened

        collisionWithBoundaryEdge.apply(ball)
        assert ball.speed.x == -abs(originalSpeed.x)
        assert ball.speed.y == originalSpeed.y

    def test_do_not_apply_collision_impact_if_collision_did_not_happened(self, ball, originalSpeed):
        collisionWithBoundaryEdge = CollisionWithBoundaryEdge()
        collisionWithBoundaryEdge.type = None

        assert not collisionWithBoundaryEdge.happened

        collisionWithBoundaryEdge.apply(ball)
        assert ball.speed.x == originalSpeed.x
        assert ball.speed.y == originalSpeed.y