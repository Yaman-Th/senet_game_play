import time
import pygame
from copy import deepcopy
from game_engine import GameEngine
from game_state import PlayerColor, State
from game_renderer.renderer import Renderer
from algorithms.expectiminimax import ExpectiMinimaxPlayer

class algorithmPlayerMode:
    """Class that contain game loop (algorithm vs player)"""
    def __init__(self):
        pygame.init()
        self.algo = ExpectiMinimaxPlayer(PlayerColor.BLACK)
        self.renderer = Renderer()
        self.engine = GameEngine()
        self.inital_state = State()
        self.state = deepcopy(self.inital_state)
        self.action = None
        self.waiting_for_sticks = False
        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True
        self.start_time =  time.time()
        
    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_z:
                    self.undo()
                elif event.key == pygame.K_r:
                    self.restart()

            if self.state.current_player == PlayerColor.WHITE:
                if event.type == pygame.MOUSEBUTTONDOWN:
                        click_value = self.renderer.handle_events(event.button, self.state.sticks, self.state, self.engine.actions(self.state))
                        if click_value == None:
                            return
                        elif click_value == -1:
                            sticks = self.engine.TossStick()
                            self.state.sticks = sticks
                            self.engine.handle_special_houses(self.state)
                        else:
                            self.action = click_value 
            else:
                pass
                      
    def restart(self):
        self.state = self.inital_state
        self.state.sticks = 0
        self.action = None
        self.waiting_for_sticks = False

    def undo(self):
        if self.state.parent is not None:
            self.state = self.state.parent
            self.state.sticks = 0
            self.action = None
            self.waiting_for_sticks = False
    
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
