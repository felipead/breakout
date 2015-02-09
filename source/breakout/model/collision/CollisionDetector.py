from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.model.collision.CollisionWithObject import CollisionWithObject


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
