import random

_RANDOM_CHOICE_RANGE = (-1, 1)


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

    def apply(self, movableObject):
        if self.happened:
            self.__applyHorizontalImpact(movableObject)
            self.__applyVerticalImpact(movableObject)

            if not (self.hasLeftIntersection or self.hasRightIntersection or self.hasTopIntersection or self.hasBottomIntersection):
                # Avoids dead-locks by choosing a random direction
                movableObject.speed.x = abs(movableObject.speed.x) * random.choice(_RANDOM_CHOICE_RANGE)
                movableObject.speed.y = abs(movableObject.speed.y) * random.choice(_RANDOM_CHOICE_RANGE)

    def __applyHorizontalImpact(self, movableObject):
        if self.hasLeftIntersection:
            movableObject.speed.x = -abs(movableObject.speed.x)
        elif self.hasRightIntersection:
            movableObject.speed.x = abs(movableObject.speed.x)

    def __applyVerticalImpact(self, movableObject):
        if self.hasTopIntersection:
            movableObject.speed.y = abs(movableObject.speed.y)
        elif self.hasBottomIntersection:
            movableObject.speed.y = -abs(movableObject.speed.y)