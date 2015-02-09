from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.model.Color import Color
from breakout.util.Drawing import Drawing

_HEIGHT = 5.0
_VERTICAL_BORDER = 0
_HORIZONTAL_BORDER = 2
_INNER_COLOR = Color.RED
_OUTER_COLOR = Color.GRAY
_COLOR_BRIGHTNESS_FREQUENCY = 30

class Paddle(AbstractMovableGameObject):

    def __init__(self, engine, position=None, speed=None, width=40):
        AbstractMovableGameObject.__init__(self, engine, position, speed)
        self._width = width
        self._height = _HEIGHT
        self._rectangle = None
        self.__rebuildRectangle()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

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
    def rectangle(self):
        return self._rectangle

    def update(self, milliseconds, tick):
        self.position.x += self.speed.x * milliseconds
        self.__rebuildRectangle()
        self.__checkBoundaries()

    def __checkBoundaries(self):
        screenRectangle = self._engine.rectangle
        thisRectangle = self.rectangle
        if thisRectangle.left <= screenRectangle.left:
            self.position.x = screenRectangle.left + self._width / 2.0
            self.speed.x = 0
        elif thisRectangle.right >= screenRectangle.right:
            self.position.x = screenRectangle.right - self._width / 2.0
            self.speed.x = 0

    def display(self, milliseconds, tick):
        colorBrightness = float(tick % _COLOR_BRIGHTNESS_FREQUENCY)/_COLOR_BRIGHTNESS_FREQUENCY
        if colorBrightness > 1:
            colorBrightness = 1

        x = self.position.x
        y = self.position.y
        dy = float(self._height)/2
        dx = float(self._width)/2

        self.__drawOuterRectangle(colorBrightness, x, y, dx, dy)
        self.__drawInnerRectangle(colorBrightness, x, y, dx, dy)

    def __drawOuterRectangle(self, colorBrightness, x, y, dx, dy):
        outerColor = tuple(i * (1-colorBrightness) for i in _OUTER_COLOR.value)
        Drawing.drawRectangle2d(x, y, dx, dy, outerColor)

    def __drawInnerRectangle(self, colorBrightness, x, y, dx, dy):
        innerColor = tuple(i * colorBrightness for i in _INNER_COLOR.value)
        Drawing.drawRectangle2d(x, y, dx - _HORIZONTAL_BORDER, dy - _VERTICAL_BORDER, innerColor)

    def __rebuildRectangle(self):
        left = self.position.x - self.width/2.0
        right = self.position.x + self.width/2.0
        top = self.position.y + self.height/2.0
        bottom = self.position.y - self.height/2.0
        self._rectangle = Rectangle(left, bottom, right, top)

    def __str__(self):
        return "Paddle {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"