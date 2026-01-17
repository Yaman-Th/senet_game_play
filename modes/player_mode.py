import pygame

class PLayerMode:
    """Class that contain game loop (player vs player)"""
    def __init__(self, game):
        self.game = game
        
    def processInput(self, events):
        for event in events:      
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_value = self.game.renderer.handle_events(
                    event.button,
                    self.game.state.sticks,
                    self.game.state,
                    self.game.engine.actions(self.game.state)
                )
                if click_value == None:
                    return
                elif click_value == -1:
                    sticks = self.game.engine.TossStick()
                    self.game.state.sticks = sticks
                    self.game.engine.handle_special_houses(self.game.state)
                else:
                    self.game.action = click_value      
    
    def update(self):
        if self.game.action is not None:
            new_state = self.game.engine.transition_model(self.game.state, self.game.action)
            if new_state is not None:
                self.game.state = new_state
                self.game.action = None
