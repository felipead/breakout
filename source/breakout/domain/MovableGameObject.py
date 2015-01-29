from breakout.domain.GameObject import GameObject


class MovableGameObject(GameObject):

    def __init__(self, game, position, speed):
        GameObject.__init__(self, game, position)
        self.speed = speed
        
    def __str__(self):
        return "MovableGameObject {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"