from OpenGL.GL import *

from breakout.domain.MovableGameObject import *
from ..geometry.Rectangle import *
from ..geometry.Vector import *

PADDLE_HEIGHT = 5.0

class Paddle(MovableGameObject):

    def __init__(self, game, position, speed = Vector((0,0)), width = 40):
        MovableGameObject.__init__(self, game, position, speed)
        self.width = width
        self.height = PADDLE_HEIGHT


    @property
    def rectangle(self):
        left = self.position.x - self.width/2.0
        right = self.position.x + self.width/2.0
        bottom = self.position.y - self.height/2.0
        top = self.position.y + self.height/2.0
        return Rectangle(left, bottom, right, top)


    def update(self, milliseconds, tick):
        # Moves the paddle (horizontally only). Speed is in pixels per second.
        self.position.x += self.speed.x * milliseconds

        # Don't let the paddle cross the screen boundaries
        screenRect = self.game.boundaries
        thisRect = self.rectangle
        if thisRect.left <= screenRect.left:
            self.position.x = screenRect.left + self.width/2.0
            self.speed.x = 0
        elif thisRect.right >= screenRect.right:
            self.position.x = screenRect.right - self.width/2.0
            self.speed.x = 0


    def display(self, milliseconds, tick):
        tick = tick % 10

        colorTone = 0.1 * tick
        if colorTone > 1:
            colorTone = 1

        bv = 1
        bh = 2

        x = self.position.x
        y = self.position.y
        h = self.height/2 - bv
        w = self.width/2 - bh

        # outer rectangle
        glBegin(GL_POLYGON)
        glColor(1 - colorTone, 1 - colorTone, 1 - colorTone)
        glVertex(x - (w + bh), y + (h + bv))
        glVertex(x + (w + bh), y + (h + bv))
        glVertex(x + (w + bh), y - (h + bv))
        glVertex(x - (w + bh), y - (h + bv))
        glEnd()

        # inner rectangle
        glBegin(GL_POLYGON)
        glColor(colorTone, 0.0, 0.0)
        glVertex(x - w, y + h)
        glVertex(x + w, y + h)
        glVertex(x + w, y - h)
        glVertex(x - w, y - h)
        glEnd()

    def __str__(self):
        return "Paddle {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"