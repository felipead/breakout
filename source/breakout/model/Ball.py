import random
from enum import IntEnum

from pygame.mixer import Sound

from breakout.model.AbstractMovableGameObject import AbstractMovableGameObject
from breakout.geometry.Rectangle import Rectangle
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
        self.radius = radius
        self.color = color
        self.__soundCollisionBallWithWall = Sound(_SOUND_FILE_COLLISION_BALL_WITH_WALL)
        self.__soundCollisionBallWithBall = Sound(_SOUND_FILE_COLLISION_BALL_WITH_BALL)
        self.__soundCollisionBallWithBlock = Sound(_SOUND_FILE_COLLISION_BALL_WITH_BLOCK)
        self.__soundCollisionBallWithPaddle = Sound(_SOUND_FILE_COLLISION_BALL_WITH_PADDLE)
        self.__soundBallDestroyed = Sound(_SOUND_FILE_BALL_DESTROYED)

    @property
    def boundaries(self):
        left = self.position.x - self.radius
        right = self.position.x + self.radius
        bottom = self.position.y - self.radius
        top = self.position.y + self.radius
        return Rectangle(left, bottom, right, top)


    def display(self, milliseconds, tick):
        self.__drawPolygons(tick)

    def __drawPolygons(self, tick):
        brightness = float(tick % _COLOR_BRIGHTNESS_FREQUENCY) / _COLOR_BRIGHTNESS_FREQUENCY
        if brightness > 1:
            brightness = 1
        baseColor = self.color.value

        x = self.position.x
        y = self.position.y
        rotation = (tick % _POLYGON_ROTATION_FREQUENCY) / float(_POLYGON_ROTATION_FREQUENCY)
        radiansOffset = (_CIRCLE_LENGTH / float(_POLYGON_EDGES)) * rotation

        outerCircleColor = tuple(i * (1 - brightness) for i in baseColor)
        Drawing.drawCircle2d(x, y, self.radius, outerCircleColor, _POLYGON_EDGES, radiansOffset)

        middleCircleColor = tuple(i * brightness for i in baseColor)
        Drawing.drawCircle2d(x, y, self.radius * 0.75, middleCircleColor, _POLYGON_EDGES, radiansOffset)

        innerCircleColor = tuple(i * (1 - brightness) for i in baseColor)
        Drawing.drawCircle2d(x, y, self.radius * 0.50, innerCircleColor, _POLYGON_EDGES, radiansOffset)


    def update(self, milliseconds, tick):
        self.position.x += self.speed.x * milliseconds
        self.position.y += self.speed.y * milliseconds

        self.__detectCollisions()
        self.__checkIfBallCrossedBottomBoundary()


    def __checkIfBallCrossedBottomBoundary(self):
        screenRectangle = self.engine.boundaries
        thisRectangle = self.boundaries
        if thisRectangle.bottom < screenRectangle.bottom:
            self.__soundBallDestroyed.play()
            self.engine.destroyBall(self)


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
        collision = self.__detectCollisionWithObject(self.engine.paddle)
        if collision:
            self.speed.y = abs(self.speed.y)
            return _CollisionType.PADDLE
        return None

    def __detectCollisionWithBlock(self):
        for block in self.engine.blocks:
            if self.__detectCollisionWithObject(block):
                self.engine.destroyBlock(block)
                return _CollisionType.BLOCK

        return None

    def __detectCollisionWithAnotherBall(self):
        for ball in self.engine.balls:
            if ball is not self:
                if self.__detectCollisionWithObject(ball):
                    return  _CollisionType.BALL

        return None

    def __detectCollisionWithWallEdges(self):
        screenRectangle = self.engine.boundaries
        thisRectangle = self.boundaries

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

    def __detectCollisionWithObject(self, obj):
        if obj is None:
            return False
        if obj == self:
            return False
            
        A = self.boundaries # A is this object rectangle
        B = obj.boundaries # B is target object rectangle
    
        verticalIntersection = False
        topIntersection = False
        bottomIntersection = False
        
        # Checks for vertical intersections
        if A.top >= B.top and A.bottom >= B.bottom and A.bottom <= B.top:
            verticalIntersection = True
            topIntersection = True
        elif A.top <= B.top and A.bottom >= B.bottom:
            verticalIntersection = True
        elif A.top <= B.top and A.bottom <= B.bottom and A.top >= B.bottom:
            verticalIntersection = True
            bottomIntersection = True
            
        horizontalIntersection = False
        leftIntersection = False
        rightIntersection = False
            
        # Checks for horizontal intersections
        if A.left <= B.left and A.right <= B.right and B.left <= A.right:
            horizontalIntersection = True
            leftIntersection = True
        elif A.left >= B.left and A.right <= B.right:
            horizontalIntersection = True
        elif A.left >= B.left and A.right >= B.right and A.left <= B.right:
            horizontalIntersection = True
            rightIntersection = True
        
        collision = (horizontalIntersection and verticalIntersection)
        
        if collision:
            if leftIntersection:
                self.speed.x = -abs(self.speed.x)
            elif rightIntersection:
                self.speed.x = abs(self.speed.x)
                
            if topIntersection:
                self.speed.y = abs(self.speed.y)
            elif bottomIntersection:
                self.speed.y = -abs(self.speed.y)

            if not (leftIntersection or rightIntersection or topIntersection or bottomIntersection):
                # Avoids dead-locks by choosing a random direction
                self.speed.x = abs(self.speed.x) * random.choice([-1, 1])
                self.speed.y = abs(self.speed.y) * random.choice([-1, 1])
            
        return collision


    def __str__(self):
        return "Ball {Position: " + str(self.position) + ", Speed: " + str(self.speed) + ", Color: " + str(self.color) + ", Radius: " + str(self.radius) + "}"
