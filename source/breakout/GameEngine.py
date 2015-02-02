from datetime import datetime

from OpenGL.GL import *
from OpenGL.GLUT import *

import pygame
from pygame.font import Font
from pygame.constants import K_q, K_r
from breakout.LevelFactory import LevelFactory

from breakout.domain.Paddle import Paddle
from breakout.geometry.Vector import Vector
from breakout.geometry.Rectangle import Rectangle

GAME_STATE_PLAY = 1
GAME_STATE_PAUSE = 2
GAME_STATE_HALT = 3
GAME_STATE_HALT_RUN_CYCLE = 4
GAME_STATE_LOST = 5
GAME_STATE_WON = 6

_FILE_FONT_INFORMATION_BAR = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'
_FILE_FONT_MESSAGE = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'

_INFORMATION_BAR_FONT_SIZE = 14
_INFORMATION_BAR_FOREGROUND_COLOR = (255, 255, 255)
_INFORMATION_BAR_BACKGROUND_COLOR = (0, 0, 0)

_MESSAGE_FONT_SIZE = 28
_MESSAGE_FOREGROUND_COLOR = (255, 0, 0)
_MESSAGE_BACKGROUND_COLOR = (0, 0, 0)

_VELOCITY_BAR_HEIGHT = 3.0
_INFORMATION_BAR_HEIGHT = 12.0

_PADDLE_MAX_SPEED = 0.75

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 3
MOUSE_BUTTON_SCROLL_UP = 4
MOUSE_BUTTON_SCROLL_DOWN = 5


class GameEngine:

    def __init__(self, canvasWidth, canvasHeight):
        self.__canvas = Rectangle(0, 0, canvasWidth, canvasHeight)
        self.__boundaries = Rectangle(self.__canvas.left, self.__canvas.bottom + _VELOCITY_BAR_HEIGHT,
            self.__canvas.right, self.__canvas.top - _INFORMATION_BAR_HEIGHT)

        self.__informationBarFont = None
        self.__messageFont = None

        self.__levelFactory = LevelFactory(self)
        self.__currentLevel = None

        self.__gameState = None
        self.__gamePoints = 0

        self.__blocks = list()
        self.__balls = list()
        self.__paddle = Paddle(self)
        self.__paddle.position = Vector((self.__boundaries.right/2.0, self.__boundaries.bottom + self.__paddle.height))

    @property
    def balls(self):
        return self.__balls

    @property
    def blocks(self):
        return self.__blocks

    @property
    def paddle(self):
        return self.__paddle

    @property
    def canvas(self):
        return self.__canvas

    @property
    def gameObjects(self):
        gameObjects = [self.__paddle]
        gameObjects.extend(self.__balls)
        gameObjects.extend(self.__blocks)
        return gameObjects

    @property
    def boundaries(self):
        return self.__boundaries

    @property
    def gameState(self):
        return self.__gameState

    @property
    def gamePoints(self):
        return self.__gamePoints


    def initialize(self):
        self.__informationBarFont = Font(_FILE_FONT_INFORMATION_BAR, _INFORMATION_BAR_FONT_SIZE)
        self.__messageFont = Font(_FILE_FONT_MESSAGE, _MESSAGE_FONT_SIZE)

        self._loadLevel(self.__levelFactory.getLevel(1))
        if self.__currentLevel.backgroundMusic is not None:
            self.__currentLevel.backgroundMusic.play(-1)

        self.__gameState = GAME_STATE_PAUSE

    def _loadLevel(self, level):
        self.__balls = list(level.balls)
        self.__blocks = list(level.blocks)
        self.__currentLevel = level

    def reset(self):
        if self.__currentLevel.backgroundMusic is not None:
            self.__currentLevel.backgroundMusic.stop()

        del self.__balls[0:len(self.__balls)]
        del self.__blocks[0:len(self.__blocks)]
        self.__gamePoints = 0
        self.__paddle.position.x = self.boundaries.right/2.0

        self.initialize()

    def update(self, milliseconds, tick):
        if self.__gameState is None:
            raise Exception("Invalid operation. Did you forget to call initialize() first?")

        # The player looses the game when all balls are gone.
        # The player wins the game when all blocks are destroyed.
        if len(self.__balls) == 0:
            self.__gameState = GAME_STATE_LOST
        elif len(self.__blocks) == 0:
            self.__gameState = GAME_STATE_WON

        if (self.__gameState == GAME_STATE_PLAY) or (self.__gameState == GAME_STATE_HALT_RUN_CYCLE):
            for gameObject in self.gameObjects:
                gameObject.update(milliseconds, tick)

        if self.__gameState == GAME_STATE_HALT_RUN_CYCLE:
            self.__gameState = GAME_STATE_HALT

    def destroyBlock(self, block):
        if block in self.__blocks:
            self.__gamePoints += block.points
            self.__blocks.remove(block)
            del block

    def destroyBall(self, ball):
        if ball in self.__balls:
            self.__balls.remove(ball)
            del ball

    def display(self, milliseconds, tick, screen_width, screen_height):

        if self.__gameState is None:
            raise Exception("Invalid operation. Did you forget to call initialize() first?")
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)   # clear the screen
        self.__drawBackground(screen_height, screen_width)
        self.__drawVelocityBar()
        self.__drawInformationBar()
        self.__drawGameObjects(milliseconds, tick)
        self.__drawMessage()


    def __drawBackground(self, screen_height, screen_width):
        glEnable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)
        glBindTexture(GL_TEXTURE_2D, self.__currentLevel.backgroundTexture)
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
        for gameObject in self.gameObjects:
                gameObject.display(milliseconds, tick)

    def __drawInformationBar(self):
        # Draw the information bar, on the screen top edge
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(self.__canvas.left, self.__canvas.top)
        glVertex(self.__canvas.right, self.__canvas.top)
        glVertex(self.__canvas.right, self.__canvas.top - _INFORMATION_BAR_HEIGHT)
        glVertex(self.__canvas.left, self.__canvas.top - _INFORMATION_BAR_HEIGHT)
        glEnd()
        # Fills the information bar with the game status
        text = (" Level 1  |  Balls %d  |  Points %d " % (len(self.__balls), self.__gamePoints))
        x = self.__canvas.left
        y = self.__canvas.top - _INFORMATION_BAR_HEIGHT
        rendered = self.__informationBarFont.render(text, True,
                                            _INFORMATION_BAR_FOREGROUND_COLOR, _INFORMATION_BAR_BACKGROUND_COLOR)
        renderedTextBytes = pygame.image.tostring(rendered, "RGBA", 1)
        size = rendered.get_size()
        glRasterPos2d(x, y)
        glPixelZoom(1, 1)
        glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, renderedTextBytes)

    def __drawVelocityBar(self):
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(self.__canvas.left, self.__canvas.bottom)
        glVertex(self.__canvas.right, self.__canvas.bottom)
        glVertex(self.__canvas.right, self.__canvas.bottom + _VELOCITY_BAR_HEIGHT)
        glVertex(self.__canvas.left, self.__canvas.bottom + _VELOCITY_BAR_HEIGHT)
        glEnd()
        half = (self.__canvas.right - self.__canvas.left) / 2
        paddleSpeed = self.__paddle.speed.x
        glBegin(GL_POLYGON)
        glColor(0.8, 0.8, 0)
        glVertex(half, self.__canvas.bottom)
        glVertex(half, self.__canvas.bottom + _VELOCITY_BAR_HEIGHT)
        glVertex(paddleSpeed * half / _PADDLE_MAX_SPEED + half, self.__canvas.bottom + _VELOCITY_BAR_HEIGHT)
        glVertex(paddleSpeed * half / _PADDLE_MAX_SPEED + half, self.__canvas.bottom)
        glEnd()
        glBegin(GL_LINES)
        glVertex(self.__canvas.left, self.__canvas.bottom)
        glVertex(self.__canvas.right, self.__canvas.bottom)
        glEnd()

    def __drawMessage(self):
        if self.__gameState == GAME_STATE_PAUSE:
            text = "Pause"
        elif self.__gameState == GAME_STATE_LOST:
            text = "Game Over"
        elif self.__gameState == GAME_STATE_WON:
            text = "Congratulations"
        else:
            text = None

        if text is not None:
            renderedText = self.__messageFont.render(text, True,
                                                _MESSAGE_FOREGROUND_COLOR, _MESSAGE_BACKGROUND_COLOR)
            renderedTextBytes = pygame.image.tostring(renderedText, "RGBA", 1)
            size = renderedText.get_size()
            x = (self.__canvas.right - self.__canvas.left) / 2 - size[0] / 4
            y = (self.__canvas.top - self.__canvas.bottom) / 2 - size[1] / 4
            glRasterPos2d(x, y)
            glPixelZoom(1, 1)
            glDrawPixels(size[0], size[1], GL_RGBA, GL_UNSIGNED_BYTE, renderedTextBytes)

    def __printDebugInfo(self):
        now = datetime.now()
        print "[" + now.strftime("%H:%M:%S") + "." + str(now.microsecond) + "]"

        print self.__paddle
        for ball in self.__balls:
            print ball
        for block in self.__blocks:
            print block
        print

    def handleMouseButtonDownEvent(self, button, coordinates):
        if button == MOUSE_BUTTON_RIGHT:
            self.__printDebugInfo()
            if self.__gameState == GAME_STATE_HALT:
                self.__gameState = GAME_STATE_HALT_RUN_CYCLE
            else:
                self.__gameState = GAME_STATE_HALT
        if button == MOUSE_BUTTON_LEFT:
            if self.__gameState == GAME_STATE_HALT or self.__gameState == GAME_STATE_PAUSE:
                self.__gameState = GAME_STATE_PLAY
            elif self.__gameState == GAME_STATE_PLAY:
                self.__gameState = GAME_STATE_PAUSE

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
        if self.__gameState == GAME_STATE_PLAY or self.__gameState == GAME_STATE_HALT or self.__gameState == GAME_STATE_HALT_RUN_CYCLE:
            (x, y) = absoluteCoordinates
            median = (self.__canvas.right - self.__canvas.left) / 2
            paddleSpeed = (x - median) / median
            paddleSpeed *= _PADDLE_MAX_SPEED
            self.__paddle.speed.x = paddleSpeed
