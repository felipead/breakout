

class AbstractLevelBuilder:

    def __init__(self, engine, index):
        self._engine = engine
        self._index = index

    def build(self):
        raise NotImplemented()
