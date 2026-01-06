class State:
    """
    white positions (frozenset),
    black positions (frozenset),
    player turn (bool): if it is True the black turn else white turn,
    sticks (int 1 -> 5),
    parent (state)
    """

    def __init__(self, white_positions:set = None, black_positions:set = None, turn:bool = True, sticks:int = 0, parent = None):
        self.white_positions = white_positions if white_positions is not None else frozenset(1, 3, 5, 7, 9, 11, 13)
        self.black_positions = black_positions if black_positions is not None else frozenset(2, 4, 6, 8, 10, 12, 14)
        self.black_turn = turn
        self.sticks = sticks
        self.parent = parent
