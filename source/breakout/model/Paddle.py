from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.model.Color import Color
from breakout.util.Drawing import Drawing

_HEIGHT = 5.0
_VERTICAL_BORDER = 0
_HORIZONTAL_BORDER = 2
_INNER_COLOR = Color.RED
_OUTER_COLOR = Color.GRAY
_COLOR_TONE_FREQUENCY = 25

class Paddle(AbstractMovableGameObject):

    def __init__(self, engine, position=None, speed=None, width=40):
        AbstractMovableGameObject.__init__(self, engine, position, speed)
        self._width = width
        self._height = _HEIGHT

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def rectangle(self):
        left = self.position.x - self._width/2.0
        right = self.position.x + self._width/2.0
        bottom = self.position.y - self._height/2.0
        top = self.position.y + self._height/2.0
        return Rectangle(left, bottom, right, top)

    def update(self, milliseconds, tick):
        self.position.x += self.speed.x * milliseconds
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
        colorTone = float(tick % _COLOR_TONE_FREQUENCY)/_COLOR_TONE_FREQUENCY
        if colorTone > 1:
            colorTone = 1

        x = self.position.x
        y = self.position.y
        dy = float(self._height)/2
        dx = float(self._width)/2

        self.__drawOuterRectangle(colorTone, x, y, dx, dy)
        self.__drawInnerRectangle(colorTone, x, y, dx, dy)

    def __drawOuterRectangle(self, colorTone, x, y, dx, dy):
        rgb = _OUTER_COLOR.value
        outerColor = (rgb[0] * (1 - colorTone), rgb[1] * (1 - colorTone), rgb[2] * (1 - colorTone))
        Drawing.drawRectangle2d(x, y, dx, dy, outerColor)

    def __drawInnerRectangle(self, colorTone, x, y, dx, dy):
        rgb = _INNER_COLOR.value
        innerColor = (rgb[0] * colorTone, rgb[1] * colorTone, rgb[2] * colorTone)
        Drawing.drawRectangle2d(x, y, dx - _HORIZONTAL_BORDER, dy - _VERTICAL_BORDER, innerColor)

    def __str__(self):
        return "Paddle {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"