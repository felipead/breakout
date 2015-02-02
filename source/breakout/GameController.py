from OpenGL.GL import *
from OpenGL.GLU import *

import pygame
from pygame.constants import *
from breakout.GameEngine import GameEngine

_FRAMES_PER_SECOND = 60
_MOUSE_VISIBLE = True

_CANVAS_WIDTH = 250
_CANVAS_HEIGHT = 300
_DEFAULT_SCREEN_WIDTH = 500
_DEFAULT_SCREEN_HEIGHT = 600


class GameController:

    def __init__(self):
        self._engine = GameEngine(_CANVAS_WIDTH, _CANVAS_HEIGHT)
        self._screenWidth = _DEFAULT_SCREEN_WIDTH
        self._screenHeight = _DEFAULT_SCREEN_HEIGHT

    def run(self):
        self._initialize()
        self._gameLoop()

    def _initialize(self):
        pygame.init()
        pygame.mouse.set_visible(_MOUSE_VISIBLE)
        pygame.display.set_mode((self._screenWidth, self._screenHeight), OPENGL | DOUBLEBUF)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_FLAT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquation(GL_FUNC_ADD)

        self._handleScreenResizeEvent(self._screenWidth, self._screenHeight)
        self._engine.initialize()


    def _gameLoop(self):
        clock = pygame.time.Clock()
        ticks = 0
        while True:
            for event in pygame.event.get():
                self._handleInputEvent(event)

            milliseconds = clock.tick(_FRAMES_PER_SECOND)
            ticks += 1

            self._engine.update(milliseconds, ticks)
            self._engine.display(milliseconds, ticks, self._screenWidth, self._screenHeight)

            pygame.display.flip()  # swap buffers


    def _handleInputEvent(self, event):
        if event.type == QUIT:
            exit()
        elif event.type == VIDEORESIZE:
            self._handleScreenResizeEvent(event.w, event.h)
        elif event.type == MOUSEMOTION:
            self._handleMouseMoveEvent(event.pos, event.rel, event.buttons)
        elif event.type == MOUSEBUTTONUP:
            self._handleMouseButtonUpEvent(event.button, event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            self._handleMouseButtonDownEvent(event.button, event.pos)
        elif event.type == KEYUP:
            self._handleKeyUpEvent(event.key, event.mod)
        elif event.type == KEYDOWN:
            self._handleKeyDownEvent(event.key, event.mod, event.unicode)


    def _handleScreenResizeEvent(self, width, height):
        self._screenWidth = width
        self._screenHeight = height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(self._engine.canvas.left, self._engine.canvas.right,
                   self._engine.canvas.bottom, self._engine.canvas.top)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _handleMouseButtonUpEvent(self, button, coordinates):
        mappedCoordinates = self._mapScreenCoordinatesToCanvas(coordinates)
        self._engine.handleMouseButtonUpEvent(button, mappedCoordinates)

    def _handleMouseButtonDownEvent(self, button, coordinates):
        mappedCoordinates = self._mapScreenCoordinatesToCanvas(coordinates)
        self._engine.handleMouseButtonDownEvent(button, mappedCoordinates)

    def _handleMouseMoveEvent(self, absolute_coordinates, relative_coordinates, buttons):
        mapped_absolute_coordinates = self._mapScreenCoordinatesToCanvas(absolute_coordinates)
        self._engine.handleMouseMoveEvent(mapped_absolute_coordinates, relative_coordinates, buttons)

    def _handleKeyUpEvent(self, key, modifiers):
        self._engine.handleKeyUpEvent(key, modifiers)

    def _handleKeyDownEvent(self, key, modifiers, char):
        self._engine.handleKeyDownEvent(key, modifiers, char)

    def _mapScreenCoordinatesToCanvas(self, coordinates):
        horizontalCanvasToScreenRatio = self._engine.canvas.width / float(self._screenWidth)
        verticalCanvasToScreenRatio = self._engine.canvas.height / float(self._screenHeight)

        (x, y) = coordinates
        x *= horizontalCanvasToScreenRatio
        y *= verticalCanvasToScreenRatio

        y = self._engine.canvas.top - y
        return x, y
