import time
import pygame
from copy import deepcopy
from enum import Enum, auto
from game_state import State
from game_engine import GameEngine
from modes.player_mode import PLayerMode
from modes.algo_mode import algorithmMode
from game_renderer.renderer import Renderer
from modes.algo_player_mode import algorithmPlayerMode
from modes.algo_random_mode import algorithmAndRandMode

class Mode(Enum):
    PLAYER_MODE = auto()
    ALGORITHM_AND_PLAYER_MODE = auto()
    ALGORITHM_MODE = auto()
    ALGORITHM_AND_RANDOM_MODE = auto()

class Game:
    """
    this class guide you to game mode
    and contain the Game Loop
    e.g: Game -> PLayer_mode
              -> algo_player_mode
              -> algorithm_mode
    """
    def __init__(self, mode:Mode):
        pygame.init()
        self.mode = self._create_mode_instance(mode)
        # self.renderer = Renderer()
        self.engine = GameEngine()
        self.initial_state = State()
        self.state = deepcopy(self.initial_state)
        self.action = None
        self.clock = pygame.time.Clock()
        self.running = True
        self.start_time = time.time()

    def _create_mode_instance(self, mode:Mode):
        if mode == Mode.PLAYER_MODE:
            return PLayerMode(self)
        elif mode == Mode.ALGORITHM_AND_PLAYER_MODE:
            return algorithmPlayerMode(self)
        elif mode == Mode.ALGORITHM_MODE:
            return algorithmMode(self)
        elif mode == Mode.ALGORITHM_AND_RANDOM_MODE:
            return algorithmAndRandMode(self)
        else:
            raise ValueError(f"Unknown game mode: {mode}")

    def processInput(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_z:
                    self.undo()
                elif event.key == pygame.K_r:
                    self.restart()
        
        self.mode.processInput(events)

    def update(self):
        self.mode.update()

    def render(self):
        self.mode.render()

    def restart(self):
        self.state = deepcopy(self.initial_state)
        self.state.sticks = 0
        self.action = None

    def undo(self):
        if self.state.parent is not None:
            self.state = self.state.parent
            self.state.sticks = 0
            self.action = None

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
