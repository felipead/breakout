from datetime import datetime
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
from pygame.font import Font
from pygame.constants import K_q, K_r, K_SPACE, K_p

from breakout.util.MouseButton import MouseButton
from breakout.game.GameState import GameState
from breakout.game.LevelFactory import LevelFactory
from breakout.model.Paddle import Paddle
from breakout.geometry.Vector import Vector
from breakout.geometry.Rectangle import Rectangle


_INFORMATION_BAR_HEIGHT = 12.0
_INFORMATION_BAR_FONT_FILE = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'
_INFORMATION_BAR_FONT_SIZE = 14
_INFORMATION_BAR_FOREGROUND_COLOR = (255, 255, 255)
_INFORMATION_BAR_BACKGROUND_COLOR = (0, 0, 0)

_PADDLE_SPEED_BAR_HEIGHT = 3.0
_PADDLE_MAX_SPEED = 0.75

_MESSAGE_BOX_FONT_FILE = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'
_MESSAGE_BOX_FONT_SIZE = 28
_MESSAGE_BOX_FOREGROUND_COLOR = (255, 0, 0)
_MESSAGE_BOX_BACKGROUND_COLOR = (0, 0, 0)


class GameEngine:

    def __init__(self, canvasWidth, canvasHeight):
        self.__canvas = Rectangle(0, 0, canvasWidth, canvasHeight)
        self.__boundaries = Rectangle(self.__canvas.left, self.__canvas.bottom + _PADDLE_SPEED_BAR_HEIGHT,
            self.__canvas.right, self.__canvas.top - _INFORMATION_BAR_HEIGHT)

        self.__informationBarFont = None
        self.__messageBoxFont = None

        self.__levelFactory = LevelFactory(self)
        self.__currentLevel = None
        self.__state = None
        self.__totalPoints = 0

        self.__blocks = []
        self.__balls = []
        self.__paddle = Paddle(self)

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
    def state(self):
        return self.__state

    @property
    def totalPoints(self):
        return self.__totalPoints


    def initialize(self):
        self.__informationBarFont = Font(_INFORMATION_BAR_FONT_FILE, _INFORMATION_BAR_FONT_SIZE)
        self.__messageBoxFont = Font(_MESSAGE_BOX_FONT_FILE, _MESSAGE_BOX_FONT_SIZE)

        self.__paddle.position = Vector((self.__boundaries.right/2.0, self.__boundaries.bottom + self.__paddle.height))

        self.__loadLevel(self.__levelFactory.buildLevel(1))
        self.__playBackgroundMusic()
        self.__state = GameState.PLAY

    def reset(self):
        self.__balls = []
        self.__blocks = []
        self.__paddle.position.x = self.boundaries.right/2.0
        self.__totalPoints = 0
        self.__stopBackgroundMusic()
        self.initialize()

    def __loadLevel(self, level):
        self.__balls = list(level.balls)
        self.__blocks = list(level.blocks)
        self.__currentLevel = level

    def __playBackgroundMusic(self):
        if self.__currentLevel.backgroundMusic is not None:
            self.__currentLevel.backgroundMusic.play(-1)

    def __stopBackgroundMusic(self):
        if self.__currentLevel.backgroundMusic is not None:
            self.__currentLevel.backgroundMusic.stop()

    def update(self, milliseconds, tick):
        if self.__state is None:
            raise Exception("Invalid operation. Did you forget to call initialize() first?")

        self.__updateState()
        if self.__state == GameState.PLAY:
            self.__updateGameObjects(milliseconds, tick)

    def __updateState(self):
        if len(self.__balls) == 0:
            self.__state = GameState.LOST
        elif len(self.__blocks) == 0:
            self.__state = GameState.WON
        if self.__state == GameState.HALT_RUN_CYCLE:
            self.__state = GameState.HALT

    def __updateGameObjects(self, milliseconds, tick):
        if (self.__state == GameState.PLAY) or (self.__state == GameState.HALT_RUN_CYCLE):
            for gameObject in self.gameObjects:
                gameObject.update(milliseconds, tick)

    def destroyBlock(self, block):
        if block in self.__blocks:
            self.__totalPoints += block.points
            self.__blocks.remove(block)
            del block

    def destroyBall(self, ball):
        if ball in self.__balls:
            self.__balls.remove(ball)
            del ball

    def display(self, milliseconds, tick, screen_width, screen_height):
        if self.__state is None:
            raise Exception("Invalid operation. Did you forget to call initialize() first?")
        glClear(GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT)   # clear the screen
        self.__drawBackground(screen_height, screen_width)
        self.__drawPaddleSpeedBar()
        self.__drawInformationBar()
        self.__drawGameObjects(milliseconds, tick)
        self.__drawMessageBox()


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
        status = (" Level %d  |  Balls %d  |  Points %d " % (self.__currentLevel.index, len(self.__balls), self.__totalPoints))
        x = self.__canvas.left
        y = self.__canvas.top - _INFORMATION_BAR_HEIGHT
        glRasterPos2d(x, y)
        glPixelZoom(1, 1)
        renderedStatus = self.__informationBarFont.render(status, True,
                                            _INFORMATION_BAR_FOREGROUND_COLOR, _INFORMATION_BAR_BACKGROUND_COLOR)
        renderedStatusBytes = pygame.image.tostring(renderedStatus, "RGBA", 1)
        renderedStatusSize = renderedStatus.get_size()
        glDrawPixels(renderedStatusSize[0], renderedStatusSize[1], GL_RGBA, GL_UNSIGNED_BYTE, renderedStatusBytes)

    def __drawPaddleSpeedBar(self):
        glColor(0, 0, 0)
        glBegin(GL_POLYGON)
        glVertex(self.__canvas.left, self.__canvas.bottom)
        glVertex(self.__canvas.right, self.__canvas.bottom)
        glVertex(self.__canvas.right, self.__canvas.bottom + _PADDLE_SPEED_BAR_HEIGHT)
        glVertex(self.__canvas.left, self.__canvas.bottom + _PADDLE_SPEED_BAR_HEIGHT)
        glEnd()
        half = (self.__canvas.right - self.__canvas.left) / 2
        paddleSpeed = self.__paddle.speed.x
        glBegin(GL_POLYGON)
        glColor(0.8, 0.8, 0)
        glVertex(half, self.__canvas.bottom)
        glVertex(half, self.__canvas.bottom + _PADDLE_SPEED_BAR_HEIGHT)
        glVertex(paddleSpeed * half / _PADDLE_MAX_SPEED + half, self.__canvas.bottom + _PADDLE_SPEED_BAR_HEIGHT)
        glVertex(paddleSpeed * half / _PADDLE_MAX_SPEED + half, self.__canvas.bottom)
        glEnd()
        glBegin(GL_LINES)
        glVertex(self.__canvas.left, self.__canvas.bottom)
        glVertex(self.__canvas.right, self.__canvas.bottom)
        glEnd()

    def __drawMessageBox(self):
        if self.__state == GameState.PAUSE:
            text = "Pause"
        elif self.__state == GameState.LOST:
            text = "Game Over"
        elif self.__state == GameState.WON:
            text = "Congratulations"
        else:
            text = None

        if text is not None:
            renderedText = self.__messageBoxFont.render(text, True,
                                                        _MESSAGE_BOX_FOREGROUND_COLOR, _MESSAGE_BOX_BACKGROUND_COLOR)
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
        if button == MouseButton.RIGHT:
            self.__printDebugInfo()
            if self.__state == GameState.HALT:
                self.__state = GameState.HALT_RUN_CYCLE
            else:
                self.__state = GameState.HALT
        if button == MouseButton.LEFT:
            self.__togglePauseState()

    def handleMouseButtonUpEvent(self, button, coordinates):
        pass

    def handleKeyDownEvent(self, key, modifiers, char):
        if key == K_q:
            print "Game aborted."
            sys.exit()
        if key == K_r:
            print "Game reset."
            self.reset()
        if key == K_SPACE or key == K_p:
            self.__togglePauseState()

    def __togglePauseState(self):
        if self.__state == GameState.HALT or self.__state == GameState.PAUSE:
            self.__state = GameState.PLAY
        elif self.__state == GameState.PLAY:
            self.__state = GameState.PAUSE

    def handleKeyUpEvent(self, key, modifiers):
        pass

    def handleMouseMoveEvent(self, absoluteCoordinates, relativeCoordinates, buttons):
        if self.__state == GameState.PLAY or self.__state == GameState.HALT or self.__state == GameState.HALT_RUN_CYCLE:
            (x, y) = absoluteCoordinates
            median = (self.__canvas.right - self.__canvas.left) / 2
            paddleSpeed = (x - median) / median
            paddleSpeed *= _PADDLE_MAX_SPEED
            self.__paddle.speed.x = paddleSpeed

