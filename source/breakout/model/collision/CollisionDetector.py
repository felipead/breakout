from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.model.collision.CollisionWithBoundaryEdge import CollisionWithBoundaryEdge
from breakout.model.collision.CollisionWithObject import CollisionWithObject
from breakout.model.collision.BoundaryEdgeType import BoundaryEdgeType


class CollisionDetector(object):

    def __init__(self, movingObject):
        if not isinstance(movingObject, AbstractMovableGameObject):
            raise Exception("object must be movable")
        self._movingObject = movingObject

    @property
    def movingObject(self):
        return self._movingObject

    def detectCollisionWithObject(self, otherObject):
        collisionWithObject = CollisionWithObject()

        if otherObject is None or otherObject is self._movingObject:
            return False

        self.__detectVerticalIntersection(collisionWithObject, self._movingObject.rectangle, otherObject.rectangle)
        self.__detectHorizontalIntersection(collisionWithObject, self._movingObject.rectangle, otherObject.rectangle)

        return collisionWithObject

    def detectCollisionWithBoundaryEdge(self, boundariesRectangle):
        objectRectangle = self._movingObject.rectangle

        collisionWithBoundaryEdge = CollisionWithBoundaryEdge()

        if objectRectangle.left <= boundariesRectangle.left:
            collisionWithBoundaryEdge.type = BoundaryEdgeType.LEFT
        elif objectRectangle.right >= boundariesRectangle.right:
            collisionWithBoundaryEdge.type = BoundaryEdgeType.RIGHT
        elif objectRectangle.top >= boundariesRectangle.top:
            collisionWithBoundaryEdge.type = BoundaryEdgeType.TOP
        elif objectRectangle.bottom <= boundariesRectangle.bottom:
            collisionWithBoundaryEdge.type = BoundaryEdgeType.BOTTOM

        return collisionWithBoundaryEdge


    # noinspection PyChainedComparisons
    @staticmethod
    def __detectVerticalIntersection(collisionWithObject, A, B):
        if A.top >= B.top and A.bottom >= B.bottom and A.bottom <= B.top:
            collisionWithObject.hasVerticalIntersection = True
            collisionWithObject.hasTopIntersection = True
        elif A.top <= B.top and A.bottom >= B.bottom:
            collisionWithObject.hasVerticalIntersection = True
        elif A.top <= B.top and A.bottom <= B.bottom and A.top >= B.bottom:
            collisionWithObject.hasVerticalIntersection = True
            collisionWithObject.hasBottomIntersection = True

    # noinspection PyChainedComparisons
    @staticmethod
    def __detectHorizontalIntersection(collisionWithObject, A, B):
        if A.left <= B.left and A.right <= B.right and B.left <= A.right:
            collisionWithObject.hasHorizontalIntersection = True
            collisionWithObject.hasLeftIntersection = True
        elif A.left >= B.left and A.right <= B.right:
            collisionWithObject.hasHorizontalIntersection = True
        elif A.left >= B.left and A.right >= B.right and A.left <= B.right:
            collisionWithObject.hasHorizontalIntersection = True
            collisionWithObject.hasRightIntersection = True
