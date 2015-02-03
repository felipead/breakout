from enum import Enum
from breakout.model.Color import Color


class BlockType(Enum):

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

    BLUE = Holder(Color.BLUE, 10)
    GREEN = Holder(Color.GREEN, 20)
    RED = Holder(Color.RED, 30)
    PURPLE = Holder(Color.PURPLE, 50)