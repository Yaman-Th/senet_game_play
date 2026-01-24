from game_state import PlayerColor
# from algorithms.expectiminimax import ExpectiMinimaxPlayer
from algorithms.algorithm import ExpectiMinimaxPlayer
import random
from game_renderer.renderer import Renderer 
from copy import deepcopy

class algorithmMode:
    """Class that contain game loop (algorithm vs algorithm)"""
    def __init__(self, game):
        self.game = game
        self.renderer = Renderer()
        self.algo_black = ExpectiMinimaxPlayer(2)
        self.algo_white = ExpectiMinimaxPlayer(2)
        self.sticks = 0
        self.turn = None
        self.actions = None
        self.best_action = 0
        
    def processInput(self, events):
        pass
    
    def update(self):
        if self.game.state.current_player == PlayerColor.BLACK:
            self.turn = "Black"
            self._algorithm_turn(self.algo_black)
        elif self.game.state.current_player == PlayerColor.WHITE:
            self.turn = "White"
            self._algorithm_turn(self.algo_white)

    def render(self):
        self.renderer.render(self.game.state,
                             self.actions,
                             self.sticks,
                             self.turn,
                             self.best_action,
                             self.algo_black.stats()[0] if self.turn == "Black" else self.algo_white.stats()[0],
                             self.algo_black.stats()[1] if self.turn == "Black" else self.algo_white.stats()[1])
    
    def _algorithm_turn(self, ai_player):
        sticks = self.game.engine.TossStick()
        self.sticks = sticks
        self.game.state.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        actions = self.game.engine.actions(self.game.state)
        if not actions:
            self.game.state.change_player()
            return
        
        self.actions = actions
        ai_state = deepcopy(self.game.state)
        
        best_action = ai_player.best_action(ai_state)
        self.best_action = best_action
        
        if best_action and best_action is not None:
            self.game.action = best_action
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
                # self.best_action = 0