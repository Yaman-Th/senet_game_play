from game_state import PlayerColor
# from algorithms.expectiminimax import ExpectiMinimaxPlayer
from algorithms.algorithm import ExpectiMinimaxPlayer
import random
from copy import deepcopy

class algorithmMode:
    """Class that contain game loop (algorithm vs algorithm)"""
    def __init__(self, game):
        self.game = game
        self.algo_black = ExpectiMinimaxPlayer(4)
        # self.algo_white = ExpectiMinimaxPlayer(PlayerColor.WHITE)
        
    def processInput(self, events):
        pass
    
    def update(self):
        if self.game.state.current_player == PlayerColor.BLACK:
            self._algorithm_turn(self.algo_black)
        elif self.game.state.current_player == PlayerColor.WHITE:
            # self._algorithm_turn(self.algo_white)
            self._random_agent_turn()

    def _algorithm_turn(self, ai_player):
        sticks = self.game.engine.TossStick()
        self.game.state.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        if not self.game.engine.actions(self.game.state):
            self.game.state.change_player()
            return
        
        ai_state = deepcopy(self.game.state)
        best_action = ai_player.best_action(ai_state)
        
        if best_action and best_action is not None:
            self.game.action = best_action
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
    
    def _random_agent_turn(self):
        sticks = self.game.engine.TossStick()
        self.game.state.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        actions = self.game.engine.actions(self.game.state)
        if not actions:
            self.game.state.change_player()
            return
        
        # best_action = ai_player.find_best_move(self.game.state)
        action = random.choice(list(actions))
        
        if action and action is not None:
            self.game.action = action
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
