from math import inf
from game_state import State, PlayerColor
from game_engine import GameEngine
from copy import deepcopy

class ExpectiMinimaxPlayer:
    def __init__(self, player_color: PlayerColor, depth: int = 5):
        self.player_color = player_color
        self.depth = depth
        self.game_engine = GameEngine()
        self.probabilities = {1: 4/16, 2: 6/16, 3: 4/16, 4: 1/16, 5: 1/16}
        self.visited_states=0
        
    def minimax(self, state:State, depth) -> float:
        self.visited_states=0
        possible_moves = self.game_engine.actions(state)
        best_move = -1

        if self.depth == 0 or self._is_terminal:
            return self.evaluate(state)

        # if the node is MAX
        if state.current_player == PlayerColor.BLACK:
            value = -inf  
            for move in possible_moves:
                expected = 0
                for sticks_roll, probability in self.probabilities.items():
                    roll_state = State(
                        white_positions = deepcopy(state.white_positions),
                        black_positions = deepcopy(state.black_positions),
                        current_player = state.current_player,
                        sticks = sticks_roll,
                        parent = state.parent)
                    expected += probability * self.minimax(roll_state, self.depth - 1)
                return expected
                next_state = self.game_engine.transition_model(state, move)

                # if next_state is None:
                #     continue

                value = max(value, self.minimax(next_state, self.depth - 1))

            return value
        
        # if the node is MIN
        elif state.current_player == PlayerColor.WHITE:
            value = inf
            for move in possible_moves:

                next_state = self.game_engine.transition_model(state, move)

                if next_state is None:
                    continue
                
                value = min(value, self.minimax(next_state, self.depth - 1))
            return value
        


    def _is_terminal(self, state: State) -> bool:
        return not state.white_positions or not state.black_positions

    def _get_player_score(self, positions: frozenset) -> float:
        score = 0.0
        House_of_Happiness = 26
        House_of_Water = 27
        House_of_Three = 28 # square you can get stuck in
        House_of_Atom = 29 # square you can get stuck in
        Total_Pawns = 7

        for pawn_pos in positions:
            if pawn_pos == House_of_Water:
                score -= 50

            elif pawn_pos == House_of_Happiness:
                score += 40
            elif pawn_pos == House_of_Three:
                score -= 25
            elif pawn_pos == House_of_Atom:
                score -= 30
            else:
                score += pawn_pos

        pawns_off_board = Total_Pawns - len(positions)
        score += pawns_off_board * 100

        return score
    
    def evaluate(self, state: State) -> float:
        if self._is_terminal(state):
            if not state.black_positions:
                return inf if self.player_color == PlayerColor.BLACK else -inf
            if not state.white_positions:
                return inf if self.player_color == PlayerColor.WHITE else -inf
        black_score = self._get_player_score(state.black_positions)
        white_score = self._get_player_score(state.white_positions)
        if self.player_color == PlayerColor.BLACK:
            return black_score - white_score
        else:
            return white_score - black_score
    
    # def expected_value(self,state :State, depth :int) ->int:
    #     total_expected_value = 0.0

    #     for sticks_roll, probability in self.probabilities.items():
    #         roll_state = State( 
    #             white_positions = deepcopy(state.white_positions),
    #             black_positions = deepcopy(state.black_positions),
    #             current_player = state.current_player,
    #             sticks = sticks_roll,
    #             parent = state.parent)

    #         total_expected_value += self.get_value(roll_state, depth) * probability

    #     return total_expected_value

    # def get_value(self, state: State, depth: int) -> float:
    #     self.visited_states+=1
    #     if depth == 0 or self._is_game_over(state):
    #         return self.evaluate(state)
        
    #     possible_moves = self.game_engine.actions(state)
        
    #     if not possible_moves:
    #         next_Player = PlayerColor.WHITE if state.current_player == PlayerColor.BLACK else PlayerColor.BLACK
    #         skipped_state = State(state.white_positions, state.black_positions, next_Player, 0, state)
    #         return self.expected_value(skipped_state, depth-1)
        
    #     # max player's turn
    #     if state.current_player == self.player_color:
    #         max_value = -math.inf
    #         for move in possible_moves:
    #             next_state = self.game_engine.transition_model(state, move)
    #             if next_state is None:
    #                 continue
    #             value = self.expected_value(next_state, depth-1)
    #             max_value = max(max_value,value)

    #         return max_value

    #     #min player's turn
    #     else:
    #         min_value = math.inf
    #         for move in possible_moves:
    #             next_state = self.game_engine.transition_model(state, move)
    #             if next_state is None:
    #                 continue
    #             value = self.expected_value(next_state, depth-1)
    #             min_value = min(min_value, value)

    #         return min_value
     
    # def analysis_inf(self,state:State):
    #     self.visited_states=0
    #     best_move,score =self.find_best_move(state)
    #     if best_move==-1:
    #         return None
    #     next_state=self.game_engine.transition_model(state,best_move)
    #     moved_set = (
    #     next_state.black_positions - state.black_positions
    #      if self.player_color == PlayerColor.BLACK
    #      else next_state.white_positions - state.white_positions
    #      )
    #     destenation=moved_set.pop() if moved_set else None
    #     return{
    #         "pawn":best_move,
    #         "score":score,
    #         "visited":self.visited_states,
    #         "whereToGo":destenation
    #     }