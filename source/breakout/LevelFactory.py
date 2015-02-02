from breakout.building.Level1Builder import Level1Builder


class LevelFactory:

    def __init__(self, engine):
        self._engine = engine
        self._levels = {}

    def getLevel(self, index):
        if self._levels.has_key(index):
            return self._levels[index]
        else:
            level = self.__buildLevel(index)
            self._levels[index] = level
            return level

    def __buildLevel(self, index):
        if index == 1:
            return Level1Builder(self._engine).build()
        else:
            raise Exception("Level index does not exist: " + index)
