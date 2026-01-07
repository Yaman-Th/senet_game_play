import pygame
from pygame.math import Vector2

def get_length(cell, margin,repeat):
    return (cell + margin)* repeat

CELL_SIZE = 100
MARGIN = 8

SCREEN_WIDTH = get_length(CELL_SIZE, MARGIN, 14)
SCREEN_HEIGHT = get_length(CELL_SIZE, MARGIN, 6)

BACKGROUND_WIDTH = get_length(CELL_SIZE, MARGIN, 12) + MARGIN
BACKGROUND_HEIGHT = get_length(CELL_SIZE, MARGIN, 3) + MARGIN
BACKGROUND_X = (CELL_SIZE + MARGIN)
BACKGROUND_Y = (CELL_SIZE + MARGIN) * 2

GRID_ORIGIN_X = (CELL_SIZE + MARGIN) + MARGIN
GRID_ORIGIN_Y = (CELL_SIZE + MARGIN) * 2 + MARGIN

INFO_PANEL_X = (CELL_SIZE + MARGIN) * 12 + MARGIN - (CELL_SIZE + MARGIN)
INFO_PANEL_Y = (CELL_SIZE + MARGIN) * 2 + MARGIN
INFO_PANEL_WIDTH = get_length(CELL_SIZE, MARGIN, 2) - MARGIN
INFO_PANEL_HEIGHT = get_length(CELL_SIZE, MARGIN, 2) - MARGIN

POSITIONS = {
    # Position 1 to 10 (row 0)
    0: (2, 10), 1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4), 6: (0, 5), 7: (0, 6), 8: (0, 7), 9: (0, 8), 10: (0, 9),
    # Position 11 to 20 (row 1)
    11: (1, 9), 12: (1, 8), 13: (1, 7), 14: (1, 6), 15: (1, 5), 16: (1, 4), 17: (1, 3), 18: (1, 2), 19: (1, 1), 20: (1, 0),
    # Position 21 to 30 (row 2)
    21: (2, 0), 22: (2, 1), 23: (2, 2), 24: (2, 3), 25: (2, 4), 26: (2, 5), 27: (2, 6), 28: (2, 7), 29: (2, 8), 30: (2, 9),
}

ELEMENTS = {15: (1, 5), 26: (2, 5), 27: (2, 6), 28: (2, 7), 29: (2, 8), 30: (2, 9), 0: (2, 10)}

COLORS = {
    'light':(221, 160, 98),
    'dark':(240, 228, 216),
    'white': (255,252,242),
    'black': (27,18,4),
    'brown':(116,71,0)
}

IMAGES = {
    15 : pygame.image.load("images/start_1.png"),   # start
    26 : pygame.image.load("images/stop.png"),      # stop
    27 : pygame.image.load("images/return.png"),    # return to start
    28 : pygame.image.load("images/three.png"),     # three steps
    29 : pygame.image.load("images/two.png"),       # two steps
    30 : pygame.image.load("images/go.png"),        # any step to go
     0 : pygame.image.load("images/target.png"),    # final goal
}



class inital_board:
    """
    TODO: define static board elements
    """
    def __init__(self):
        self.color1 = {}
        self.color2 = {}
    

class Renderer:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.countdown_font = pygame.font.Font(None, int(CELL_SIZE * 0.7)) 
        self.playerRadius = int(CELL_SIZE / 4)
    
    def get_coordinate(self, r, c):
        x, y = c * (CELL_SIZE + MARGIN) + GRID_ORIGIN_X, r * (CELL_SIZE + MARGIN) + GRID_ORIGIN_Y
        return x, y
    
    def center_coordinate(self, x, y, cell_size):
        return Vector2(x + (cell_size // 2), y + (cell_size // 2))
         
    def render(self, state, start_time):
        self.screen.fill((235,202,148))
        self.draw_grid()
        self.draw_info_panel()
        self.draw_elements()
        self.draw_players(state)
        pygame.display.update()
        
    def draw_grid(self):
        
        # draw background
        bg_rect = pygame.Rect(BACKGROUND_X, BACKGROUND_Y, BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['brown'], bg_rect, border_radius=20)
        
        # draw cells
        for key, value in POSITIONS.items():
            r, c = value[0], value[1]
            x, y = self.get_coordinate(r, c)
            
            if (r + c) % 2 == 0:
                color = COLORS['light']
            else:
                color = COLORS['dark']
                
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=20)

    def draw_info_panel(self):
        rect = pygame.Rect(INFO_PANEL_X, INFO_PANEL_Y, INFO_PANEL_WIDTH, INFO_PANEL_HEIGHT)
        pygame.draw.rect(self.screen, COLORS['dark'], rect, border_radius=20)
    
    def draw_players(self, state):
        
        for pos in state.white_positions :            
            r, c = POSITIONS[pos][0], POSITIONS[pos][1]
            x, y = self.get_coordinate(r, c)
            
            player_center =  self.center_coordinate(x, y, CELL_SIZE)
                       
            pygame.draw.circle(self.screen, COLORS['white'], player_center, self.playerRadius)
        
        for pos in state.black_positions :            
            r, c = POSITIONS[pos][0], POSITIONS[pos][1]
            x, y = self.get_coordinate(r, c)
            
            player_center = self.center_coordinate(x, y, CELL_SIZE)
                        
            pygame.draw.circle(self.screen, COLORS['black'], player_center, self.playerRadius)
    
    def draw_elements(self):
        for key, value in ELEMENTS.items():
            
            r, c = value[0], value[1]
            x, y = self.get_coordinate(r, c)
            w, h = 80, 80
            
            image = pygame.transform.scale(IMAGES[key], (w, h))
            
            image_center = self.center_coordinate(x, y, CELL_SIZE - h)
    
            self.screen.blit(image, image_center)
    