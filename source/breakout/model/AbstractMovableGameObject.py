from breakout.model.AbstractGameObject import AbstractGameObject
from breakout.geometry.Vector import Vector


class AbstractMovableGameObject(AbstractGameObject):

    def __init__(self, engine, position=None, speed=None):
        AbstractGameObject.__init__(self, engine, position)
        if speed is None:
            self._speed = Vector((0,0))
        else:
            self._speed = speed

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = value

    def __str__(self):
        return "MovableGameObject {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"
