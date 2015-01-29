# encoding: utf-8
"""
Copyright (c) 2010 Felipe Augusto Dornelas. All rights reserved.
"""

import pygame
from pygame.mixer import Sound

import random

from OpenGL.GL import *
from OpenGL.GLU import *

from Geometry import *
from Constants import *
from Drawing import *

#===================================================================================================

class GameObject:

    def __init__(self, game, position = Vector((0,0))):
        self.game = game
        self.position = position

    def __str__(self):
        return "GameObject {Position: " + str(self.position) + "}"

#===================================================================================================

class MovableGameObject(GameObject):

    def __init__(self, game, position, speed):
        GameObject.__init__(self, game, position)
        self.speed = speed
        
    def __str__(self):
        return "MovableGameObject {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"

#===================================================================================================

class Ball(MovableGameObject):

    def __init__(self, game, position, speed, radius = BALL_RADIUS):
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

        # outter circle
        glColor(1 - colorTone, 1 - colorTone, 1 - colorTone)
        drawCircle(x, y, self.radius)

        # inner circle
        glColor(colorTone, 0, 1 - colorTone)
        drawCircle(x, y, self.radius - 1.0)
    
    
    def __str__(self):
        return "Ball {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"

#===================================================================================================

class Paddle(MovableGameObject):

    def __init__(self, game, position, speed = Vector((0,0)), width = 40):
        MovableGameObject.__init__(self, game, position, speed)
        self.width = width
        self.height = PADDLE_HEIGHT


    @property
    def rectangle(self):
        left = self.position.x - self.width/2.0
        right = self.position.x + self.width/2.0
        bottom = self.position.y - self.height/2.0
        top = self.position.y + self.height/2.0
        return Rectangle(left, bottom, right, top)


    def update(self, milliseconds, tick):
        # Moves the paddle (horizontally only). Speed is in pixels per second.
        self.position.x += self.speed.x * milliseconds

        # Don't let the paddle cross the screen boundaries
        screenRect = self.game.boundaries
        thisRect = self.rectangle
        if thisRect.left <= screenRect.left:
            self.position.x = screenRect.left + self.width/2.0
            self.speed.x = 0
        elif thisRect.right >= screenRect.right:
            self.position.x = screenRect.right - self.width/2.0
            self.speed.x = 0


    def display(self, milliseconds, tick):
        tick = tick % 10

        colorTone = 0.1 * tick
        if colorTone > 1:
            colorTone = 1

        bv = 1
        bh = 2

        x = self.position.x
        y = self.position.y
        h = self.height/2 - bv
        w = self.width/2 - bh

        # outter rectangle
        glBegin(GL_POLYGON)
        glColor(1 - colorTone, 1 - colorTone, 1 - colorTone)
        glVertex(x - (w + bh), y + (h + bv))
        glVertex(x + (w + bh), y + (h + bv))
        glVertex(x + (w + bh), y - (h + bv))
        glVertex(x - (w + bh), y - (h + bv))
        glEnd()

        # inner rectangle
        glBegin(GL_POLYGON)
        glColor(colorTone, 0.0, 0.0)
        glVertex(x - w, y + h)
        glVertex(x + w, y + h)
        glVertex(x + w, y - h)
        glVertex(x - w, y - h)
        glEnd()

    def __str__(self):
        return "Paddle {Position: " + str(self.position) + ", Speed: " + str(self.speed) + "}"

#===================================================================================================

class Block(GameObject):

    @property
    def points(self):
        if self.color == BLOCK_COLOR_BLUE:
            return BLOCK_POINTS_BLUE
        elif self.color == BLOCK_COLOR_GREEN:
            return BLOCK_POINTS_GREEN
        elif self.color == BLOCK_COLOR_RED:
            return BLOCK_POINTS_RED
        else:
            raise Exception


    def __init__(self, game, position, color = BLOCK_COLOR_GREEN, width = 20, height = 10):
        GameObject.__init__(self, game, position)
        self.width = width
        self.height = height
        self.color = color


    @property
    def rectangle(self):
        left = self.position.x - self.width/2.0
        right = self.position.x + self.width/2.0
        top = self.position.y + self.height/2.0
        bottom = self.position.y - self.height/2.0
        return Rectangle(left, bottom, right, top)


    def update(self, milliseconds, tick):
        pass


    def display(self, milliseconds, tick):
        tick = tick % 10

        colorTone = 0.1 * tick
        if colorTone > 1:
            colorTone = 1

        bv = 1
        bh = 2

        x = self.position.x
        y = self.position.y
        h = self.height/2.0 - bv
        w = self.width/2.0 - bh

        # outter rectangle
        glBegin(GL_POLYGON)
        glColor(1 - colorTone, 1 - colorTone, 1 - colorTone)
        glVertex(x - (w + bh), y + (h + bv))
        glVertex(x + (w + bh), y + (h + bv))
        glVertex(x + (w + bh), y - (h + bv))
        glVertex(x - (w + bh), y - (h + bv))
        glEnd()

        # inner rectangle
        glBegin(GL_POLYGON)

        if self.color == BLOCK_COLOR_RED:
            glColor(colorTone, 0, 0)
        elif self.color == BLOCK_COLOR_GREEN:
            glColor(0, colorTone, 0)
        elif self.color == BLOCK_COLOR_BLUE:
            glColor(0, 0, colorTone)
        else:
            raise Exception("Color not supported.")

        glVertex(x - w, y + h)
        glVertex(x + w, y + h)
        glVertex(x + w, y - h)
        glVertex(x - w, y - h)
        glEnd()
    

    def __str__(self):
        return "Block {Position: " + str(self.position) + ", Points: " + str(self.points) + "}"

#===================================================================================================
