from breakout.game.building.Level1Builder import Level1Builder


class LevelFactory(object):

    def __init__(self, engine):
        self._engine = engine

    def buildLevel(self, index):
        if index == 1:
            return Level1Builder(self._engine).build()
        else:
            raise Exception("Level index does not exist: " + index)
