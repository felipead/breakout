# encoding: utf-8
"""
Copyright (c) 2010 Felipe Augusto Dornelas. All rights reserved.
"""

#===================================================================================================

# Screen and canvas dimensions constants

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600

CANVAS_SCREEN_RATIO = 0.5

CANVAS_LEFT = 0
CANVAS_BOTTOM = 0
CANVAS_RIGHT = SCREEN_WIDTH * CANVAS_SCREEN_RATIO
CANVAS_TOP = SCREEN_HEIGHT * CANVAS_SCREEN_RATIO

# Display frame rate, in FPS. 0 for no display sync.
FRAME_RATE = 60

#===================================================================================================

BALL_SPEED_DEFAULT = 0.05
BALL_RADIUS = 3.0

VELOCITYBAR_HEIGHT = 3.0
INFOBAR_HEIGHT = 12.0

PADDLE_SPEED_MAX = 0.75
PADDLE_HEIGHT = 5.0

BLOCK_COLOR_RED = 1
BLOCK_COLOR_BLUE = 2
BLOCK_COLOR_GREEN = 3

BLOCK_POINTS_BLUE = 10
BLOCK_POINTS_GREEN = 20
BLOCK_POINTS_RED = 30

#===================================================================================================

# Collision constants

COLLISION_BALL_WALL = 1
COLLISION_BALL_BALL = 2
COLLISION_BALL_BLOCK = 4
COLLISION_BALL_PADDLE = 8

#===================================================================================================

# Input

MOUSE_VISIBLE = True

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 3
MOUSE_BUTTON_SCROLLUP = 4
MOUSE_BUTTON_SCROLLDOWN = 5

#===================================================================================================

# Media file names

FILE_SOUND_COLLISION_BALL_WALL = 'breakout/resources/sounds/Pop.wav'
FILE_SOUND_COLLISION_BALL_BALL = 'breakout/resources/sounds/Bottle.wav'
FILE_SOUND_COLLISION_BALL_BLOCK = 'breakout/resources/sounds/Tuntz.wav'
FILE_SOUND_COLLISION_BALL_PADDLE = 'breakout/resources/sounds/Ping.wav'
FILE_SOUND_BALL_DESTROYED = 'breakout/resources/sounds/Basso.wav'

FILE_BACKGROUND_LEVEL1 = 'breakout/resources/graphics/Stage1.png'

FILE_MUSIC_LEVEL1 = 'breakout/resources/sounds/ChemicalBurn.wav'

#===================================================================================================

# Fonts

FILE_FONT_INFOBAR = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'
FILE_FONT_MESSAGE = 'breakout/resources/fonts/pf_tempesta_five_extended.ttf'

FONT_INFOBAR_SIZE = 14
FONT_INFOBAR_COLOR_FOREGROUND = (255, 255, 255)
FONT_INFOBAR_COLOR_BACKGROUND = (0, 0, 0)

FONT_MESSAGE_SIZE = 28
FONT_MESSAGE_COLOR_FOREGROUND = (255, 0, 0)
FONT_MESSAGE_COLOR_BACKGROUND = (0, 0, 0)