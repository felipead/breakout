from enum import Enum


class GameState(Enum):
    PLAY = 1
    PAUSE = 2
    HALT = 3
    HALT_RUN_CYCLE = 4
    LOST = 5
    WON = 6
