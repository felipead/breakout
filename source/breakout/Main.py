#!/usr/bin/env python
# encoding: utf-8


from pygame.locals import *

from breakout.Game import *
from breakout.geometry.Rectangle import Rectangle
from util.Drawing import *
from Settings import *


#===================================================================================================

# Static variables

game = Game(Rectangle(CANVAS_LEFT, CANVAS_BOTTOM, CANVAS_RIGHT, CANVAS_TOP)) # the game controller

#===================================================================================================

# System events handlers

def screenResizeEvent(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(CANVAS_LEFT, CANVAS_RIGHT, CANVAS_BOTTOM, CANVAS_TOP)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def mapScreenCoordinatesToCanvas(coordinates):
    (x, y) = coordinates
    x = x * CANVAS_SCREEN_RATIO
    y = y * CANVAS_SCREEN_RATIO
    y = CANVAS_TOP - y
    return (x, y)


def mouseButtonUpEvent(button, coordinates):
    mappedCoordinates = mapScreenCoordinatesToCanvas(coordinates)
    game.mouseButtonUpEvent(button, mappedCoordinates)


def mouseButtonDownEvent(button, coordinates):
    mappedCoordinates = mapScreenCoordinatesToCanvas(coordinates)
    game.mouseButtonDownEvent(button, mappedCoordinates)


def mouseMoveEvent(absoluteCoordinates, relativeCoordinates, buttons):
    mappedAbsoluteCoordinates = mapScreenCoordinatesToCanvas(absoluteCoordinates)
    game.mouseMoveEvent(mappedAbsoluteCoordinates, relativeCoordinates, buttons)


def keyUpEvent(key, modifiers):
    game.keyUpEvent(key, modifiers)


def keyDownEvent(key, modifiers, char):
    game.keyDownEvent(key, modifiers, char)


#===================================================================================================

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glShadeModel(GL_FLAT)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBlendEquation(GL_FUNC_ADD)

    pygame.init()
    game.init()


def run():
    # create the screen; set its default size
    defaultScreenSize = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(defaultScreenSize, OPENGL|DOUBLEBUF)
    screenResizeEvent(*defaultScreenSize)

    clock = pygame.time.Clock()
    tick = 0

    # show/hide the mouse pointer
    pygame.mouse.set_visible(MOUSE_VISIBLE)

    init()

    # the game main loop
    while True:
        # process input events
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == VIDEORESIZE:
                screenResizeEvent(event.w, event.h)
            if event.type == MOUSEMOTION:
                mouseMoveEvent(event.pos, event.rel, event.buttons)
            if event.type == MOUSEBUTTONUP:
                mouseButtonUpEvent(event.button, event.pos)
            if event.type == MOUSEBUTTONDOWN:
                mouseButtonDownEvent(event.button, event.pos)
            if event.type == KEYUP:
                keyUpEvent(event.key, event.mod)
            if event.type == KEYDOWN:
                keyDownEvent(event.key, event.mod, event.unicode)

        milliseconds = clock.tick(FRAME_RATE)
        tick = tick + 1

        # Updates the game logic
        game.update(milliseconds, tick)

        # Draws the game graphics
        game.display(milliseconds, tick)

        pygame.display.flip() # swap buffers

#===================================================================================================

if __name__ == "__main__":
    run()
