import os
import random
import pygame
from copy import deepcopy
from game_state import PlayerColor
from game_renderer.renderer import Renderer
from algorithms.algorithm import ExpectiMinimaxPlayer

class algorithmAndRandMode:
    """Class that contain game loop (algorithm vs algorithm)"""
    def __init__(self, game):
        self.game = game
        self.renderer = Renderer()
        self.algo_black = ExpectiMinimaxPlayer(2)
        self.sticks = None
        self.actions = None
        self.action = None
        self.turn = None
        audio_path = os.path.join("audio", "move.wav")
        self.jump_sfx = pygame.mixer.Sound(str(audio_path))
        self.jump_sfx.set_volume(1)
        
    def processInput(self, events):
        pass
    
    def update(self):
        if self.game.state.current_player == PlayerColor.BLACK:
            self.turn = "Black"
            self._algorithm_turn(self.algo_black)
        elif self.game.state.current_player == PlayerColor.WHITE:
            self.turn = "White"
            self._random_agent_turn()

    def _algorithm_turn(self, ai_player):
        sticks = self.game.engine.TossStick()
        self.game.state.sticks = sticks
        self.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        actions = self.game.engine.actions(self.game.state)
        
        if not actions:
            self.game.state.change_player()
            return
        
        self.actions = actions
        
        ai_state = deepcopy(self.game.state)
        best_action = ai_player.best_action(ai_state)
        self.action = best_action
        self.jump_sfx.play()
        
        if best_action and best_action is not None:
            self.game.action = best_action
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
    
    def _random_agent_turn(self):
        sticks = self.game.engine.TossStick()
        self.sticks = sticks
        self.game.state.sticks = sticks
        self.game.engine.handle_special_houses(self.game.state)

        actions = self.game.engine.actions(self.game.state)
        if not actions:
            self.game.state.change_player()
            return
        self.actions = actions
        action = random.choice(list(actions))
        self.jump_sfx.play()
        self.action = action
        
        if action and action is not None:
            self.game.action = action
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
    
    def render(self):
        self.renderer.render(self.game.state,
                             self.actions,
                             self.sticks,
                             self.turn,
                             self.action,
                              self.algo_black.stats()[0], self.algo_black.stats()[1])
