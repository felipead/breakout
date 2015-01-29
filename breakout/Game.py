# encoding: utf-8
"""
Copyright (c) 2010 Felipe Augusto Dornelas. All rights reserved.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import pygame
from pygame.mixer import Sound
from pygame.font import Font
from pygame.locals import *

from datetime import datetime

from Geometry import Vector, Rectangle
from GameObjects import *
from DrawingUtil import *
from Constants import *

#===================================================================================================

# Game State Constants
GAME_STATE_PLAY = 1
GAME_STATE_PAUSE = 2
GAME_STATE_HALT = 3
GAME_STATE_HALT_RUNCYCLE = 4
GAME_STATE_LOST = 5
GAME_STATE_WON = 6

class Game:

    # Create a new game instance. The canvas argument is the rectangle of the screen where the game
    # will display itself. The canvas uses internal game coordinates, not screen coordinates.
    def __init__(self, canvas):
        self._canvas = canvas
        
        # The boundaries rectangle is the canvas excluding the information and velocity bars.
        self._boundaries = Rectangle(canvas.left, canvas.bottom + VELOCITYBAR_HEIGHT, \
            canvas.right, canvas.top - INFOBAR_HEIGHT)
        
        self._backgroundTexture = None
        self._backgroundMusic = None
        self._infobarFont = None
        self._messageFont = None
        
        # Game state variables
        self._state = None
        self.points = 0

        # Game objects
        self.blocks = list()
        self.balls = list()
        self.paddle = Paddle(self, position=Vector(\
            (self.boundaries.right/2.0, self.boundaries.bottom + PADDLE_HEIGHT)))


    def init(self):
        # Draws the level objects. Currently, there's only one level (Level 1),
        # and its definition is "hard coded".
        # TODO: add support for more levels.
        # TODO: store the level definition in an external text file
        self.buildLevel1()
        
        self._infobarFont = Font(FILE_FONT_INFOBAR, FONT_INFOBAR_SIZE)
        self._messageFont = Font(FILE_FONT_MESSAGE, FONT_MESSAGE_SIZE)
        
        if self._backgroundMusic != None:
            self._backgroundMusic.play(-1) # plays the background music in infinite loop
        
        self._state = GAME_STATE_PAUSE # the game starts paused


    def reset(self):
        if self._backgroundMusic != None:
            self._backgroundMusic.stop()
        
        del self.balls[0:len(self.balls)]
        del self.blocks[0:len(self.blocks)]
        self.points = 0
        self.paddle.position.x = self.boundaries.right/2.0
        
        self.init()


    @property
    def boundaries(self):
        return self._boundaries

    # Destroys a block that was hit by a ball. The game score
    # is updated with the block points.
    def destroyBlock(self, block):
        if block in self.blocks:
            self.points += block.points
            self.blocks.remove(block)
            del block


    # Destroys a ball that hit the floor.
    def destroyBall(self, ball):
        if ball in self.balls:
            self.balls.remove(ball)
            del ball


    # Updates the logic of one game cycle
    def update(self, milliseconds, tick):        
        if (self._state == None):
            raise Exception("Invalid operation. Did you forget to call init() first?")
        
        # The player looses the game when all balls are gone.
        # The player wins the game when all blocks are destroyed.
        if len(self.balls) == 0:
            self._state = GAME_STATE_LOST
        elif len(self.blocks) == 0:
            self._state = GAME_STATE_WON
        
        if (self._state == GAME_STATE_PLAY) or (self._state == GAME_STATE_HALT_RUNCYCLE):
            self.paddle.update(milliseconds, tick)
            for ball in self.balls:
                ball.update(milliseconds, tick)
            for block in self.blocks:
                block.update(milliseconds, tick)
                
        if self._state == GAME_STATE_HALT_RUNCYCLE:
            self._state = GAME_STATE_HALT


    # Draws the graphics of one game cycle
    def display(self, milliseconds, tick):
        if self._state == None:
            raise Exception("Invalid operation. Did you forget to call init() first?")
            
        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)

        # draw the background texture
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, self._backgroundTexture)
        glColor(1, 1, 1, 1)
        h = SCREEN_HEIGHT
        w = SCREEN_WIDTH
        glBegin(GL_POLYGON)
        glTexCoord(-1, -1)
        glVertex(0, 0)
        glTexCoord(1, -1)
        glVertex(w, 0)
        glTexCoord(1, 1)
        glVertex(w, h)
        glTexCoord(-1, 1)
        glVertex(0, h)
        glEnd()
        glEnable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
        
        # Draw the velocity bar, on the screen bottom
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(CANVAS_LEFT, CANVAS_BOTTOM)
        glVertex(CANVAS_RIGHT, CANVAS_BOTTOM)
        glVertex(CANVAS_RIGHT, CANVAS_BOTTOM + VELOCITYBAR_HEIGHT)
        glVertex(CANVAS_LEFT, CANVAS_BOTTOM + VELOCITYBAR_HEIGHT)
        glEnd()
        
        half = (CANVAS_RIGHT - CANVAS_LEFT) / 2;
        paddleSpeed = self.paddle.speed.x
        glBegin(GL_POLYGON)
        glColor(0.8, 0.8, 0)
        glVertex(half, CANVAS_BOTTOM)
        glVertex(half, CANVAS_BOTTOM + VELOCITYBAR_HEIGHT)
        glVertex(paddleSpeed * half / PADDLE_SPEED_MAX + half,
            CANVAS_BOTTOM + VELOCITYBAR_HEIGHT)
        glVertex(paddleSpeed * half / PADDLE_SPEED_MAX + half, CANVAS_BOTTOM)
        glEnd()
        glBegin(GL_LINES)
        glVertex(CANVAS_LEFT, CANVAS_BOTTOM)
        glVertex(CANVAS_RIGHT, CANVAS_BOTTOM)
        glEnd()

        # Draw the information bar, on the screen top edge
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(CANVAS_LEFT, CANVAS_TOP)
        glVertex(CANVAS_RIGHT, CANVAS_TOP)
        glVertex(CANVAS_RIGHT, CANVAS_TOP - INFOBAR_HEIGHT)
        glVertex(CANVAS_LEFT, CANVAS_TOP - INFOBAR_HEIGHT)
        glEnd()
        
        # Fills the information bar with the game status
        text = (" Level 1  |  Balls %d  |  Points %d " % (len(self.balls), self.points))
        x = CANVAS_LEFT
        y = CANVAS_TOP - INFOBAR_HEIGHT
        rendered = self._infobarFont.render(text, True,\
            FONT_INFOBAR_COLOR_FOREGROUND, FONT_INFOBAR_COLOR_BACKGROUND)
        bytes = pygame.image.tostring(rendered, "RGBA", 1)
        size = rendered.get_size()
        glRasterPos2d(x, y)
        glPixelZoom(1, 1)
        glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, bytes)
        
        # Draw the game objects (each game object implements its own drawing method).
        self.paddle.display(milliseconds, tick)
        for ball in self.balls:
            ball.display(milliseconds, tick)
        for block in self.blocks:
            block.display(milliseconds, tick)
        
        # Shows a message in the screen describing the state of the game, if necessary.
        if self._state == GAME_STATE_PAUSE:        
            text = "Pause"
        elif self._state == GAME_STATE_LOST:
            text = "Game Over"
        elif self._state == GAME_STATE_WON:
            text = "Congratulations"
        else:
            text = None        
        if text != None:
            rendered = self._messageFont.render(text, True,\
                FONT_MESSAGE_COLOR_FOREGROUND, FONT_MESSAGE_COLOR_BACKGROUND)
            bytes = pygame.image.tostring(rendered, "RGBA", 1)
            size = rendered.get_size()
            x = (CANVAS_RIGHT - CANVAS_LEFT)/2 - size[0]/4
            y = (CANVAS_TOP - CANVAS_BOTTOM)/2 - size[1]/4
            glRasterPos2d(x, y)
            glPixelZoom(1, 1)
            glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, bytes)

    # Prints a textual information in the command line, describing the state
    # of each game object for debugging purposes
    def printDebugInfo(self):
        # Prints time stamp first
        now = datetime.now()
        print "[" + now.strftime("%H:%M:%S") + "." + str(now.microsecond) + "]"
        
        print self.paddle
        for ball in self.balls:
            print ball
        for block in self.blocks:
            print block
        
        print


    def mouseButtonDownEvent(self, button, coordinates):
        if button == MOUSE_BUTTON_RIGHT:
            self.printDebugInfo()
            if self._state == GAME_STATE_HALT:
                self._state = GAME_STATE_HALT_RUNCYCLE
            else:
                self._state = GAME_STATE_HALT
        if button == MOUSE_BUTTON_LEFT:
            if self._state == GAME_STATE_HALT or self._state == GAME_STATE_PAUSE:
                self._state = GAME_STATE_PLAY
            elif self._state == GAME_STATE_PLAY:
                self._state = GAME_STATE_PAUSE


    def mouseButtonUpEvent(self, button, coordinates):
        pass


    def keyDownEvent(self, key, modifiers, char):
        if key == K_q:
            print "Game aborted."
            sys.exit()
        if key == K_r:
            print "Game reset."
            self.reset()


    def keyUpEvent(self, key, modifiers):
        pass


    def mouseMoveEvent(self, absoluteCoordinates, relativeCoordinates, buttons):
        if self._state == GAME_STATE_PLAY or self._state == GAME_STATE_HALT or self._state == GAME_STATE_HALT_RUNCYCLE:
            (x, y) = absoluteCoordinates
            median = (self._canvas.right - self._canvas.left) / 2
            paddleSpeed = (x - median) / median
            paddleSpeed *= PADDLE_SPEED_MAX            
            self.paddle.speed.x = paddleSpeed


    def buildLevel1(self):
        self._backgroundTexture = loadTexture(FILE_BACKGROUND_LEVEL1, False)
        self._backgroundMusic = pygame.mixer.Sound(FILE_MUSIC_LEVEL1)
        
        blockWidth = 20
        blockHeight = 10
        
        columns = (int) (self._boundaries.width // (blockWidth))
        rows = (int) (self._boundaries.height // (blockHeight))
        
        for i in xrange(3, columns-1):
            for j in xrange(15, rows-3):
                color = j % 3 + 1
                position = Vector((self._boundaries.left + i * blockWidth, self._boundaries.bottom + j * blockHeight))
                block = Block(self, position, color = color, width = blockWidth, height = blockHeight)
                self.blocks.append(block)
        
        for i in xrange(3, columns - 1):
            color = i % 3 + 1
            j = 10
            position = Vector((self._boundaries.left + i * blockWidth, self._boundaries.bottom + j * blockHeight))
            block = Block(self, position, color = color, width = blockWidth, height = blockHeight)
            self.blocks.append(block)
            
        s = BALL_SPEED_DEFAULT
        
        self.balls.append(Ball(self, position=Vector((self._boundaries.width/2, self._boundaries.top - BALL_RADIUS)), speed=Vector((-s, s))))
        self.balls.append(Ball(self, position=Vector((self._boundaries.right - BALL_RADIUS, self._boundaries.top - BALL_RADIUS)), speed=Vector((-s, -s))))
        self.balls.append(Ball(self, position=Vector((self._boundaries.left + BALL_RADIUS, self._boundaries.top - BALL_RADIUS)), speed=Vector((s, -s))))