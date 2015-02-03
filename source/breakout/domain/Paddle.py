from OpenGL.GL import *

from breakout.domain.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle

_PADDLE_HEIGHT = 5.0

_PADDLE_VERTICAL_BORDER = 1
_PADDLE_HORIZONTAL_BORDER = 2

class Paddle(AbstractMovableGameObject):

    def __init__(self, engine, position = None, speed = None, width = 40):
        AbstractMovableGameObject.__init__(self, engine, position, speed)
        self._width = width
        self._height = _PADDLE_HEIGHT

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def boundaries(self):
        left = self.position.x - self._width/2.0
        right = self.position.x + self._width/2.0
        bottom = self.position.y - self._height/2.0
        top = self.position.y + self._height/2.0
        return Rectangle(left, bottom, right, top)

    def update(self, milliseconds, tick):
        self.position.x += self.speed.x * milliseconds
        self.__checkBoundaries()

    def __checkBoundaries(self):
        screenRectangle = self.engine.boundaries
        thisRectangle = self.boundaries
        if thisRectangle.left <= screenRectangle.left:
            self.position.x = screenRectangle.left + self._width / 2.0
            self.speed.x = 0
        elif thisRectangle.right >= screenRectangle.right:
            self.position.x = screenRectangle.right - self._width / 2.0
            self.speed.x = 0

    def display(self, milliseconds, tick):
        colorTone = 0.1 * (tick % 10)
        if colorTone > 1:
            colorTone = 1

        x = self.position.x
        y = self.position.y
        dy = self._height/2 - _PADDLE_VERTICAL_BORDER
        dx = self._width/2 - _PADDLE_HORIZONTAL_BORDER

        self.__drawOuterRectangle(colorTone, x, y, dx, dy, _PADDLE_HORIZONTAL_BORDER, _PADDLE_VERTICAL_BORDER)
        self.__drawInnerRectangle(colorTone, x, y, dx, dy)

    @staticmethod
    def __drawOuterRectangle(colorTone, x, y, dx, dy, horizontalBorder, verticalBorder):
        glBegin(GL_POLYGON)
        glColor(1 - colorTone, 1 - colorTone, 1 - colorTone)
        glVertex(x - (dx + horizontalBorder), y + (dy + verticalBorder))
        glVertex(x + (dx + horizontalBorder), y + (dy + verticalBorder))
        glVertex(x + (dx + horizontalBorder), y - (dy + verticalBorder))
        glVertex(x - (dx + horizontalBorder), y - (dy + verticalBorder))
        glEnd()

    @staticmethod
    def __drawInnerRectangle(colorTone, x, y, dx, dy):
        glBegin(GL_POLYGON)
        glColor(colorTone, 0.0, 0.0)
        glVertex(x - dx, y + dy)
        glVertex(x + dx, y + dy)
        glVertex(x + dx, y - dy)
        glVertex(x - dx, y - dy)
        glEnd()

    def __str__(self):
        return "Paddle {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"