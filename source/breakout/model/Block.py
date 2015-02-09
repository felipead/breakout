from breakout.model.AbstractGameObject import AbstractGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.util.Drawing import Drawing

_COLOR_BRIGHTNESS_FREQUENCY = 30

_VERTICAL_BORDER = 0.5
_HORIZONTAL_BORDER = 0.5


class Block(AbstractGameObject):

    def __init__(self, engine, blockColor, width, height, position=None):
        AbstractGameObject.__init__(self, engine, position)
        self._width = width
        self._height = height
        self._blockColor = blockColor
        self._rectangle = None
        self.__rebuildRectangle()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self.__rebuildRectangle()

    @property
    def rectangle(self):
        return self._rectangle

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def color(self):
        return self._blockColor.value.color

    @property
    def points(self):
        return self._blockColor.value.points

    def __rebuildRectangle(self):
        left = self.position.x - self.width/2.0
        right = self.position.x + self.width/2.0
        top = self.position.y + self.height/2.0
        bottom = self.position.y - self.height/2.0
        self._rectangle = Rectangle(left, bottom, right, top)

    def update(self, milliseconds, tick):
        pass

    def display(self, milliseconds, tick):
        colorBrightness = (tick % _COLOR_BRIGHTNESS_FREQUENCY)/float(_COLOR_BRIGHTNESS_FREQUENCY)
        if colorBrightness > 1:
            colorBrightness = 1

        x = self.position.x
        y = self.position.y
        dy = self.height/2.0
        dx = self.width/2.0

        self.__drawOuterRectangle(x, y, dx, dy, colorBrightness)
        self.__drawInnerRectangle(x, y, dx, dy, colorBrightness)

    def __drawOuterRectangle(self, x, y, dx, dy, colorBrightness):
        outerColor = tuple(i * (1 - colorBrightness) for i in self.color.value)
        Drawing.drawRectangle2d(x, y, dx, dy, outerColor)

    def __drawInnerRectangle(self, x, y, dx, dy, colorBrightness):
        innerColor = tuple(i * colorBrightness for i in self.color.value)
        Drawing.drawRectangle2d(x, y, dx - _HORIZONTAL_BORDER, dy - _VERTICAL_BORDER, innerColor)

    def __str__(self):
        return "Block {Color: " + str(self._blockColor) + ", Position: " + str(self.position) + "}"
