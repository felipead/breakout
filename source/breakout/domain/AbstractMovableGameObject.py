from breakout.domain.AbstractGameObject import AbstractGameObject
from breakout.geometry.Vector import Vector


class AbstractMovableGameObject(AbstractGameObject):

    def __init__(self, engine, position, speed=None):
        AbstractGameObject.__init__(self, engine, position)
        if speed is None:
            self.speed = Vector((0,0))
        else:
            self.speed = speed

    def __str__(self):
        return "MovableGameObject {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"
