from OpenGL.GL import *
import math
import pygame

_CIRCLE_LENGTH = 2 * math.pi

class Drawing(object):

    @staticmethod
    def loadTexture(filename, use_alpha=False):
        if use_alpha:
            imageFormat, openGlFormat, bitsPerPixel = 'RGBA', GL_RGBA, 4
        else:
            imageFormat, openGlFormat, bitsPerPixel = 'RGB', GL_RGB, 3

        # Load texture and extract the raw data
        imageSurface = pygame.image.load(filename)
        data = pygame.image.tostring(imageSurface, imageFormat, True)

        # Generate and bind a texture id
        textureId = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureId)

        # Set texture parameters and alignment
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        # Upload texture data
        width, height = imageSurface.get_rect().size
        glTexImage2D(GL_TEXTURE_2D, 0, bitsPerPixel, width, height, 0, openGlFormat, GL_UNSIGNED_BYTE, data)

        # Return the texture id, so we can use glBindTexture
        return textureId

    @staticmethod
    def drawRenderedText(x, y, renderedText):
        glRasterPos2d(x, y)
        glPixelZoom(1, 1)
        renderedTextBytes = pygame.image.tostring(renderedText, "RGBA", 1)
        renderedTextSize = renderedText.get_size()
        glDrawPixels(renderedTextSize[0], renderedTextSize[1], GL_RGBA, GL_UNSIGNED_BYTE, renderedTextBytes)

    @staticmethod
    def drawLine2d(point1, point2, rgbColor):
        if rgbColor is not None:
            glColor(*rgbColor)

        glBegin(GL_LINES)
        glVertex(point1[0], point1[1])
        glVertex(point2[0], point2[1])
        glEnd()

    @staticmethod
    def drawCircle2d(x, y, radius, rgbColor=None, numberOfEdges=6, radianOffset=0):
        if rgbColor is not None:
            glColor(*rgbColor)
        if numberOfEdges < 3:
            raise Exception("number of edges must be greater or equal than 3")

        angleStep = _CIRCLE_LENGTH / float(numberOfEdges)

        glBegin(GL_POLYGON)
        radians = 0
        while radians < _CIRCLE_LENGTH:
            glVertex(x + math.cos(radians + radianOffset) * radius, y + math.sin(radians + radianOffset) * radius)
            radians += angleStep
        glEnd()

    @staticmethod
    def drawRectangle2d(x, y, dx, dy, rgbColor):
        vertex1 = (x - dx, y + dy)
        vertex2 = (x + dx, y + dy)
        vertex3 = (x + dx, y - dy)
        vertex4 = (x - dx, y - dy)
        Drawing.drawQuadrilateral2d(vertex1, vertex2, vertex3, vertex4, rgbColor)

    @staticmethod
    def drawQuadrilateral2d(vertex1, vertex2, vertex3, vertex4, rgbColor=None):
        if rgbColor is not None:
            glColor(*rgbColor)

        glBegin(GL_POLYGON)
        glVertex(vertex1[0], vertex1[1])
        glVertex(vertex2[0], vertex2[1])
        glVertex(vertex3[0], vertex3[1])
        glVertex(vertex4[0], vertex4[1])
        glEnd()
