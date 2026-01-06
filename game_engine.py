from game_state import PlayerColor, State

class GameEngine:

    def transition_model(self, state:State, action:int):
        """
        return the new state
        """
        white_positions:set = state.white_positions.copy()
        black_positions:set = state.black_positions.copy()
        sticks:int = state.sticks
        current_player = state.current_player

        if current_player == PlayerColor.BLACK and action not in black_positions:
            return None
        elif current_player == PlayerColor.WHITE and action not in black_positions:
            return None

        if current_player == PlayerColor.BLACK:
            new_position = action + state.sticks
            if new_position < 27:
                black_positions.remove(action)
                black_positions.add(new_position)
                if new_position in white_positions:
                    white_positions.remove(new_position)
                    white_positions.add(action)
            elif action > 26:
                black_positions.remove(action)
                if new_position < 31:
                    black_positions.add(new_position)
            else:
                return None
            
        else:
            new_position = action + state.sticks
            if new_position < 27:
                white_positions.remove(action)
                white_positions.add(new_position)
                if new_position in black_positions:
                    black_positions.remove(new_position)
                    black_positions.add(action)
            elif action > 26:
                white_positions.remove(action)
                if new_position < 31:
                    white_positions.add(new_position)
            else:
                return None

        next_player = PlayerColor.BLACK if current_player == PlayerColor.WHITE else PlayerColor.WHITE

        return State(
            white_positions,
            black_positions,
            next_player,
            sticks,
            state
        )

    def actions(self, state):
        """
        TODO: return a set of pawns that player can move
        e.g: set (1, 3, 5, 7, 9, 11, 13) the black pawns
             return set(1, 3) the avaliable moves
        """

black_set = {2, 4, 6, 8, 10, 12, 25}
white_set = {1, 3, 5, 7, 9, 11, 26}
print(f"black_set: {black_set}")
print(f"white_set: {white_set}")
state = State(white_set, black_set, PlayerColor.BLACK, 1)
gameEngine = GameEngine()
new_state = gameEngine.transition_model(state, 25)
if new_state is not None:
    print(f"black_set: {new_state.black_positions}")
    print(f"white_set: {new_state.white_positions}")
    print(f"player turn: {new_state.current_player}")
