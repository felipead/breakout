import random

_RANDOM_CHOICE_RANGE = (-1, 1)


class Collision(object):

    def __init__(self):
        self.leftIntersection = False
        self.rightIntersection = False
        self.topIntersection = False
        self.bottomIntersection = False
        self.horizontalIntersection = False
        self.verticalIntersection = False

    @property
    def happened(self):
        return self.horizontalIntersection and self.verticalIntersection

    def apply(self, movableObject):
        if self.happened:
            self.__applyHorizontalImpact(movableObject)
            self.__applyVerticalImpact(movableObject)

            if not (self.leftIntersection or self.rightIntersection or self.topIntersection or self.bottomIntersection):
                # Avoids dead-locks by choosing a random direction
                movableObject.speed.x = abs(movableObject.speed.x) * random.choice(_RANDOM_CHOICE_RANGE)
                movableObject.speed.y = abs(movableObject.speed.y) * random.choice(_RANDOM_CHOICE_RANGE)

    def __applyHorizontalImpact(self, movableObject):
        if self.leftIntersection:
            movableObject.speed.x = -abs(movableObject.speed.x)
        elif self.rightIntersection:
            movableObject.speed.x = abs(movableObject.speed.x)

    def __applyVerticalImpact(self, movableObject):
        if self.topIntersection:
            movableObject.speed.y = abs(movableObject.speed.y)
        elif self.bottomIntersection:
            movableObject.speed.y = -abs(movableObject.speed.y)