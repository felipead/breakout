from enum import Enum
from breakout.model.Color import Color


class BlockColor(Enum):

    class Holder:

        def __init__(self, color, points):
            self.__color = color
            self.__points = points

        @property
        def color(self):
            return self.__color

        @property
        def points(self):
            return self.__points

    RED = Holder(Color.RED, 10)
    ORANGE = Holder(Color.ORANGE, 20)
    YELLOW = Holder(Color.YELLOW, 30)
    LIME = Holder(Color.LIME, 40)
    TEAL = Holder(Color.TEAL, 50)
    BLUE = Holder(Color.BLUE, 60)
    INDIGO = Holder(Color.INDIGO, 70)
    VIOLET = Holder(Color.VIOLET, 80)

    @classmethod
    def selectInRainbowOrder(cls, index):
        index %= 8
        if index == 0:
            return BlockColor.RED
        elif index == 1:
            return BlockColor.ORANGE
        elif index == 2:
            return BlockColor.YELLOW
        elif index == 3:
            return BlockColor.LIME
        elif index == 4:
            return BlockColor.TEAL
        elif index == 5:
            return BlockColor.BLUE
        elif index == 6:
            return BlockColor.INDIGO
        elif index == 7:
            return BlockColor.VIOLET
