import pytest

from breakout.geometry.Vector2d import Vector2d
from breakout.model.Ball import Ball
from breakout.game.GameEngine import GameEngine
from breakout.model.Block import Block
from breakout.model.BlockColor import BlockColor
from breakout.model.collision.CollisionDetector import CollisionDetector


# noinspection PyUnresolvedReferences
@pytest.fixture
def gameEngine():
    return GameEngine(250, 300)

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def ball(gameEngine):
    return Ball(gameEngine, radius=2.5)

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def block(gameEngine):
    return Block(gameEngine, BlockColor.BLUE, width=10, height=10)

# noinspection PyShadowingNames, PyUnresolvedReferences
@pytest.fixture
def collisionDetector(ball):
    return CollisionDetector(ball)

# noinspection PyShadowingNames, PyMethodMayBeStatic
class TestCollisionDetector(object):

    def test_raise_exception_if_object_is_not_movable(self, block):
        with pytest.raises(Exception):
            CollisionDetector(block)

    def test_top_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x, block.position.y + block.height/2)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == True
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == False

    def test_bottom_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x, block.position.y - block.height/2)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == True
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == False

    def test_right_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x + block.width/2, block.position.y)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == True
        assert collisionWithObject.hasLeftIntersection == False

    def test_left_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x - block.width/2, block.position.y)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == True

    def test_top_right_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x + block.width/2, block.position.y + block.height/2)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == True
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == True
        assert collisionWithObject.hasLeftIntersection == False

    def test_top_left_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x - block.width/2, block.position.y + block.height/2)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == True
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == True

    def test_bottom_right_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x + block.width/2, block.position.y - block.height/2)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == True
        assert collisionWithObject.hasRightIntersection == True
        assert collisionWithObject.hasLeftIntersection == False

    def test_bottom_left_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x - block.width/2, block.position.y - block.height/2)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == True
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == True

    def test_inner_collision_with_object(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x, block.position.y)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == True
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == False

    def test_vertical_intersection_without_horizontal_intersection_with_object_is_not_collision(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x - block.width, block.position.y)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == False
        assert collisionWithObject.hasVerticalIntersection == True
        assert collisionWithObject.hasHorizontalIntersection == False

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == False

    def test_horizontal_intersection_without_vertical_intersection_with_object_is_not_collision(self, collisionDetector, block):
        block.position = Vector2d(block.width/2, block.height/2)

        ball = collisionDetector.movingObject
        ball.position = Vector2d(block.position.x, block.position.y + block.height)

        collisionWithObject = collisionDetector.detectCollisionWithObject(block)
        assert collisionWithObject.happened == False
        assert collisionWithObject.hasVerticalIntersection == False
        assert collisionWithObject.hasHorizontalIntersection == True

        assert collisionWithObject.hasTopIntersection == False
        assert collisionWithObject.hasBottomIntersection == False
        assert collisionWithObject.hasRightIntersection == False
        assert collisionWithObject.hasLeftIntersection == False