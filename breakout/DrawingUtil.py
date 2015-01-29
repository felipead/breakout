# encoding: utf-8
"""
Copyright (c) 2010 Felipe Augusto Dornelas. All rights reserved.
"""

from OpenGL.GL import *

import pygame


#===================================================================================================

def loadTexture(filename, use_alpha=False):
    # Read an image file and upload a texture
    if use_alpha:
        format, gl_format, bits_per_pixel = 'RGBA', GL_RGBA, 4
    else:
        format, gl_format, bits_per_pixel = 'RGB', GL_RGB, 3

    # Load texture and extract the raw data
    img_surface = pygame.image.load(filename)
    data = pygame.image.tostring(img_surface, format, True)

    # Generate and bind a texture id
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters and alignment
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # Upload texture data
    width, height = img_surface.get_rect().size
    glTexImage2D(GL_TEXTURE_2D,
        0,
        bits_per_pixel,
        width, height,
        0,
        gl_format,
        GL_UNSIGNED_BYTE, data)

    # Return the texture id, so we can use glBindTexture
    return texture_id


#===================================================================================================

def drawCircle(x, y, radius):
    i = radius/7.0

    glBegin(GL_POLYGON)

    glVertex(x+1*i, y+7*i)
    glVertex(x+2*i, y+6*i)
    glVertex(x+3*i, y+5*i)
    glVertex(x+4*i, y+4*i)
    glVertex(x+5*i, y+3*i)
    glVertex(x+6*i, y+2*i)
    glVertex(x+7*i, y+1*i)

    glVertex(x+7*i, y-1*i)
    glVertex(x+6*i, y-2*i)
    glVertex(x+5*i, y-3*i)
    glVertex(x+4*i, y-4*i)
    glVertex(x+3*i, y-5*i)
    glVertex(x+2*i, y-6*i)
    glVertex(x+1*i, y-7*i)

    glVertex(x-1*i, y-7*i)
    glVertex(x-2*i, y-6*i)
    glVertex(x-3*i, y-5*i)
    glVertex(x-4*i, y-4*i)
    glVertex(x-5*i, y-3*i)
    glVertex(x-6*i, y-2*i)
    glVertex(x-7*i, y-1*i)

    glVertex(x-7*i, y+1*i)
    glVertex(x-6*i, y+2*i)
    glVertex(x-5*i, y+3*i)
    glVertex(x-4*i, y+4*i)
    glVertex(x-3*i, y+5*i)
    glVertex(x-2*i, y+6*i)
    glVertex(x-1*i, y+7*i)

    glEnd()
