from ..geometry.Vector import *

class GameObject:

    def __init__(self, game, position = Vector((0,0))):
        self.game = game
        self.position = position

    def __str__(self):
        return "GameObject {Position: " + str(self.position) + "}"
