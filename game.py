from enum import Enum, auto
from player_mode import PLayerMode
from algo_player_mode import algorithmPlayerMode

class Mode(Enum):
    PLAYER_MODE = auto()
    ALGORITHM_AND_PLAYER_MODE = auto()
    ALGORITHM_MODE = auto()

class Game:
    """
    this class guide you to game mode
    e.g: Game -> PLayer_mode
              -> algo_player_mode
              -> algorithm_mode
    """
    def __init__(self, mode:Mode):
        self.mode = mode

    def run(self):
        if self.mode == Mode.PLAYER_MODE:
            game_loop = PLayerMode()
        elif self.mode == Mode.ALGORITHM_AND_PLAYER_MODE:
            game_loop = algorithmPlayerMode()
        elif self.mode == Mode.ALGORITHM_MODE:
            game_loop = PLayerMode()
        game_loop.run()
