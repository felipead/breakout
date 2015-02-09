from breakout.model.collision.BoundaryEdgeType import BoundaryEdgeType


class CollisionWithBoundaryEdge(object):

    def __init__(self):
        self._type = None

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def happened(self):
        return self._type is not None

    def apply(self, movingObject):
        if self.happened:
            if self._type == BoundaryEdgeType.LEFT:
                movingObject.speed.x = abs(movingObject.speed.x)
            elif self._type == BoundaryEdgeType.RIGHT:
                movingObject.speed.x = -abs(movingObject.speed.x)
            elif self._type == BoundaryEdgeType.TOP:
                movingObject.speed.y = -abs(movingObject.speed.y)
            elif self._type == BoundaryEdgeType.BOTTOM:
                movingObject.speed.y = abs(movingObject.speed.y)