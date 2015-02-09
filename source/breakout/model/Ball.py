import math

from enum import IntEnum, Enum

from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.model.SoundPlayer import SoundPlayer
from breakout.model.collision.CollisionDetector import CollisionDetector
from breakout.model.Color import Color
from breakout.util.Drawing import Drawing


_POLYGON_EDGES = 6
_POLYGON_ROTATION_FREQUENCY = 15
_CIRCLE_LENGTH = 2 * math.pi

_COLOR_BRIGHTNESS_FREQUENCY = 30
_DEFAULT_COLOR = Color.WHITE
_DEFAULT_RADIUS = 4


class _SoundFile(Enum):
    COLLISION_WITH_WALL = 'breakout/resources/sounds/Silence.wav'
    COLLISION_WITH_BALL = 'breakout/resources/sounds/Bottle.wav'
    COLLISION_WITH_BLOCK = 'breakout/resources/sounds/Tuntz.wav'
    COLLISION_WITH_PADDLE = 'breakout/resources/sounds/Ping.wav'
    BALL_DESTROYED = 'breakout/resources/sounds/Hero.wav'

class _CollisionType(IntEnum):
    WALL = 1
    BALL = 2
    BLOCK = 4
    PADDLE = 8


class Ball(AbstractMovableGameObject):

    def __init__(self, engine, position=None, speed=None, color=_DEFAULT_COLOR, radius=_DEFAULT_RADIUS):
        AbstractMovableGameObject.__init__(self, engine, position, speed)
        self._radius = radius
        self._color = color
        self._collisionDetector = CollisionDetector(self)
        self._soundPlayer = SoundPlayer()

    @property
    def radius(self):
        return self._radius

    @property
    def color(self):
        return self._color

    @property
    def rectangle(self):
        left = self.position.x - self._radius
        right = self.position.x + self._radius
        bottom = self.position.y - self._radius
        top = self.position.y + self._radius
        return Rectangle(left, bottom, right, top)


    def display(self, milliseconds, tick):
        self.__drawPolygons(tick)

    def __drawPolygons(self, tick):
        colorBrightness = float(tick % _COLOR_BRIGHTNESS_FREQUENCY) / _COLOR_BRIGHTNESS_FREQUENCY
        if colorBrightness > 1:
            colorBrightness = 1
        baseColor = self._color.value

        x = self.position.x
        y = self.position.y
        rotation = (tick % _POLYGON_ROTATION_FREQUENCY) / float(_POLYGON_ROTATION_FREQUENCY)
        radiansOffset = (_CIRCLE_LENGTH / float(_POLYGON_EDGES)) * rotation

        outerCircleColor = tuple(i * (1 - colorBrightness) for i in baseColor)
        Drawing.drawCircle2d(x, y, self._radius, outerCircleColor, _POLYGON_EDGES, radiansOffset)

        middleCircleColor = tuple(i * colorBrightness for i in baseColor)
        Drawing.drawCircle2d(x, y, self._radius * 0.75, middleCircleColor, _POLYGON_EDGES, radiansOffset)

        innerCircleColor = tuple(i * (1 - colorBrightness) for i in baseColor)
        Drawing.drawCircle2d(x, y, self._radius * 0.50, innerCircleColor, _POLYGON_EDGES, radiansOffset)


    def update(self, milliseconds, tick):
        self.position.x += self.speed.x * milliseconds
        self.position.y += self.speed.y * milliseconds

        self.__detectCollisions()
        self.__checkIfBallCrossedBottomBoundary()


    def __checkIfBallCrossedBottomBoundary(self):
        screenRectangle = self._engine.rectangle
        thisRectangle = self.rectangle
        if thisRectangle.bottom < screenRectangle.bottom:
            self._engine.destroyBall(self)
            self._soundPlayer.play(_SoundFile.BALL_DESTROYED.value)


    def __detectCollisions(self):
        collisionType = self.__detectCollisionWithPaddle()
        if collisionType is None:
            collisionType = self.__detectCollisionWithWallEdges()
        if collisionType is None:
            collisionType = self.__detectCollisionWithBlock()
        if collisionType is None:
            collisionType = self.__detectCollisionWithAnotherBall()

        self.__playCollisionSound(collisionType)

        return collisionType

    def __detectCollisionWithPaddle(self):
        collision = self.__detectCollisionWith(self._engine.paddle)
        if collision.happened:
            self.speed.y = abs(self.speed.y)
            return _CollisionType.PADDLE
        return None

    def __detectCollisionWithBlock(self):
        for block in self._engine.blocks:
            collision = self.__detectCollisionWith(block)
            if collision.happened:
                self._engine.destroyBlock(block)
                return _CollisionType.BLOCK

        return None

    def __detectCollisionWithAnotherBall(self):
        for ball in self._engine.balls:
            if ball is not self:
                collision = self.__detectCollisionWith(ball)
                if collision.happened:
                    return  _CollisionType.BALL

        return None

    def __detectCollisionWithWallEdges(self):
        screenRectangle = self._engine.rectangle
        thisRectangle = self.rectangle

        if thisRectangle.left <= screenRectangle.left:
            self.speed.x = abs(self.speed.x)
            return _CollisionType.WALL
        elif thisRectangle.right >= screenRectangle.right:
            self.speed.x = -abs(self.speed.x)
            return _CollisionType.WALL
        elif thisRectangle.top >= screenRectangle.top:
            self.speed.y = -abs(self.speed.y)
            return _CollisionType.WALL

        return None

    def __detectCollisionWith(self, anotherObject):
        collision = self._collisionDetector.detectCollisionWithObject(anotherObject)
        if collision.happened:
            collision.apply(self)
        return collision

    def __playCollisionSound(self, collisionType):
        if collisionType is not None:
            if collisionType == _CollisionType.WALL:
                self._soundPlayer.play(_SoundFile.COLLISION_WITH_WALL.value)
            if collisionType == _CollisionType.BLOCK:
                self._soundPlayer.play(_SoundFile.COLLISION_WITH_BLOCK.value)
            if collisionType == _CollisionType.PADDLE:
                self._soundPlayer.play(_SoundFile.COLLISION_WITH_PADDLE.value)
            if collisionType == _CollisionType.BALL:
                self._soundPlayer.play(_SoundFile.COLLISION_WITH_BALL.value)

    def __str__(self):
        return "Ball {Position: " + str(self.position) + ", Speed: " + str(self.speed) + ", Color: " + str(self._color) + ", Radius: " + str(self._radius) + "}"
