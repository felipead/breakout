from datetime import datetime

from OpenGL.GL import *
from OpenGL.GLUT import *

import pygame
from pygame.mixer import Sound
from pygame.font import Font
from pygame.constants import K_q
from pygame.constants import K_r

from breakout.domain.Ball import Ball
from breakout.domain.Block import Block
from breakout.domain.Paddle import Paddle
from breakout.geometry.Vector import Vector
from breakout.geometry.Rectangle import Rectangle
from breakout.util.DrawingUtil import DrawingUtil


# FIXME
_DEFAULT_SCREEN_WIDTH = 500
_DEFAULT_SCREEN_HEIGHT = 600
CANVAS_SCREEN_RATIO = 0.5
CANVAS_LEFT = 0
CANVAS_BOTTOM = 0
CANVAS_RIGHT = _DEFAULT_SCREEN_WIDTH * CANVAS_SCREEN_RATIO
CANVAS_TOP = _DEFAULT_SCREEN_HEIGHT * CANVAS_SCREEN_RATIO

GAME_STATE_PLAY = 1
GAME_STATE_PAUSE = 2
GAME_STATE_HALT = 3
GAME_STATE_HALT_RUN_CYCLE = 4
GAME_STATE_LOST = 5
GAME_STATE_WON = 6

_FILE_BACKGROUND_LEVEL1 = 'breakout/resources/graphics/Level1.png'
_FILE_MUSIC_LEVEL1 = 'breakout/resources/sounds/ChemicalBurn.wav'
_FILE_FONT_INFORMATION_BAR = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'
_FILE_FONT_MESSAGE = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'

_INFORMATION_BAR_FONT_SIZE = 14
_INFORMATION_BAR_FOREGROUND_COLOR = (255, 255, 255)
_INFORMATION_BAR_BACKGROUND_COLOR = (0, 0, 0)

_MESSAGE_FONT_SIZE = 28
_MESSAGE_FOREGROUND_COLOR = (255, 0, 0)
_MESSAGE_BACKGROUND_COLOR = (0, 0, 0)

_BALL_DEFAULT_SPEED = 0.05
_BALL_RADIUS = 3.0

_VELOCITY_BAR_HEIGHT = 3.0
_INFORMATION_BAR_HEIGHT = 12.0

_PADDLE_MAX_SPEED = 0.75

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 3
MOUSE_BUTTON_SCROLL_UP = 4
MOUSE_BUTTON_SCROLL_DOWN = 5

class BreakoutEngine:

    def __init__(self, canvas):
        """
        :param canvas: the rectangle of the screen where the game will display itself. The canvas uses internal game coordinates, not screen coordinates.
        """
        self._canvas = canvas

        # The boundaries rectangle is the canvas excluding the information and velocity bars.
        self._boundaries = Rectangle(canvas.left, canvas.bottom + _VELOCITY_BAR_HEIGHT, \
            canvas.right, canvas.top - _INFORMATION_BAR_HEIGHT)

        self._backgroundTexture = None
        self._backgroundMusic = None
        self._informationBarFont = None
        self._messageFont = None

        self._gameState = None
        self._gamePoints = 0

        # Game objects
        self.blocks = list()
        self.balls = list()
        self.paddle = Paddle(self)
        self.paddle.position = Vector((self._boundaries.right/2.0, self._boundaries.bottom + self.paddle.height))

    @property
    def boundaries(self):
        return self._boundaries

    @property
    def gameState(self):
        return self._gameState

    @property
    def gamePoints(self):
        return self._gamePoints

    def initialize(self):
        # Draws the level objects. Currently, there's only one level (Level 1),
        # and its definition is "hard coded".
        # TODO: add support for more levels.
        # TODO: store the level definition in an external text file
        self.__buildLevel1()

        self._informationBarFont = Font(_FILE_FONT_INFORMATION_BAR, _INFORMATION_BAR_FONT_SIZE)
        self._messageFont = Font(_FILE_FONT_MESSAGE, _MESSAGE_FONT_SIZE)

        if self._backgroundMusic != None:
            self._backgroundMusic.play(-1) # plays the background music in infinite loop

        self._gameState = GAME_STATE_PAUSE # the game starts paused


    def reset(self):
        if self._backgroundMusic != None:
            self._backgroundMusic.stop()

        del self.balls[0:len(self.balls)]
        del self.blocks[0:len(self.blocks)]
        self._gamePoints = 0
        self.paddle.position.x = self.boundaries.right/2.0

        self.initialize()


    def update(self, milliseconds, tick):
        """
        Updates the logic of one game cycle
        :param milliseconds: elapsed milliseconds since last cycle
        :param tick: number of ticks (cycles) elapsed so far
        """
        if (self._gameState == None):
            raise Exception("Invalid operation. Did you forget to call initialize() first?")

        # The player looses the game when all balls are gone.
        # The player wins the game when all blocks are destroyed.
        if len(self.balls) == 0:
            self._gameState = GAME_STATE_LOST
        elif len(self.blocks) == 0:
            self._gameState = GAME_STATE_WON

        if (self._gameState == GAME_STATE_PLAY) or (self._gameState == GAME_STATE_HALT_RUN_CYCLE):
            self.paddle.update(milliseconds, tick)
            for ball in self.balls:
                ball.update(milliseconds, tick)
            for block in self.blocks:
                block.update(milliseconds, tick)

        if self._gameState == GAME_STATE_HALT_RUN_CYCLE:
            self._gameState = GAME_STATE_HALT

    def destroyBlock(self, block):
        if block in self.blocks:
            self._gamePoints += block.points
            self.blocks.remove(block)
            del block

    def destroyBall(self, ball):
        if ball in self.balls:
            self.balls.remove(ball)
            del ball

    def display(self, milliseconds, tick, screen_width, screen_height):
        """
        Draws the graphics of one game cycle
        :param milliseconds: elapsed milliseconds since last cycle
        :param tick: number of ticks (cycles) elapsed so far
        :param screen_width: width of the screen
        :param screen_height: height of the screen
        """

        if self._gameState == None:
            raise Exception("Invalid operation. Did you forget to call initialize() first?")

        # clear the screen
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)

        self.__drawBackground(screen_height, screen_width)
        self.__drawVelocityBar()
        self.__drawInformationBar()
        self.__drawGameObjects(milliseconds, tick)
        self.__drawMessage()


    def __drawBackground(self, screen_height, screen_width):
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, self._backgroundTexture)
        glColor(1, 1, 1, 1)
        h = screen_height
        w = screen_width
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

    def __drawGameObjects(self, milliseconds, tick):
        self.paddle.display(milliseconds, tick)
        for ball in self.balls:
            ball.display(milliseconds, tick)
        for block in self.blocks:
            block.display(milliseconds, tick)

    def __drawInformationBar(self):
        # Draw the information bar, on the screen top edge
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(CANVAS_LEFT, CANVAS_TOP)
        glVertex(CANVAS_RIGHT, CANVAS_TOP)
        glVertex(CANVAS_RIGHT, CANVAS_TOP - _INFORMATION_BAR_HEIGHT)
        glVertex(CANVAS_LEFT, CANVAS_TOP - _INFORMATION_BAR_HEIGHT)
        glEnd()
        # Fills the information bar with the game status
        text = (" Level 1  |  Balls %d  |  Points %d " % (len(self.balls), self._gamePoints))
        x = CANVAS_LEFT
        y = CANVAS_TOP - _INFORMATION_BAR_HEIGHT
        rendered = self._informationBarFont.render(text, True, \
                                            _INFORMATION_BAR_FOREGROUND_COLOR, _INFORMATION_BAR_BACKGROUND_COLOR)
        bytes = pygame.image.tostring(rendered, "RGBA", 1)
        size = rendered.get_size()
        glRasterPos2d(x, y)
        glPixelZoom(1, 1)
        glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, bytes)

    def __drawVelocityBar(self):
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(CANVAS_LEFT, CANVAS_BOTTOM)
        glVertex(CANVAS_RIGHT, CANVAS_BOTTOM)
        glVertex(CANVAS_RIGHT, CANVAS_BOTTOM + _VELOCITY_BAR_HEIGHT)
        glVertex(CANVAS_LEFT, CANVAS_BOTTOM + _VELOCITY_BAR_HEIGHT)
        glEnd()
        half = (CANVAS_RIGHT - CANVAS_LEFT) / 2
        paddleSpeed = self.paddle.speed.x
        glBegin(GL_POLYGON)
        glColor(0.8, 0.8, 0)
        glVertex(half, CANVAS_BOTTOM)
        glVertex(half, CANVAS_BOTTOM + _VELOCITY_BAR_HEIGHT)
        glVertex(paddleSpeed * half / _PADDLE_MAX_SPEED + half, CANVAS_BOTTOM + _VELOCITY_BAR_HEIGHT)
        glVertex(paddleSpeed * half / _PADDLE_MAX_SPEED + half, CANVAS_BOTTOM)
        glEnd()
        glBegin(GL_LINES)
        glVertex(CANVAS_LEFT, CANVAS_BOTTOM)
        glVertex(CANVAS_RIGHT, CANVAS_BOTTOM)
        glEnd()

    def __drawMessage(self):
        if self._gameState == GAME_STATE_PAUSE:
            text = "Pause"
        elif self._gameState == GAME_STATE_LOST:
            text = "Game Over"
        elif self._gameState == GAME_STATE_WON:
            text = "Congratulations"
        else:
            text = None
        if text != None:
            rendered = self._messageFont.render(text, True, \
                                                _MESSAGE_FOREGROUND_COLOR, _MESSAGE_BACKGROUND_COLOR)
            bytes = pygame.image.tostring(rendered, "RGBA", 1)
            size = rendered.get_size()
            x = (CANVAS_RIGHT - CANVAS_LEFT) / 2 - size[0] / 4
            y = (CANVAS_TOP - CANVAS_BOTTOM) / 2 - size[1] / 4
            glRasterPos2d(x, y)
            glPixelZoom(1, 1)
            glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, bytes)

    def __printDebugInfo(self):
        now = datetime.now()
        print "[" + now.strftime("%H:%M:%S") + "." + str(now.microsecond) + "]"

        print self.paddle
        for ball in self.balls:
            print ball
        for block in self.blocks:
            print block
        print

    def handleMouseButtonDownEvent(self, button, coordinates):
        if button == MOUSE_BUTTON_RIGHT:
            self.__printDebugInfo()
            if self._gameState == GAME_STATE_HALT:
                self._gameState = GAME_STATE_HALT_RUN_CYCLE
            else:
                self._gameState = GAME_STATE_HALT
        if button == MOUSE_BUTTON_LEFT:
            if self._gameState == GAME_STATE_HALT or self._gameState == GAME_STATE_PAUSE:
                self._gameState = GAME_STATE_PLAY
            elif self._gameState == GAME_STATE_PLAY:
                self._gameState = GAME_STATE_PAUSE

    def handleMouseButtonUpEvent(self, button, coordinates):
        pass

    def handleKeyDownEvent(self, key, modifiers, char):
        if key == K_q:
            print "Game aborted."
            sys.exit()
        if key == K_r:
            print "Game reset."
            self.reset()

    def handleKeyUpEvent(self, key, modifiers):
        pass

    def handleMouseMoveEvent(self, absoluteCoordinates, relativeCoordinates, buttons):
        if self._gameState == GAME_STATE_PLAY or self._gameState == GAME_STATE_HALT or self._gameState == GAME_STATE_HALT_RUN_CYCLE:
            (x, y) = absoluteCoordinates
            median = (self._canvas.right - self._canvas.left) / 2
            paddleSpeed = (x - median) / median
            paddleSpeed *= _PADDLE_MAX_SPEED
            self.paddle.speed.x = paddleSpeed

    def __buildLevel1(self):
        self._backgroundTexture = DrawingUtil.loadTexture(_FILE_BACKGROUND_LEVEL1, False)
        self._backgroundMusic = Sound(_FILE_MUSIC_LEVEL1)

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

        s = _BALL_DEFAULT_SPEED

        self.balls.append(Ball(self, position=Vector((self._boundaries.width/2, self._boundaries.top - _BALL_RADIUS)), speed=Vector((-s, s)), radius=_BALL_RADIUS))
        self.balls.append(Ball(self, position=Vector((self._boundaries.right - _BALL_RADIUS, self._boundaries.top - _BALL_RADIUS)), speed=Vector((-s, -s)), radius=_BALL_RADIUS))
        self.balls.append(Ball(self, position=Vector((self._boundaries.left + _BALL_RADIUS, self._boundaries.top - _BALL_RADIUS)), speed=Vector((s, -s)), radius=_BALL_RADIUS))