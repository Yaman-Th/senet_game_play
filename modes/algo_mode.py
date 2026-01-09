import time
import pygame
from copy import deepcopy
from game_engine import GameEngine
from game_state import PlayerColor, State
from game_renderer.renderer import Renderer
from algorithms.expectiminimax import ExpectiMinimaxPlayer

class algorithmMode:
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
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # player turn (listen to mouse click)
                if self.state.current_player == PlayerColor.WHITE:
                    click_value = self.renderer.handle_events(
                        event.button,
                        self.state.sticks,
                        self.state,
                        self.engine.actions(self.state)
                    )
                    if click_value is None:
                        continue
                    elif click_value == -1:
                        if not self.waiting_for_sticks:
                            sticks = self.engine.TossStick()
                            self.state.sticks = sticks
                            self.engine.handle_special_houses(self.state)
                            self.waiting_for_sticks = True
                            valid_actions = self.engine.actions(self.state)
                            if not valid_actions:
                                self.state.current_player = PlayerColor.BLACK
                                self.state.sticks = 0
                                self.waiting_for_sticks = False
                            else:
                                self.waiting_for_sticks = True
                    else:
                        if self.waiting_for_sticks and self.state.sticks:
                            self.action = click_value
                            self.waiting_for_sticks = False
                # AI turn (ignore mouse click)
                else:
                    pass
                      
    def restart(self):
        self.state = self.inital_state
        self.waiting_for_sticks = False
    
    def update(self):
        # AI turn (Black)
        if self.state.current_player == PlayerColor.BLACK:
            sticks = self.engine.TossStick()
            self.state.sticks = sticks
            self.engine.handle_special_houses(self.state)
            best_action = self.algo.find_best_move(self.state)
            self.action = best_action[0]
            new_state = self.engine.transition_model(self.state, self.action)
            if new_state is None:
                return
            self.state = new_state
            self.action = None
        # Player Turn (White)
        elif self.state.current_player == PlayerColor.WHITE:
            if self.action is not None:
                new_state = self.engine.transition_model(self.state, self.action)
                if new_state is None:
                    self.action = None
                    return
                self.state = new_state
                self.action = None
                 
    def render(self):
        self.renderer.render(self.state, self.start_time, self.engine.actions(self.state))
    
    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)
        
        self.elapsed_time = time.time() - self.start_time
        print(f"Time: {self.elapsed_time:.2f}s")
        pygame.quit()
        exit()
