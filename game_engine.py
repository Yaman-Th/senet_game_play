from game_state import PlayerColor, State

class GameEngine:

    def transition_model(self, state:State, action:int):
        white_positions:set = state.white_positions.copy()
        black_positions:set = state.black_positions.copy()
        sticks:int = state.sticks
        current_player = state.current_player

        if current_player == PlayerColor.BLACK and action not in black_positions:
            return None
        elif current_player == PlayerColor.WHITE and action not in white_positions:
            return None
        
        # TODO: handle each home what should do

        if current_player == PlayerColor.BLACK:
            success = self._move_pawn(action, black_positions, white_positions, state.sticks)
        else:
            success = self._move_pawn(action, white_positions, black_positions, state.sticks)

        if not success:
            print("none")
            return None
        
        next_player = PlayerColor.BLACK if current_player == PlayerColor.WHITE else PlayerColor.WHITE

        return State(
            white_positions,
            black_positions,
            next_player,
            sticks,
            state
        )
    
    def _move_pawn(self, action, current_player_positions, opponent_positions, sticks):
        new_position = action + sticks

        if new_position < 27:
            current_player_positions.remove(action)
            current_player_positions.add(new_position)
            if new_position in opponent_positions:
                opponent_positions.remove(new_position)
                opponent_positions.add(action)
        elif action > 26:
            current_player_positions.remove(action)
            if new_position < 31:
                current_player_positions.add(new_position)
        else:
            return False
        
        return True

    def actions(self, state):
        """
        TODO: return a set of pawns that player can move
        e.g: set (1, 3, 5, 7, 9, 11, 13) the black pawns
             return set(1, 3) the avaliable moves
        """

def test():
    black_set = {2, 4, 6, 8, 10, 12, 25}
    white_set = {1, 3, 5, 7, 9, 11, 26}
    print(f"black_set: {black_set}")
    print(f"white_set: {white_set}")
    state = State(white_set, black_set, PlayerColor.WHITE, 1)
    gameEngine = GameEngine()
    new_state = gameEngine.transition_model(state, 11)
    if new_state is not None:
        print(f"black_set: {new_state.black_positions}")
        print(f"white_set: {new_state.white_positions}")
        print(f"player turn: {new_state.current_player}")

test()
