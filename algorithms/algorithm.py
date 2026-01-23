from math import inf
from game_state import State, PlayerColor
from game_engine import GameEngine
from copy import deepcopy


class ExpectiMinimaxPlayer:
    def __init__(self, depth: int):
        self.depth = depth
        self.action = None
        self.game_engine = GameEngine()
        self.probabilities = {1: 4/16, 2: 6/16, 3: 4/16, 4: 1/16, 5: 1/16}
        
    def eminimax(self, state:State, depth:int, node:str, indent=0, is_root=False) -> float: # type: ignore
        print("  " * indent, node)
        possible_moves = self.game_engine.actions(state)

        if depth == 0 or state.is_terminal():
            return self.evaluate(state)

        if node == "TOSS":
            expected = 0
            for sticks, prob in self.probabilities.items():
                toss_state = deepcopy(state)
                toss_state.sticks = sticks

                next_node = "MAX" if state.current_player == PlayerColor.BLACK else "MIN"

                value = self.eminimax(toss_state, depth - 1, next_node, indent + 1)
                
                expected += prob * value
                
            return expected
        
        # if the node is MAX
        elif node == "MAX":
            
            best_value = -inf
            best_action = None
            for move in possible_moves:
                next_state = self.game_engine.transition_model(state, move)
                
                if next_state is None:
                    continue
                
                value = self.eminimax(next_state, depth, "TOSS", indent + 1)
                
                if value > best_value:
                    best_value = value
                    best_action = move
            
            if is_root:
                return best_action
            
            return best_value
        
        # if the node is MIN
        elif node == "MIN":
            best_value = inf
            best_action = None
            for move in possible_moves:
                next_state = self.game_engine.transition_model(state, move)
                
                if next_state is None:
                    continue
                
                value = self.eminimax(next_state, depth, "TOSS", indent + 1)
                
                if value < best_value:
                    best_value = value
                    best_action = move
            
            if is_root:
                return best_action
            
            return best_value
        
        
    def best_action(self, state:State):
        
        if state.current_player == PlayerColor.BLACK:
            return self.best_action_max(state)
        elif state.current_player == PlayerColor.WHITE:
            return self.best_action_min(state)
        
    def best_action_max(self, state:State):

        action = self.eminimax(state, 2, "MAX", is_root=True)
        return action
    
    def best_action_min(self, state:State):
        action = self.eminimax(state, 2, "MIN", is_root=True)
        return action


    def _get_player_score(self, positions:set) -> float:
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

        if state.winner() == "Black":
            return 10000
        elif state.winner() == "White":
            return -10000
        
        black_score = self._get_player_score(state.black_positions)
        white_score = self._get_player_score(state.white_positions)
        
        return black_score - white_score