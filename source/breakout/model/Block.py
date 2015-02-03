from breakout.model.AbstractGameObject import AbstractGameObject
from breakout.model.Color import Color
from breakout.geometry.Rectangle import Rectangle
from breakout.util.Drawing import Drawing


_BLOCK_POINTS_BLUE = 10
_BLOCK_POINTS_GREEN = 20
_BLOCK_POINTS_RED = 30

_DEFAULT_BLOCK_HEIGHT = 10
_DEFAULT_BLOCK_WIDTH = 20

_BLOCK_VERTICAL_BORDER = 0.5
_BLOCK_HORIZONTAL_BORDER = 1


class Block(AbstractGameObject):

    def __init__(self, engine, position, color, width=_DEFAULT_BLOCK_WIDTH, height=_DEFAULT_BLOCK_HEIGHT):
        AbstractGameObject.__init__(self, engine, position)
        self._width = width
        self._height = height
        self._color = color

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def points(self):
        if self._color == Color.BLUE:
            return _BLOCK_POINTS_BLUE
        elif self._color == Color.GREEN:
            return _BLOCK_POINTS_GREEN
        elif self._color == Color.RED:
            return _BLOCK_POINTS_RED
        else:
            raise Exception("Color not supported: " + self._color)

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
        brightness = 0.1 * (tick % 10)
        if brightness > 1:
            brightness = 1

        x = self.position.x
        y = self.position.y
        dy = self.height/2.0 - _BLOCK_VERTICAL_BORDER
        dx = self.width/2.0 - _BLOCK_HORIZONTAL_BORDER

        self.__drawOuterRectangle(brightness, x, y, dx, dy, _BLOCK_HORIZONTAL_BORDER, _BLOCK_VERTICAL_BORDER)
        self.__drawInnerRectangle(self._color, brightness, x, y, dx, dy)

    @staticmethod
    def __drawOuterRectangle(brightness, x, y, dx, dy, horizontalBorder, verticalBorder):
        color = (1 - brightness, 1 - brightness, 1 - brightness)
        a = (x - (dx + horizontalBorder), y + (dy + verticalBorder))
        b = (x + (dx + horizontalBorder), y + (dy + verticalBorder))
        c = (x + (dx + horizontalBorder), y - (dy + verticalBorder))
        d = (x - (dx + horizontalBorder), y - (dy + verticalBorder))
        Drawing.drawRectangle2d(a, b, c, d, color)

    @staticmethod
    def __drawInnerRectangle(color, brightness, x, y, dx, dy):
        brightenedColor = (color.value[0] * brightness, color.value[1] * brightness, color.value[2] * brightness)
        a = (x - dx, y + dy)
        b = (x + dx, y + dy)
        c = (x + dx, y - dy)
        d = (x - dx, y - dy)
        Drawing.drawRectangle2d(a, b, c, d, brightenedColor)

    def __str__(self):
        return "Block {Color: " + str(self._color) + ", Position: " + str(self.position) + ", Points: " + str(self.points) + "}"
