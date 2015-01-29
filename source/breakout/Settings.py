# encoding: utf-8


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

FILE_BACKGROUND_LEVEL1 = 'breakout/resources/graphics/Level1.png'

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