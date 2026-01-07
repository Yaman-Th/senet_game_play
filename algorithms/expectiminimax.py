import math
from game_state import State, PlayerColor
from game_engine import GameEngine

class ExpectiMinimaxPleyer:
    def __init__(self, player_color: PlayerColor, max_depth: int = 3):
        self.player_color = player_color
        self.max_depth = max_depth
        self.game_engine = GameEngine()
        self.probabilities = {1: 4/16, 2: 6/16, 3: 4/16, 4: 1/16, 5: 1/16}
        
    def find_best_move(self, state: State) -> int:
        pass

    def _is_game_over(self, state: State) -> bool:
        return not state.white_positions or not state.black_positions

    def _get_player_score(self, positions: frozenset) -> float:
        score = 0.0
        House_of_Happiness = 26
        House_of_Water = 27
        Trapped_Squares = {28, 29} # square you can get stuck in
        Total_Pawns = 7

        for pawn_pos in positions:
            if pawn_pos == House_of_Water:
                score -= 50

            elif pawn_pos == House_of_Happiness:
                score += 20

            elif pawn_pos in Trapped_Squares:
                score -= 25    
            else:
                score += pawn_pos

        pawns_off_board = Total_Pawns - len(positions)
        score += pawns_off_board *100

        return score
    
    def evaluate(self, state: State) -> float:
        if self._is_game_over(state):
            if not state.black_positions:
                return math.inf   # Black wins
            else:
                return -math.inf  # white wins

        black_score = self._get_player_score(state.black_positions)
        white_score = self._get_player_score(state.white_positions)

        return black_score - white_score
    
    def expected_value(self,state :State, depth :int) ->float:
        total_expected_value = 0.0

        for sticks_roll, probability in self.probabilities.items():
            roll_state = State(
                white_positions = state.white_positions,
                black_positions = state.black_positions,
                current_player = state.current_player,
                sticks = sticks_roll,
                parent = state.parent

            )

            total_expected_value += self.get_value(roll_state, depth)* probability

        return total_expected_value

    def get_value(self, state: State, depth: int) -> float:
        pass