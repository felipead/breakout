from pygame.mixer import Sound
from breakout.domain.Color import Color

from breakout.game.building.AbstractLevelBuilder import AbstractLevelBuilder
from breakout.domain.Ball import Ball
from breakout.domain.Block import Block
from breakout.game.Level import Level
from breakout.geometry.Vector import Vector
from breakout.util.Drawing import Drawing

_FILE_MUSIC_LEVEL1 = 'breakout/resources/sounds/ChemicalBurn.wav'
_FILE_BACKGROUND_LEVEL1 = 'breakout/resources/graphics/Level1.png'

_BALL_RADIUS = 3.0
_BALL_SPEED = 0.075
_BLOCK_WIDTH = 20
_BLOCK_HEIGHT = 10

class Level1Builder(AbstractLevelBuilder):

    def __init__(self, engine):
        AbstractLevelBuilder.__init__(self, engine, 1)

    def build(self):
        level = Level(1)
        level.backgroundTexture = Drawing.loadTexture(_FILE_BACKGROUND_LEVEL1, False)
        level.backgroundMusic = Sound(_FILE_MUSIC_LEVEL1)

        level.blocks = self.__buildBlocks()
        level.balls = self.__buildBalls()

        return level

    def __buildBlocks(self):
        boundaries = self._engine.boundaries

        columns = (int)(boundaries.width // _BLOCK_WIDTH)
        rows = (int)(boundaries.height // _BLOCK_HEIGHT)
        blocks = []

        for i in xrange(3, columns - 1):
            for j in xrange(15, rows - 3):
                color = self.__chooseColor(j % 3 + 1)
                position = Vector((boundaries.left + i * _BLOCK_WIDTH, boundaries.bottom + j * _BLOCK_HEIGHT))
                block = Block(self._engine, position, color=color, width=_BLOCK_WIDTH, height=_BLOCK_HEIGHT)
                blocks.append(block)

        for i in xrange(3, columns - 1):
            color = self.__chooseColor(i % 3 + 1)
            j = 10
            position = Vector((boundaries.left + i * _BLOCK_WIDTH, boundaries.bottom + j * _BLOCK_HEIGHT))
            block = Block(self._engine, position, color=color, width=_BLOCK_WIDTH, height=_BLOCK_HEIGHT)
            blocks.append(block)

        return blocks

    def __buildBalls(self):
        boundaries = self._engine.boundaries

        ball1 = Ball(self._engine,
                     position=Vector((boundaries.width / 2, boundaries.top - _BALL_RADIUS)),
                     speed=Vector((-_BALL_SPEED, _BALL_SPEED)), radius=_BALL_RADIUS)
        ball2 = Ball(self._engine,
                     position=Vector((boundaries.right - _BALL_RADIUS, boundaries.top - _BALL_RADIUS)),
                     speed=Vector((-_BALL_SPEED, -_BALL_SPEED)), radius=_BALL_RADIUS)
        ball3 = Ball(self._engine,
                     position=Vector((boundaries.left + _BALL_RADIUS, boundaries.top - _BALL_RADIUS)),
                     speed=Vector((_BALL_SPEED, -_BALL_SPEED)), radius=_BALL_RADIUS)

        return [ball1, ball2, ball3]

    def __chooseColor(self, index):
        if index == 1:
            return Color.RED
        elif index == 2:
            return Color.GREEN
        elif index == 3:
            return Color.BLUE