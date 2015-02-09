from breakout.model.Collision import Collision


class CollisionDetector(object):

    def __init__(self, movableObject):
        self._movableObject = movableObject

    def detectCollisionWith(self, anotherObject):
        collision = Collision()

        if anotherObject is None or anotherObject is self._movableObject:
            return False

        self.__detectVerticalIntersection(collision, self._movableObject.rectangle, anotherObject.rectangle)
        self.__detectHorizontalIntersection(collision, self._movableObject.rectangle, anotherObject.rectangle)

        return collision

    # noinspection PyChainedComparisons
    @staticmethod
    def __detectVerticalIntersection(collision, A, B):
        if A.top >= B.top and A.bottom >= B.bottom and A.bottom <= B.top:
            collision.verticalIntersection = True
            collision.topIntersection = True
        elif A.top <= B.top and A.bottom >= B.bottom:
            collision.verticalIntersection = True
        elif A.top <= B.top and A.bottom <= B.bottom and A.top >= B.bottom:
            collision.verticalIntersection = True
            collision.bottomIntersection = True

    # noinspection PyChainedComparisons
    @staticmethod
    def __detectHorizontalIntersection(collision, A, B):
        if A.left <= B.left and A.right <= B.right and B.left <= A.right:
            collision.horizontalIntersection = True
            collision.leftIntersection = True
        elif A.left >= B.left and A.right <= B.right:
            collision.horizontalIntersection = True
        elif A.left >= B.left and A.right >= B.right and A.left <= B.right:
            collision.horizontalIntersection = True
            collision.rightIntersection = True
