from breakout.domain.GameObject import GameObject
from breakout.geometry.Vector import Vector


# Abstract class
class MovableGameObject(GameObject):

    def __init__(self, engine, position, speed=None):
        GameObject.__init__(self, engine, position)
        if speed is None:
            self.speed = Vector((0,0))
        else:
            self.speed = speed

    def __str__(self):
        return "MovableGameObject {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"
