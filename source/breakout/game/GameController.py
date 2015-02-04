from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.constants import *

from breakout.game.GameEngine import GameEngine


_FRAMES_PER_SECOND = 60
_MOUSE_VISIBLE = True

_CANVAS_WIDTH = 250
_CANVAS_HEIGHT = 300
_DEFAULT_SCREEN_WIDTH = 500
_DEFAULT_SCREEN_HEIGHT = 600


class GameController:

    def __init__(self):
        self.__engine = GameEngine(_CANVAS_WIDTH, _CANVAS_HEIGHT)
        self.__screenWidth = _DEFAULT_SCREEN_WIDTH
        self.__screenHeight = _DEFAULT_SCREEN_HEIGHT

    def run(self):
        self.__initialize()
        self.__gameLoop()

    def __initialize(self):
        pygame.init()
        pygame.mouse.set_visible(_MOUSE_VISIBLE)
        pygame.display.set_mode((self.__screenWidth, self.__screenHeight), OPENGL | DOUBLEBUF)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_FLAT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquation(GL_FUNC_ADD)

        self.__handleScreenResizeEvent(self.__screenWidth, self.__screenHeight)
        self.__engine.initialize()

    def __gameLoop(self):
        clock = pygame.time.Clock()
        ticks = 0
        while True:
            for event in pygame.event.get():
                self.__handleInputEvent(event)

            milliseconds = clock.tick(_FRAMES_PER_SECOND)
            ticks += 1

            self.__engine.update(milliseconds, ticks)
            self.__engine.display(milliseconds, ticks, self.__screenWidth, self.__screenHeight, clock.get_fps())

            pygame.display.flip()  # swap buffers

    def __handleInputEvent(self, event):
        if event.type == QUIT:
            exit()
        elif event.type == VIDEORESIZE:
            self.__handleScreenResizeEvent(event.w, event.h)
        elif event.type == MOUSEMOTION:
            self.__handleMouseMoveEvent(event.pos, event.rel, event.buttons)
        elif event.type == MOUSEBUTTONUP:
            self.__handleMouseButtonUpEvent(event.button, event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            self.__handleMouseButtonDownEvent(event.button, event.pos)
        elif event.type == KEYUP:
            self.__handleKeyUpEvent(event.key, event.mod)
        elif event.type == KEYDOWN:
            self.__handleKeyDownEvent(event.key, event.mod, event.unicode)

    def __handleScreenResizeEvent(self, width, height):
        self.__screenWidth = width
        self.__screenHeight = height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self.__engine.canvas.left, self.__engine.canvas.right,
                   self.__engine.canvas.bottom, self.__engine.canvas.top)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def __handleMouseButtonUpEvent(self, button, coordinates):
        mappedCoordinates = self.__mapScreenCoordinatesToCanvas(coordinates)
        self.__engine.handleMouseButtonUpEvent(button, mappedCoordinates)

    def __handleMouseButtonDownEvent(self, button, coordinates):
        mappedCoordinates = self.__mapScreenCoordinatesToCanvas(coordinates)
        self.__engine.handleMouseButtonDownEvent(button, mappedCoordinates)

    def __handleMouseMoveEvent(self, absolute_coordinates, relative_coordinates, buttons):
        mapped_absolute_coordinates = self.__mapScreenCoordinatesToCanvas(absolute_coordinates)
        self.__engine.handleMouseMoveEvent(mapped_absolute_coordinates, relative_coordinates, buttons)

    def __handleKeyUpEvent(self, key, modifiers):
        self.__engine.handleKeyUpEvent(key, modifiers)

    def __handleKeyDownEvent(self, key, modifiers, char):
        self.__engine.handleKeyDownEvent(key, modifiers, char)

    def __mapScreenCoordinatesToCanvas(self, coordinates):
        horizontalCanvasToScreenRatio = self.__engine.canvas.width / float(self.__screenWidth)
        verticalCanvasToScreenRatio = self.__engine.canvas.height / float(self.__screenHeight)

        (x, y) = coordinates
        x *= horizontalCanvasToScreenRatio
        y *= verticalCanvasToScreenRatio

        y = self.__engine.canvas.top - y
        return x, y
