import pygame
from game_state import PlayerColor
from algorithms.expectiminimax import ExpectiMinimaxPlayer

class algorithmPlayerMode:
    """Class that contain game loop (algorithm vs player)"""
    def __init__(self, game):
        self.game = game
        self.algo = ExpectiMinimaxPlayer(PlayerColor.BLACK)
        
    def processInput(self, events):
        if self.game.state.current_player == PlayerColor.WHITE:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_value = self.game.renderer.handle_events(
                        event.button,
                        self.game.state.sticks,
                        self.game.state,
                        self.game.engine.actions(self.game.state)
                    )
                    if click_value is None:
                        continue
                    elif click_value == -1:
                        sticks = self.game.engine.TossStick()
                        self.game.state.sticks = sticks
                        self.game.engine.handle_special_houses(self.game.state)
                    else:
                        self.game.action = click_value 
    
    def update(self):
        if self.game.state.current_player == PlayerColor.BLACK:
            self._algorithm_turn()
        elif self.game.state.current_player == PlayerColor.WHITE:
            self._player_turn()

    def _algorithm_turn(self):
        sticks = self.game.engine.TossStick()
        self.game.state.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        if not self.game.engine.actions(self.game.state):
            self.game.state.change_player()
            return
        
        best_action = self.algo.find_best_move(self.game.state)
        
        if best_action and best_action[0] is not None:
            self.game.action = best_action[0]
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None

    def _player_turn(self):
        new_state = self.game.engine.transition_model(self.game.state, self.game.action)
        if new_state is not None:            
            self.game.state = new_state
            self.game.action = None
