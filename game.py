import pygame
from enum import Enum, auto
from game_state import State
from game_renderer.renderer import Renderer
from game_engine import GameEngine
from copy import deepcopy

from pygame.math import Vector2
import time

class Mode(Enum):
    PLAYER_MODE = auto()
    ALGORITHM_AND_PLAYER_MODE = auto()
    ALGORITHM_MODE = auto()

class Game:
    """
    Class that contain game loop
    """
    def __init__(self, mode:Mode):
        pygame.init()
        self.inital_state = State()
        self.renderer = Renderer()
        self.engine = GameEngine()
        
        self.state = deepcopy(self.inital_state)
        self.action = None
    
        self.start_time =  time.time()
        
        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True
        
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
                click_value = self.renderer.handle_events(event.button, self.state.sticks)
                if click_value == None:
                    continue
                
                elif click_value == 0:
                    sticks = self.engine.TossStick()
                    self.state.sticks = sticks
                
                else:
                    self.action = click_value
                
                      
    def restart(self):
        self.state = self.inital_state
    
    def update(self):
        new_state = self.engine.transition_model(self.state, self.action)
        if new_state is None:
            return
        
        self.state = new_state
        
                 
    def render(self):
        self.renderer.render(self.state, self.start_time)
    
    def run(self):
        while self.running:
            
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)
        
        self.elapsed_time = time.time() - self.start_time
        # print(f"Moves: {self.moveCount}")
        print(f"Time: {self.elapsed_time:.2f}s")
        pygame.quit()
        exit()