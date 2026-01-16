from math import inf
from game_state import State, PlayerColor
from game_engine import GameEngine
from copy import deepcopy

class ExpectiMinimaxPlayer:
    def __init__(self, depth: int):
        # self.player_color = player_color
        self.depth = depth
        self.action = None
        self.game_engine = GameEngine()
        self.probabilities = {1: 4/16, 2: 6/16, 3: 4/16, 4: 1/16, 5: 1/16}
        # self.visited_states=0
        
    def eminimax(self, state:State, depth:int, node:str) -> float: # type: ignore
        # self.visited_states=0
        # best_move = -1
        possible_moves = self.game_engine.actions(state)

        if depth == 0 or self._is_terminal(state):
            print("EVALUTING")
            print("===============")
            return self.evaluate(state)

        # if the node is MAX
        if node == "MAX":
            print(f"MAXIMIZING, DEPTH = {depth}")
            print("===============")

            value = -inf
            for move in possible_moves:
                next_state = self.game_engine.transition_model(state, move)
                if next_state is None:
                    continue
                value = max(value, self.eminimax(next_state, depth - 1, "TOSS"))
            return value
        
        # if the node is MIN
        if node == "MIN":
            print(f"MINIMIZING, DEPTH = {depth}")
            print("===============")
            value = inf
            for move in possible_moves:
                next_state = self.game_engine.transition_model(state, move)
                if next_state is None:
                    continue
                # print(depth)
                value = min(value, self.eminimax(next_state, depth - 1, "TOSS"))
            return value
        
        # if the node is CHANCE(TOSS)
        if node == "TOSS":
            print(f"TOSSING, DEPTH = {depth}")
            print("===============")
            expected = 0

            for sticks, prob in self.probabilities.items():
                toss_state = deepcopy(state)
                toss_state.sticks = sticks
                toss_state.current_player = PlayerColor.BLACK if state.current_player == PlayerColor.WHITE else PlayerColor.WHITE

                next_node = "MIN" if state.current_player == PlayerColor.BLACK else "MAX"

                print(depth)
                value = self.eminimax(toss_state, depth - 1, next_node)
                expected += prob * value
            return expected

    def best_action(self, state:State):

        if state.current_player == PlayerColor.BLACK:
            b_value = -inf
            b_action = None
        
            for action in self.game_engine.actions(state):
                next_state = self.game_engine.transition_model(state, action)
                if next_state is None:
                    continue
                value = self.eminimax(next_state, self.depth, "TOSS")

                if value > b_value:
                    b_value = value
                    b_action = action

            return b_action

        # else:
        #     b_value = inf
        #     b_action = None
        
        #     for action in self.game_engine.actions(state):
        #         next_state = self.game_engine.transition_model(state, action)
        #         if next_state is None:
        #             continue
        #         value = self.eminimax(next_state, self.depth, "TOSS")

        #         if value > b_value:
        #             b_value = value
        #             b_action = action

            # return b_action


    def _is_terminal(self, state: State) -> bool:
        return not state.white_positions or not state.black_positions

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
        if not state.black_positions:
            return inf if state.current_player == PlayerColor.BLACK else -inf
        if not state.white_positions:
            return inf if state.current_player== PlayerColor.WHITE else -inf
        
        black_score = self._get_player_score(state.black_positions)
        white_score = self._get_player_score(state.white_positions)
        
        if state.current_player == PlayerColor.BLACK:
            return black_score - white_score
        else:
            return white_score - black_score