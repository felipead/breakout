from pygame.constants import *
from breakout.BreakoutEngine import BreakoutEngine
from breakout.geometry.Rectangle import Rectangle

from util.Drawing import *

_FRAME_RATE = 60
_MOUSE_VISIBLE = True

_DEFAULT_SCREEN_WIDTH = 500
_DEFAULT_SCREEN_HEIGHT = 600

CANVAS_SCREEN_RATIO = 0.5

CANVAS_LEFT = 0
CANVAS_BOTTOM = 0
CANVAS_RIGHT = _DEFAULT_SCREEN_WIDTH * CANVAS_SCREEN_RATIO
CANVAS_TOP = _DEFAULT_SCREEN_HEIGHT * CANVAS_SCREEN_RATIO

class BreakoutController:

    def __init__(self):
        self._engine = BreakoutEngine(Rectangle(CANVAS_LEFT, CANVAS_BOTTOM, CANVAS_RIGHT, CANVAS_TOP))
        self._screen_width = _DEFAULT_SCREEN_WIDTH
        self._screen_height = _DEFAULT_SCREEN_HEIGHT

    def run(self):

        pygame.display.set_mode((self._screen_width, self._screen_height), OPENGL | DOUBLEBUF)
        self._handle_screen_resize_event(self._screen_width, self._screen_height)

        self._initialize()
        self._game_loop()

    def _initialize(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glShadeModel(GL_FLAT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendEquation(GL_FUNC_ADD)

        pygame.init()
        pygame.mouse.set_visible(_MOUSE_VISIBLE)
        self._engine.initialize()

    def _game_loop(self):
        clock = pygame.time.Clock()
        clock_ticks = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                self._handle_input_event(event)

            elapsed_milliseconds = clock.tick(_FRAME_RATE)
            clock_ticks += 1

            self._engine.update(elapsed_milliseconds, clock_ticks)
            self._engine.display(elapsed_milliseconds, clock_ticks, self._screen_width, self._screen_height)

            pygame.display.flip()  # swap buffers


    def _handle_input_event(self, event):
        if event.type == VIDEORESIZE:
            self._handle_screen_resize_event(event.w, event.h)
        elif event.type == MOUSEMOTION:
            self._handle_mouse_move_event(event.pos, event.rel, event.buttons)
        elif event.type == MOUSEBUTTONUP:
            self._handle_mouse_button_up_event(event.button, event.pos)
        elif event.type == MOUSEBUTTONDOWN:
            self._handle_mouse_button_down_event(event.button, event.pos)
        elif event.type == KEYUP:
            self._handle_key_up_event(event.key, event.mod)
        elif event.type == KEYDOWN:
            self._handle_key_down_event(event.key, event.mod, event.unicode)


    def _handle_screen_resize_event(self, width, height):
        self._screen_width = width
        self._screen_height = height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(CANVAS_LEFT, CANVAS_RIGHT, CANVAS_BOTTOM, CANVAS_TOP)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _handle_mouse_button_up_event(self, button, coordinates):
        mapped_coordinates = self._map_screen_coordinates_to_canvas(coordinates)
        self._engine.handleMouseButtonUpEvent(button, mapped_coordinates)

    def _handle_mouse_button_down_event(self, button, coordinates):
        mappedCoordinates = self._map_screen_coordinates_to_canvas(coordinates)
        self._engine.handleMouseButtonDownEvent(button, mappedCoordinates)

    def _handle_mouse_move_event(self, absolute_coordinates, relative_coordinates, buttons):
        mapped_absolute_coordinates = self._map_screen_coordinates_to_canvas(absolute_coordinates)
        self._engine.handleMouseMoveEvent(mapped_absolute_coordinates, relative_coordinates, buttons)

    def _handle_key_up_event(self, key, modifiers):
        self._engine.handleKeyUpEvent(key, modifiers)

    def _handle_key_down_event(self, key, modifiers, char):
        self._engine.handleKeyDownEvent(key, modifiers, char)

    def _map_screen_coordinates_to_canvas(self, coordinates):
        (x, y) = coordinates
        x = x * CANVAS_SCREEN_RATIO
        y = y * CANVAS_SCREEN_RATIO
        y = CANVAS_TOP - y
        return (x, y)
