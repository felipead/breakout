from pygame.mixer import Sound
from breakout.model.BlockColor import BlockColor

from breakout.game.building.AbstractLevelBuilder import AbstractLevelBuilder
from breakout.model.Ball import Ball
from breakout.model.Block import Block
from breakout.model.Level import Level
from breakout.geometry.Vector2d import Vector2d
from breakout.util.Drawing import Drawing

_BLOCK_COLUMNS = 12
_BLOCK_ROWS = 30

_BACKGROUND_MUSIC_FILE = 'breakout/resources/music/ChemicalBurn.ogg'
_BACKGROUND_TEXTURE_FILE = 'breakout/resources/graphics/Level1.png'

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
        boundaries = self._engine.rectangle
        blockHeight = boundaries.height / float(_BLOCK_ROWS)
        blockWidth = boundaries.width / float(_BLOCK_COLUMNS)

        blocks = []
        blockColorIndex = 0
        for j in [27, 26, 25, 24, 23, 22, 21, 20, 15, 14, 13, 12, 11, 10, 9, 8]:
            blockColor = BlockColor.selectInRainbowOrder(blockColorIndex)
            blockColorIndex += 1
            for i in xrange(3, _BLOCK_COLUMNS - 2):
                block = Block(self._engine, blockColor, width=blockWidth, height=blockHeight)
                block.position = Vector2d(boundaries.left + i * blockWidth, boundaries.bottom + j * blockHeight)
                blocks.append(block)

        return blocks

    def __buildBalls(self):
        boundaries = self._engine.rectangle

        ball1 = Ball(self._engine)
        ball1.position = Vector2d(boundaries.width/2.0, boundaries.top - ball1.radius)
        ball1.speed = Vector2d(-_BALL_SPEED, _BALL_SPEED)

        ball2 = Ball(self._engine)
        ball2.position = Vector2d(boundaries.right - ball2.radius, boundaries.top - ball2.radius)
        ball2.speed = Vector2d(-_BALL_SPEED, -_BALL_SPEED)

        ball3 = Ball(self._engine)
        ball3.position = Vector2d(boundaries.left + ball3.radius, boundaries.top - ball3.radius)
        ball3.speed = Vector2d(_BALL_SPEED, -_BALL_SPEED)

        return [ball1, ball2, ball3]
