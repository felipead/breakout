from breakout.geometry.Vector import Vector


# Abstract class
class GameObject:

    def __init__(self, engine, position=None):
        self.engine = engine

        if position is None:
            self.position = Vector((0,0))
        else:
            self.position = position

    @property
    def boundaries(self):
        raise NotImplementedError()

    def update(self, milliseconds, tick):
        raise NotImplementedError()

    def display(self, milliseconds, tick):
        raise NotImplementedError()

    def __str__(self):
        return "GameObject {Position: " + str(self.position) + "}"
