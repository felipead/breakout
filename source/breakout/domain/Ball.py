import random
from pygame.mixer import Sound

from breakout.domain.MovableGameObject import MovableGameObject
from breakout.geometry.Rectangle import Rectangle
from breakout.util.DrawingUtil import *

_SOUND_FILE_COLLISION_BALL_WITH_WALL = 'breakout/resources/sounds/Pop.wav'
_SOUND_FILE_COLLISION_BALL_WITH_BALL = 'breakout/resources/sounds/Bottle.wav'
_SOUND_FILE_COLLISION_BALL_WITH_BLOCK = 'breakout/resources/sounds/Tuntz.wav'
_SOUND_FILE_COLLISION_BALL_WITH_PADDLE = 'breakout/resources/sounds/Ping.wav'
_SOUND_FILE_BALL_DESTROYED = 'breakout/resources/sounds/Basso.wav'

_COLLISION_BALL_WALL = 1
_COLLISION_BALL_BALL = 2
_COLLISION_BALL_BLOCK = 4
_COLLISION_BALL_PADDLE = 8

class Ball(MovableGameObject):

    def __init__(self, engine, position, speed, radius):
        MovableGameObject.__init__(self, engine, position, speed)
        self.radius = radius

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

    def update(self, milliseconds, tick):
        self.position.x += self.speed.x * milliseconds
        self.position.y += self.speed.y * milliseconds

        self.__detectAndProcessCollisions()

        # Check if the ball crossed the bottom screen edge (in this case, the ball should be
        # destroyed, and the game status updated)
        screenRect = self.engine.boundaries
        thisRect = self.boundaries
        if thisRect.bottom < (screenRect.bottom):
            self.__soundBallDestroyed.play()
            self.engine.destroyBall(self)

    def __detectAndProcessCollisions(self):
        collisionType = None
        
        # Check if the ball collides with the paddle
        collision = self.__processObjectCollision(self.engine.paddle)
        if collision:
            self.speed.y = abs(self.speed.y)
            collisionType = _COLLISION_BALL_PADDLE
        
        # Check if the ball collides with the top, left or right screen edges, in which case
        # the ball should be repelled. If the ball cross the bottom screen edge, it
        # should be destroyed (this case will not be checked here).
        if collisionType == None:
            screenRect = self.engine.boundaries
            thisRect = self.boundaries
            if thisRect.left <= screenRect.left:
                self.speed.x = abs(self.speed.x)
                collisionType = _COLLISION_BALL_WALL
            elif thisRect.right >= screenRect.right:
                self.speed.x = -abs(self.speed.x)
                collisionType = _COLLISION_BALL_WALL
            elif thisRect.top >= screenRect.top:
                self.speed.y = -abs(self.speed.y)
                collisionType = _COLLISION_BALL_WALL
            
        # Check if the ball collides with a block
        if collisionType == None:
            for block in self.engine.blocks:
                collision = self.__processObjectCollision(block)
                if collision:
                    collisionType = _COLLISION_BALL_BLOCK
                    self.engine.destroyBlock(block)
                    break

        # Check if the ball collides with another ball
        if collisionType == None:
             for ball in self.engine.balls:
                 if ball is not self:
                     collision = self.__processObjectCollision(ball)
                     if collision:
                         collisionType = _COLLISION_BALL_BALL
                         break
                         

        # If a collision occurred, process it
        if collisionType != None:
            if collisionType == _COLLISION_BALL_WALL:
                self.__soundCollisionBallWithWall.play()
            if collisionType == _COLLISION_BALL_BLOCK:
                self.__soundCollisionBallWithBlock.play()
            if collisionType == _COLLISION_BALL_PADDLE:
                self.__soundCollisionBallWithPaddle.play()
            if collisionType == _COLLISION_BALL_BALL:
                self.__soundCollisionBallWithBall.play()
            return True
        else:
            return False

    def __processObjectCollision(self, obj):
        if obj == None:
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

    def display(self, milliseconds, tick):
        colorTone = 0.1 * (tick % 10)
        if colorTone > 1:
            colorTone = 1

        x = self.position.x
        y = self.position.y

        color = (colorTone, 0, 1 - colorTone)
        DrawingUtil.drawCircle2d(x, y, self.radius, color)

    def __str__(self):
        return "Ball {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"
