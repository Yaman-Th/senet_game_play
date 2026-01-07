import pygame
from game_state import State
from game_renderer.renderer import Renderer
from copy import deepcopy
from pygame.math import Vector2
import time

class Game:
    """
    Class that contain game loop
    """
    def __init__(self):
        pygame.init()
        self.inital_state = State()
        self.state = deepcopy(self.inital_state)
        
        pygame.display.set_caption("Senet Game")
        
        icon = pygame.image.load("images/logo.png")
        pygame.display.set_icon(icon)
        
        self.renderer = Renderer()
        self.start_time =  time.time()
        self.terminal_mode = False
        
        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True
        
    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.terminal_mode:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_z:
                    self.undo()
                elif event.key == pygame.K_r:
                    self.restart()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    pos = pygame.mouse.get_pos()
                    x, y = pos[0], pos[1]
                    cell = self.renderer.get_cell_from_mouse(x, y)
                    print(f"Pos:{pos}, Cell: {cell}")            
    
    def restart(self):
        pass
    
    def update(self):
        pass
    
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