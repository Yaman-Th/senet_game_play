from game_state import PlayerColor, State
import random

class GameEngine:
    def transition_model(self, state:State, action:int):
        """
        Transition to a new state by moving a pawn
        """
        if action is None or state.sticks == 0:
            return None
        if not self._is_valid_action(state, action):
            return None
        white_positions:set = state.white_positions.copy()
        black_positions:set = state.black_positions.copy()
        sticks:int = state.sticks
        current_player = state.current_player
        # handle special houses
        if current_player == PlayerColor.BLACK:
            self._handle_special_houses(black_positions, white_positions, sticks, action)
        else:
            self._handle_special_houses(white_positions, black_positions, sticks, action)
        # handle pawn move
        if current_player == PlayerColor.BLACK:
            success = self._move_pawn(action, black_positions, white_positions, sticks)
        else:
            success = self._move_pawn(action, white_positions, black_positions, sticks)
        if not success:
            return None
        # switch players
        next_player = PlayerColor.BLACK if current_player == PlayerColor.WHITE else PlayerColor.WHITE
        return State(
            white_positions,
            black_positions,
            next_player,
            0,
            state
        )
    
    def _is_valid_action(self, state:State, action:int) -> bool:
        """
        Check is action is valid for the current player
        To prevent collision between pawns from the same color
        """
        if state.current_player == PlayerColor.BLACK:
            return action in state.black_positions
        else:
            return action in state.white_positions
        
    def _handle_special_houses(self, current_player_positions, opponent_positions, sticks, action):
        """Handling 28, 29, 30 Houses"""
        occupied_positions = current_player_positions | opponent_positions
        for pawn in current_player_positions:
            if (pawn == 28 and (sticks != 3 or action != 28)) or \
                (pawn == 29 and (sticks != 2 or action != 29)) or \
                (pawn == 30 and action != 30):
                new_position = self._first_previous(15, occupied_positions)
                current_player_positions.remove(pawn)
                current_player_positions.add(new_position)
    
    def _move_pawn(self, action, current_player_positions, opponent_positions, sticks):
        """Move pawn and handle switching"""
        new_position = action + sticks
        path = range(action + 1, sticks + action + 1)
        if 26 in path and action + sticks > 26:
            return False
        if new_position == 27 :
            current_player_positions.remove(action)
            new_pos = self._first_previous(15,current_player_positions|opponent_positions)
            current_player_positions.add(new_pos)
            return True
        if new_position < 27:
            current_player_positions.remove(action)
            current_player_positions.add(new_position)
            if new_position in opponent_positions:
                opponent_positions.remove(new_position)
                opponent_positions.add(action)
        elif action >= 26:
            current_player_positions.remove(action)
            if new_position < 31:
                current_player_positions.add(new_position)
        else:
            return False
        return True
    
    def _first_previous(self, action, positions):
        """This function returns the first empty cell less than 16"""
        for position in range(action, 0, -1):
            if position not in positions:
                return position
        return None 

    def actions(self, state:State):
        """
        This function return a set of pawns that player can move
        e.g: set (1, 3, 5, 7, 9, 11, 13) the pawns and sticks = 2
             return set(13) the avaliable moves
        """
        current_positions = set()
        movable_positions = set()
        if state.current_player == PlayerColor.BLACK:
            current_positions = state.black_positions
        else:
            current_positions = state.white_positions
        for current_position in current_positions:
            new_position = current_position + state.sticks
            if new_position in current_positions:
                continue
            elif new_position < 27:
                movable_positions.add(current_position)
            elif current_position == 26:
                movable_positions.add(current_position)
            elif current_position == 28 and state.sticks == 3:
                movable_positions.add(current_position)
            elif current_position == 29 and state.sticks == 2:
                movable_positions.add(current_position)
            elif current_position == 30:
                movable_positions.add(current_position)
        return movable_positions

    def TossStick(self):
        """This function return int (1 -> 5) probability of sticks"""
        sticks = [0, 1, 2, 3, 4]
        probs = [1/16, 4/16, 6/16, 4/16, 2/16]
        choice = random.choices(sticks,probs)[0]
        return 5 if choice == 0 else choice
