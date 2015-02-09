import random


class CollisionWithObject(object):

    def __init__(self):
        self.hasLeftIntersection = False
        self.hasRightIntersection = False
        self.hasTopIntersection = False
        self.hasBottomIntersection = False
        self.hasHorizontalIntersection = False
        self.hasVerticalIntersection = False

    @property
    def happened(self):
        return self.hasHorizontalIntersection and self.hasVerticalIntersection

    def apply(self, movingObject):
        if self.happened:
            self.__applyHorizontalImpact(movingObject)
            self.__applyVerticalImpact(movingObject)
            self.__applyInnerImpact(movingObject)

    def __applyHorizontalImpact(self, movingObject):
        if self.hasLeftIntersection:
            movingObject.speed.x = -abs(movingObject.speed.x)
        elif self.hasRightIntersection:
            movingObject.speed.x = abs(movingObject.speed.x)

    def __applyVerticalImpact(self, movingObject):
        if self.hasTopIntersection:
            movingObject.speed.y = abs(movingObject.speed.y)
        elif self.hasBottomIntersection:
            movingObject.speed.y = -abs(movingObject.speed.y)
            
    def __applyInnerImpact(self, movingObject):
        if not (self.hasLeftIntersection or self.hasRightIntersection or self.hasTopIntersection or self.hasBottomIntersection):
            # Avoids dead-locks by choosing a random direction
            movingObject.speed.x = abs(movingObject.speed.x) * self.__chooseRandomDirection()
            movingObject.speed.y = abs(movingObject.speed.y) * self.__chooseRandomDirection()

    @staticmethod
    def __chooseRandomDirection():
        return random.choice((-1, 1))