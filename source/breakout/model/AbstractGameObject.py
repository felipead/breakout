from breakout.geometry.Vector import Vector


class AbstractGameObject(object):

    def __init__(self, engine, position=None):
        if engine is None:
            raise Exception("engine can not be None")
        self._engine = engine

        if position is None:
            self._position = Vector((0,0))
        else:
            self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def rectangle(self):
        raise NotImplementedError()

    def update(self, milliseconds, tick):
        raise NotImplementedError()

    def display(self, milliseconds, tick):
        raise NotImplementedError()

    def __str__(self):
        return "GameObject {Position: " + str(self.position) + "}"
