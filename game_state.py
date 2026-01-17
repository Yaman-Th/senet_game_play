from enum import Enum, auto

class PlayerColor(Enum):
    BLACK = auto()
    WHITE = auto()

class State:
    """
    the Game State contains:
        white positions (set),
        black positions (set),
        player turn (PlayerColor),
        sticks (int 1 -> 5),
        parent (state)
    """

    def __init__(self, white_positions:set = None, black_positions:set = None, current_player:PlayerColor = PlayerColor.BLACK, sticks:int = 0, parent = None):
        self.white_positions = white_positions if white_positions is not None else set({1, 3, 5, 7, 9, 11, 13})
        self.black_positions = black_positions if black_positions is not None else set({2, 4, 6, 8, 10, 12, 14})
        self.current_player = current_player
        self.sticks = sticks
        self.parent = parent
        
    def change_player(self):
        next_player = PlayerColor.BLACK if self.current_player == PlayerColor.WHITE else PlayerColor.WHITE
        self.current_player = next_player
        self.sticks = 0

    def is_terminal(self):
        if not self.black_positions or not self.white_positions:
            return True
        return False
    
    def winner(self):
        if not self.black_positions:
            return "Black Player Win!"
        elif not self.white_positions:
            return "White Player Win!"
