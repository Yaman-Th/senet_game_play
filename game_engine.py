from game_state import PlayerColor, State
import random
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
        
       #28 , 29 ,30 handling
        handled_action=set()
        if current_player==PlayerColor.BLACK:
            updated_position=set()
            for pawn in black_positions:
                 if pawn==28 and sticks!=3:
                    new_pos=self.first_previous(15,updated_position|white_positions)
                    updated_position.add(new_pos)
                    handled_action.add(pawn)
                 elif pawn==29 and sticks!=2:
                    new_pos=self.first_previous(15,updated_position|white_positions)
                    updated_position.add(new_pos)
                    handled_action.add(pawn)
                 elif pawn==30:
                     handled_action.add(pawn)
                     continue
                 else :
                  updated_position.add(pawn)
            black_positions=updated_position
        else:
             updated_position=set()
             for pawn in white_positions:
                 if pawn==28 and sticks!=3:
                    new_pos=self.first_previous(15,updated_position|black_positions)
                    updated_position.add(new_pos)
                    handled_action.add(pawn)
                 elif pawn ==29 and sticks!=2:
                    new_pos=self.first_previous(15,updated_position|black_positions)
                    updated_position.add(new_pos)
                    handled_action.add(pawn)
                 elif pawn==30:
                     handled_action.add(pawn)
                     continue
                 else :
                  updated_position.add(pawn)
             white_positions=updated_position
    


            
        if action in handled_action:
            success=True
        else:
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
        path= range(action+1,sticks+action+1)
        if 26 in path and action+sticks>26:
            return False
        
        if new_position ==27 :
            current_player_positions.remove(action)
            new_pos=self.first_previous(15,current_player_positions|opponent_positions)
            current_player_positions.add(new_pos)
            return True
        
        
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
    def TossStick(self):
        sticks=[0,1,2,3,4]
        probs=[1/16,4/16,6/16,4/16,2/16]
        choice=random.choices(sticks,probs)[0]
        return 5 if choice ==0 else choice 
    
    def first_previous(self,action,positions):
        for position in range(action,0,-1):
            if position not in positions:
                return position
        return None    
    
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

#test()
def test_transition_model():
    engine = GameEngine()
    sticks = engine.TossStick()
    print(f"Tossed sticks: {sticks}")
    state1 = State(
        white_positions={2,4,30},
        black_positions={1, 15, 6},
        current_player=PlayerColor.WHITE,
        sticks=2
    )
    new_state1 = engine.transition_model(state1, 2)
    if new_state1 is None:
        print("Move was invalid (None returned)\n")
    else:
        print(f"White: {new_state1.white_positions}, Black: {new_state1.black_positions}\n")


   

test_transition_model()
