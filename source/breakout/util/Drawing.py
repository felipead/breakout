from OpenGL.GL import *
import math
import pygame


class Drawing:

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
    def drawCircle2d(x, y, radius, color=None, numberOfEdges=16):
        if color is not None:
            glColor(*color)

        glBegin(GL_POLYGON)

        i = 0
        while i < (2 * math.pi):
            glVertex(x + (math.cos(i) * radius), y + (math.sin(i) * radius))
            i += math.pi / float(numberOfEdges)

        glEnd()