from OpenGL.GL import *

from breakout.domain.AbstractGameObject import AbstractGameObject
from breakout.domain.Color import Color
from breakout.geometry.Rectangle import Rectangle


_BLOCK_POINTS_BLUE = 10
_BLOCK_POINTS_GREEN = 20
_BLOCK_POINTS_RED = 30

_DEFAULT_BLOCK_HEIGHT = 10
_DEFAULT_BLOCK_WIDTH = 20


class Block(AbstractGameObject):

    def __init__(self, engine, position, color, width=_DEFAULT_BLOCK_WIDTH, height=_DEFAULT_BLOCK_HEIGHT):
        AbstractGameObject.__init__(self, engine, position)
        self.width = width
        self.height = height
        self.color = color

    @property
    def points(self):
        if self.color == Color.BLUE:
            return _BLOCK_POINTS_BLUE
        elif self.color == Color.GREEN:
            return _BLOCK_POINTS_GREEN
        elif self.color == Color.RED:
            return _BLOCK_POINTS_RED
        else:
            raise Exception("Color not supported.")

    @property
    def boundaries(self):
        left = self.position.x - self.width/2.0
        right = self.position.x + self.width/2.0
        top = self.position.y + self.height/2.0
        bottom = self.position.y - self.height/2.0
        return Rectangle(left, bottom, right, top)

    def update(self, milliseconds, tick):
        pass

    def display(self, milliseconds, tick):
        colorBrightness = 0.1 * (tick % 10)
        if colorBrightness > 1:
            colorBrightness = 1

        verticalBorder = 1
        horizontalBorder = 2

        x = self.position.x
        y = self.position.y
        dy = self.height/2.0 - verticalBorder
        dx = self.width/2.0 - horizontalBorder

        self.__drawOuterRectangle(colorBrightness, x, y, dx, dy, horizontalBorder, verticalBorder)
        self.__drawInnerRectangle(colorBrightness, x, y, dx, dy)

    def __drawOuterRectangle(self, colorBrightness, x, y, dx, dy, horizontalBorder, verticalBorder):
        glColor(1 - colorBrightness, 1 - colorBrightness, 1 - colorBrightness)
        glBegin(GL_POLYGON)
        glVertex(x - (dx + horizontalBorder), y + (dy + verticalBorder))
        glVertex(x + (dx + horizontalBorder), y + (dy + verticalBorder))
        glVertex(x + (dx + horizontalBorder), y - (dy + verticalBorder))
        glVertex(x - (dx + horizontalBorder), y - (dy + verticalBorder))
        glEnd()

    def __drawInnerRectangle(self, colorBrightness, x, y, dx, dy):
        rgb = self.color.value
        glColor(rgb[0] * colorBrightness, rgb[1] * colorBrightness, rgb[2] * colorBrightness)

        glBegin(GL_POLYGON)
        glVertex(x - dx, y + dy)
        glVertex(x + dx, y + dy)
        glVertex(x + dx, y - dy)
        glVertex(x - dx, y - dy)
        glEnd()

    def __str__(self):
        return "Block {Position: " + str(self.position) + ", Points: " + str(self.points) + "}"
