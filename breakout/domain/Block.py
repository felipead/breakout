# encoding: utf-8

from MovableGameObject import *
from ..geometry.Rectangle import *

from OpenGL.GL import *
from OpenGL.GLU import *


BLOCK_COLOR_RED = 1
BLOCK_COLOR_BLUE = 2
BLOCK_COLOR_GREEN = 3

BLOCK_POINTS_BLUE = 10
BLOCK_POINTS_GREEN = 20
BLOCK_POINTS_RED = 30


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

