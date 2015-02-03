from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.model.Color import Color
from breakout.util.Drawing import Drawing

_PADDLE_HEIGHT = 5.0

_PADDLE_VERTICAL_BORDER = 0.5
_PADDLE_HORIZONTAL_BORDER = 1
_PADDLE_COLOR = Color.RED

class Paddle(AbstractMovableGameObject):

    def __init__(self, engine, position=None, speed=None, width=40, color=Color.RED):
        AbstractMovableGameObject.__init__(self, engine, position, speed)
        self._width = width
        self._height = _PADDLE_HEIGHT
        self._color = Color.RED

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
        brightness = 0.1 * (tick % 10)
        if brightness > 1:
            brightness = 1

        x = self.position.x
        y = self.position.y
        dy = self._height/2 - _PADDLE_VERTICAL_BORDER
        dx = self._width/2 - _PADDLE_HORIZONTAL_BORDER

        self.__drawOuterRectangle(brightness, x, y, dx, dy, _PADDLE_HORIZONTAL_BORDER, _PADDLE_VERTICAL_BORDER)
        self.__drawInnerRectangle(self._color, brightness, x, y, dx, dy)

    @staticmethod
    def __drawOuterRectangle(brightness, x, y, dx, dy, horizontalBorder, verticalBorder):
        rgbColor = (1 - brightness, 1 - brightness, 1 - brightness)
        a = (x - (dx + horizontalBorder), y + (dy + verticalBorder))
        b = (x + (dx + horizontalBorder), y + (dy + verticalBorder))
        c = (x + (dx + horizontalBorder), y - (dy + verticalBorder))
        d = (x - (dx + horizontalBorder), y - (dy + verticalBorder))
        Drawing.drawRectangle2d(a, b, c, d, rgbColor)

    @staticmethod
    def __drawInnerRectangle(color, brightness, x, y, dx, dy):
        rgbColor = (color.value[0] * brightness, color.value[1] * brightness, color.value[2] * brightness)
        a = (x - dx, y + dy)
        b = (x + dx, y + dy)
        c = (x + dx, y - dy)
        d = (x - dx, y - dy)
        Drawing.drawRectangle2d(a, b, c, d, rgbColor)

    def __str__(self):
        return "Paddle {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"