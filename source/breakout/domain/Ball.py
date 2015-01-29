# encoding: utf-8

import random

from pygame.mixer import Sound
from OpenGL.GL import *

from breakout.domain.MovableGameObject import *
from ..geometry.Rectangle import *
from ..util.Drawing import *


FILE_SOUND_COLLISION_BALL_WALL = 'breakout/resources/sounds/Pop.wav'
FILE_SOUND_COLLISION_BALL_BALL = 'breakout/resources/sounds/Bottle.wav'
FILE_SOUND_COLLISION_BALL_BLOCK = 'breakout/resources/sounds/Tuntz.wav'
FILE_SOUND_COLLISION_BALL_PADDLE = 'breakout/resources/sounds/Ping.wav'
FILE_SOUND_BALL_DESTROYED = 'breakout/resources/sounds/Basso.wav'

COLLISION_BALL_WALL = 1
COLLISION_BALL_BALL = 2
COLLISION_BALL_BLOCK = 4
COLLISION_BALL_PADDLE = 8


class Ball(MovableGameObject):

    def __init__(self, game, position, speed, radius):
        MovableGameObject.__init__(self, game, position, speed)

        self.soundCollisionBallWall = Sound(FILE_SOUND_COLLISION_BALL_WALL)
        self.soundCollisionBallBall = Sound(FILE_SOUND_COLLISION_BALL_BALL)
        self.soundCollisionBallBlock = Sound(FILE_SOUND_COLLISION_BALL_BLOCK)
        self.soundCollisionBallPaddle = Sound(FILE_SOUND_COLLISION_BALL_PADDLE)
        self.soundBallDestroyed = Sound(FILE_SOUND_BALL_DESTROYED)

        self.radius = radius


    @property
    def rectangle(self):
        left = self.position.x - self.radius
        right = self.position.x + self.radius
        bottom = self.position.y - self.radius
        top = self.position.y + self.radius
        return Rectangle(left, bottom, right, top)


    def update(self, milliseconds, tick):
        # Move the ball. Speed is in pixels per microseconds.
        self.position.x += self.speed.x * milliseconds
        self.position.y += self.speed.y * milliseconds

        # Detect and process collisions
        collision = self._processCollisions()

        # Check if the ball crossed the bottom screen edge (in this case, the ball should be
        # destroyed, and the game status updated)
        screenRect = self.game.boundaries
        thisRect = self.rectangle
        if thisRect.bottom < (screenRect.bottom):
            self.soundBallDestroyed.play()
            self.game.destroyBall(self)


    def _processCollisions(self):
        collisionType = None
        
        # Check if the ball collides with the paddle
        collision = self._processObjectCollision(self.game.paddle)
        if collision:
            self.speed.y = abs(self.speed.y)
            collisionType = COLLISION_BALL_PADDLE
        
        # Check if the ball collides with the top, left or right screen edges, in which case
        # the ball should be repelled. If the ball cross the bottom screen edge, it
        # should be destroyed (this case will not be checked here).
        if collisionType == None:
            screenRect = self.game.boundaries
            thisRect = self.rectangle
            if thisRect.left <= screenRect.left:
                self.speed.x = abs(self.speed.x)
                collisionType = COLLISION_BALL_WALL
            elif thisRect.right >= screenRect.right:
                self.speed.x = -abs(self.speed.x)
                collisionType = COLLISION_BALL_WALL
            elif thisRect.top >= screenRect.top:
                self.speed.y = -abs(self.speed.y)
                collisionType = COLLISION_BALL_WALL
            
        # Check if the ball collides with a block
        if collisionType == None:
            for block in self.game.blocks:
                collision = self._processObjectCollision(block)
                if collision:
                    collisionType = COLLISION_BALL_BLOCK
                    self.game.destroyBlock(block)
                    break

        # Check if the ball collides with another ball
        if collisionType == None:
             for ball in self.game.balls:
                 if ball is not self:
                     collision = self._processObjectCollision(ball)
                     if collision:
                         collisionType = COLLISION_BALL_BALL
                         break
                         

        # If a collision occured, process it
        if collisionType != None:
            if collisionType == COLLISION_BALL_WALL:
                self.soundCollisionBallWall.play()
            if collisionType == COLLISION_BALL_BLOCK:
                self.soundCollisionBallBlock.play()
            if collisionType == COLLISION_BALL_PADDLE:
                self.soundCollisionBallPaddle.play()
            if collisionType == COLLISION_BALL_BALL:
                self.soundCollisionBallBall.play()
            return True
        else:
            return False

    def _processObjectCollision(self, obj):
        if obj == None:
            return False
        if obj == self:
            return False
            
        A = self.rectangle # A is this object rectangle
        B = obj.rectangle # B is target object rectangle
    
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
        tick = tick % 10

        colorTone = 0.1 * tick
        if colorTone > 1:
            colorTone = 1

        x = self.position.x
        y = self.position.y

        # outer circle
        glColor(1 - colorTone, 1 - colorTone, 1 - colorTone)
        drawCircle(x, y, self.radius)

        # inner circle
        glColor(colorTone, 0, 1 - colorTone)
        drawCircle(x, y, self.radius - 1.0)
    
    
    def __str__(self):
        return "Ball {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"
