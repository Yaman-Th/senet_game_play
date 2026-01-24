import pygame
from game_state import PlayerColor
# from algorithms.expectiminimax import ExpectiMinimaxPlayer
from algorithms.algorithm import ExpectiMinimaxPlayer
from game_renderer.renderer import Renderer
class algorithmPlayerMode:
    """Class that contain game loop (algorithm vs player)"""
    def __init__(self, game):
        self.game = game
        self.algo = ExpectiMinimaxPlayer(2)
        self.renderer = Renderer()
        self.sticks = 0
        self.turn = None
        self.actions = None
        self.best_action = 0
        
    def processInput(self, events):
        if self.game.state.current_player == PlayerColor.WHITE:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_value = self.renderer.handle_events(
                        event.button,
                        self.game.state.sticks,
                        self.game.state,
                        self.game.engine.actions(self.game.state)
                    )
                    if click_value is None:
                        continue
                    elif click_value == -1:
                        sticks = self.game.engine.TossStick()
                        self.sticks = sticks
                        self.game.state.sticks = sticks
                        self.game.engine.handle_special_houses(self.game.state)
                    else:
                        self.game.action = click_value 
    
    def update(self):
        if self.game.state.current_player == PlayerColor.BLACK:
            self.turn = "Black"
            self._algorithm_turn()
        elif self.game.state.current_player == PlayerColor.WHITE:
            self.turn = "White"
            self._player_turn()

    def render(self):
        self.renderer.render(self.game.state, self.game.engine.actions(self.game.state), self.sticks, self.turn, self.best_action, self.algo.stats())
        
    def _algorithm_turn(self):
        sticks = self.game.engine.TossStick()
        self.sticks = sticks
        self.game.state.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        actions = self.game.engine.actions(self.game.state)
        
        if not actions:
            self.game.state.change_player()
            return
        
        # self.actions = actions
        
        best_action = self.algo.best_action(self.game.state)
        self.best_action = best_action
        
        if best_action and best_action is not None:
            self.game.action = best_action
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
                self.actions = None

    def _player_turn(self):
        new_state = self.game.engine.transition_model(self.game.state, self.game.action)
        if new_state is not None:            
            self.game.state = new_state
            self.game.action = None
            self.actions = None
