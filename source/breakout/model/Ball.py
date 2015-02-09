from enum import IntEnum

from pygame.mixer import Sound

from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.model.CollisionDetector import CollisionDetector
from breakout.model.Color import Color
from breakout.util.Drawing import *


_SOUND_FILE_COLLISION_BALL_WITH_WALL = 'breakout/resources/sounds/Pop.wav'
_SOUND_FILE_COLLISION_BALL_WITH_BALL = 'breakout/resources/sounds/Bottle.wav'
_SOUND_FILE_COLLISION_BALL_WITH_BLOCK = 'breakout/resources/sounds/Tuntz.wav'
_SOUND_FILE_COLLISION_BALL_WITH_PADDLE = 'breakout/resources/sounds/Ping.wav'
_SOUND_FILE_BALL_DESTROYED = 'breakout/resources/sounds/Basso.wav'

_COLOR_BRIGHTNESS_FREQUENCY = 25

_POLYGON_EDGES = 6
_POLYGON_ROTATION_FREQUENCY = 20
_CIRCLE_LENGTH = 2 * math.pi

_DEFAULT_COLOR = Color.WHITE
_DEFAULT_RADIUS = 4


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
        self.__soundCollisionBallWithWall = Sound(_SOUND_FILE_COLLISION_BALL_WITH_WALL)
        self.__soundCollisionBallWithBall = Sound(_SOUND_FILE_COLLISION_BALL_WITH_BALL)
        self.__soundCollisionBallWithBlock = Sound(_SOUND_FILE_COLLISION_BALL_WITH_BLOCK)
        self.__soundCollisionBallWithPaddle = Sound(_SOUND_FILE_COLLISION_BALL_WITH_PADDLE)
        self.__soundBallDestroyed = Sound(_SOUND_FILE_BALL_DESTROYED)

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
        brightness = float(tick % _COLOR_BRIGHTNESS_FREQUENCY) / _COLOR_BRIGHTNESS_FREQUENCY
        if brightness > 1:
            brightness = 1
        baseColor = self._color.value

        x = self.position.x
        y = self.position.y
        rotation = (tick % _POLYGON_ROTATION_FREQUENCY) / float(_POLYGON_ROTATION_FREQUENCY)
        radiansOffset = (_CIRCLE_LENGTH / float(_POLYGON_EDGES)) * rotation

        outerCircleColor = tuple(i * (1 - brightness) for i in baseColor)
        Drawing.drawCircle2d(x, y, self._radius, outerCircleColor, _POLYGON_EDGES, radiansOffset)

        middleCircleColor = tuple(i * brightness for i in baseColor)
        Drawing.drawCircle2d(x, y, self._radius * 0.75, middleCircleColor, _POLYGON_EDGES, radiansOffset)

        innerCircleColor = tuple(i * (1 - brightness) for i in baseColor)
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
            self.__soundBallDestroyed.play()
            self._engine.destroyBall(self)


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
        collision = self._collisionDetector.detectCollisionWith(anotherObject)
        if collision.happened:
            collision.apply(self)
        return collision

    def __playCollisionSound(self, collisionType):
        if collisionType is not None:
            if collisionType == _CollisionType.WALL:
                self.__soundCollisionBallWithWall.play()
            if collisionType == _CollisionType.BLOCK:
                self.__soundCollisionBallWithBlock.play()
            if collisionType == _CollisionType.PADDLE:
                self.__soundCollisionBallWithPaddle.play()
            if collisionType == _CollisionType.BALL:
                self.__soundCollisionBallWithBall.play()

    def __str__(self):
        return "Ball {Position: " + str(self.position) + ", Speed: " + str(self.speed) + ", Color: " + str(self._color) + ", Radius: " + str(self._radius) + "}"
