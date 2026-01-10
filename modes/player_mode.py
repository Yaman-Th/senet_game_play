import time
import pygame
from copy import deepcopy
from game_state import State
from game_engine import GameEngine
from game_renderer.renderer import Renderer

class PLayerMode:
    """Class that contain game loop (player vs player)"""
    def __init__(self):
        pygame.init()
        self.renderer = Renderer()
        self.engine = GameEngine()
        self.inital_state = State()
        self.state = deepcopy(self.inital_state)
        self.action = None
        # Loop properties
        self.running = True
        self.clock = pygame.time.Clock()
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
                click_value = self.renderer.handle_events(event.button, self.state.sticks, self.state, self.engine.actions(self.state))
                if click_value == None:
                    return
                elif click_value == -1:
                    sticks = self.engine.TossStick()
                    self.state.sticks = sticks
                    self.engine.handle_special_houses(self.state)
                else:
                    self.action = click_value      
                      
    def restart(self):
        self.state = self.inital_state
        self.state.sticks = 0
        self.action = None

    def undo(self):
        if self.state.parent is not None:
            self.state = self.state.parent
            self.state.sticks = 0
            self.action = None
    
    def update(self):
        new_state = self.engine.transition_model(self.state, self.action)
        if new_state is None:
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
