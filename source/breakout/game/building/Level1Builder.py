from pygame.mixer import Sound
from breakout.model.BlockColor import BlockColor

from breakout.game.building.AbstractLevelBuilder import AbstractLevelBuilder
from breakout.model.Ball import Ball
from breakout.model.Block import Block
from breakout.model.Level import Level
from breakout.geometry.Vector import Vector
from breakout.util.Drawing import Drawing

_BLOCK_COLUMNS = 12
_BLOCK_ROWS = 30

_BACKGROUND_MUSIC_FILE = 'breakout/resources/sounds/ChemicalBurn.wav'
_BACKGROUND_TEXTURE_FILE = 'breakout/resources/graphics/Level1.png'

_BALL_RADIUS = 3.0
_BALL_SPEED = 0.075

class Level1Builder(AbstractLevelBuilder):

    def __init__(self, engine):
        AbstractLevelBuilder.__init__(self, engine, 1)

    def build(self):
        level = Level(1)
        level.backgroundTexture = Drawing.loadTexture(_BACKGROUND_TEXTURE_FILE, False)
        level.backgroundMusic = Sound(_BACKGROUND_MUSIC_FILE)
        level.blocks = self.__buildBlocks()
        level.balls = self.__buildBalls()
        return level

    def __buildBlocks(self):
        boundaries = self._engine.boundaries
        blockHeight = boundaries.height / float(_BLOCK_ROWS)
        blockWidth = boundaries.width / float(_BLOCK_COLUMNS)

        blocks = []
        blockColorIndex = 0
        for j in [27, 26, 25, 24, 23, 22, 21, 20, 15, 14, 13, 12, 11, 10, 9, 8]:
            blockColor = BlockColor.selectInRainbowOrder(blockColorIndex)
            blockColorIndex += 1
            for i in xrange(3, _BLOCK_COLUMNS - 2):
                position = Vector((boundaries.left + i * blockWidth, boundaries.bottom + j * blockHeight))
                block = Block(self._engine, position, blockColor, width=blockWidth, height=blockHeight)
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
