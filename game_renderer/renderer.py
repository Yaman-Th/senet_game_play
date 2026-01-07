import pygame
from pygame.math import Vector2

from game_state import State

CELL_SIZE = 100
MARGIN = 8

POSITIONS = {
    # Position 1 to 10 (row 0)
    0: (2, 10), 1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4), 6: (0, 5), 7: (0, 6), 8: (0, 7), 9: (0, 8), 10: (0, 9),
    # Position 11 to 20 (row 1)
    11: (1, 9), 12: (1, 8), 13: (1, 7), 14: (1, 6), 15: (1, 5), 16: (1, 4), 17: (1, 3), 18: (1, 2), 19: (1, 1), 20: (1, 0),
    # Position 21 to 30 (row 2)
    21: (2, 0), 22: (2, 1), 23: (2, 2), 24: (2, 3), 25: (2, 4), 26: (2, 5), 27: (2, 6), 28: (2, 7), 29: (2, 8), 30: (2, 9), 31: (2, 11)
}

REVERSE_POSITIONS = {
    (2, 10): 0, (0, 0): 1, (0, 1): 2, (0, 2): 3, (0, 3): 4, (0, 4): 5, (0, 5): 6, (0, 6): 7, (0, 7): 8, (0, 8): 9, (0, 9): 10,
    (1, 9): 11, (1, 8): 12, (1, 7): 13, (1, 6): 14, (1, 5): 15, (1, 4): 16, (1, 3): 17, (1, 2): 18, (1, 1): 19, (1, 0): 20,
    (2, 0): 21, (2, 1): 22, (2, 2): 23, (2, 3): 24, (2, 4): 25, (2, 5): 26, (2, 6): 27, (2, 7): 28, (2, 8): 29, (2, 9): 30, (2, 11): 31
}

ELEMENTS = {15: (1, 5), 26: (2, 5), 27: (2, 6), 28: (2, 7), 29: (2, 8), 30: (2, 9), 0: (2, 10)}
COLORS = {
    'light':(221, 160, 98),
    'dark':(240, 228, 216),
    'white': (255,252,242),
    'black': (27,18,4),
    'brown':(116,71,0),
    'green':(26,178,19)
}
IMAGES = {
    15 : pygame.image.load("images/start_1.png"),   # start
    26 : pygame.image.load("images/stop.png"),      # stop
    27 : pygame.image.load("images/return.png"),    # return to start
    28 : pygame.image.load("images/three.png"),     # three steps
    29 : pygame.image.load("images/two.png"),       # two steps
    30 : pygame.image.load("images/go.png"),        # any step to go
     0 : pygame.image.load("images/target.png"),    # final goal
    "sticks": pygame.image.load("images/stick.png"),    # 4 sticks
}

def get_length(cell, margin,repeat):
        return (cell + margin)* repeat
        
class Renderer:
    screen_w = get_length(CELL_SIZE, MARGIN, 14)
    screen_h = get_length(CELL_SIZE, MARGIN, 6)
    
    grid_x, grid_y = (CELL_SIZE + MARGIN) + MARGIN, (CELL_SIZE + MARGIN) * 2 + MARGIN
    
    def _get_coordinate(self, r, c):
        x, y = c * (CELL_SIZE + MARGIN) + self.grid_x, r * (CELL_SIZE + MARGIN) + self.grid_y
        return x, y
    
    def _get_row_and_col(self, x, y):
        c, r = (x // (CELL_SIZE + MARGIN)) - 1 , (y // (CELL_SIZE + MARGIN)) - 2
        return c, r

    def __init__(self):
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.sticks_font = pygame.font.Font(None, int(CELL_SIZE // 1.5)) 
        self.playerRadius = int(CELL_SIZE / 4)
        self.hover_color = COLORS['white']
    
    def _center_coordinate(self, x, y, cell_w, cell_h):
        return Vector2(x + (cell_w // 2), y + (cell_h // 2))
    
    def render(self, state, start_time):
        self.screen.fill((235,202,148))
        self.draw_grid()
        self.draw_elements()
        self.draw_players(state)
        self.draw_info_panel()
        self.draw_sticks()
        self.draw_sticks_value(state)
        pygame.display.update()
    
    background_w, background_h = get_length(CELL_SIZE, MARGIN, 12) + MARGIN, get_length(CELL_SIZE, MARGIN, 3) + MARGIN
    background_x, background_y = (CELL_SIZE + MARGIN), (CELL_SIZE + MARGIN) * 2
    def draw_grid(self):
        # draw background
        bg_rect = pygame.Rect(self.background_x, self.background_y, self.background_w, self.background_h)
        pygame.draw.rect(self.screen, COLORS['brown'], bg_rect, border_radius=20)
        
        # Change color if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        # current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        
        # draw cells
        for key, value in POSITIONS.items():
            r, c = value[0], value[1]
            x, y = self._get_coordinate(r, c)
            
            if (r + c) % 2 == 0:
                color = COLORS['light']
            else:
                color = COLORS['dark']
                
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect, border_radius=20)
            
            if rect.collidepoint(mouse_pos):
                # Draw only the outline (border)
                # The 3rd argument (LINE_WIDTH) makes it an outline instead of a solid fill
                pygame.draw.rect(self.screen, COLORS['green'], rect, 3, border_radius=20)
                

    info_panel_x, info_panel_y = (CELL_SIZE + MARGIN) * 11 + MARGIN, (CELL_SIZE + MARGIN) * 2 + MARGIN
    info_panel_w, info_panel_h = get_length(CELL_SIZE, MARGIN, 2) - MARGIN, get_length(CELL_SIZE, MARGIN, 2) - MARGIN
    def draw_info_panel(self):
        rect = pygame.Rect(self.info_panel_x, self.info_panel_y, self.info_panel_w, self.info_panel_h)
        pygame.draw.rect(self.screen, COLORS['dark'], rect, border_radius=20)
    
    def draw_players(self, state):
        
        for pos in state.white_positions :            
            r, c = POSITIONS[pos][0], POSITIONS[pos][1]
            x, y = self._get_coordinate(r, c)
            
            player_center =  self._center_coordinate(x, y, CELL_SIZE, CELL_SIZE)
                       
            pygame.draw.circle(self.screen, COLORS['white'], player_center, self.playerRadius)
        
        for pos in state.black_positions :            
            r, c = POSITIONS[pos][0], POSITIONS[pos][1]
            x, y = self._get_coordinate(r, c)
            
            player_center = self._center_coordinate(x, y, CELL_SIZE, CELL_SIZE)
                        
            pygame.draw.circle(self.screen, COLORS['black'], player_center, self.playerRadius)
    
    def draw_elements(self):
        for key, value in ELEMENTS.items():
            r, c = value[0], value[1]
            x, y = self._get_coordinate(r, c)
            w, h = 80, 80
            
            image = pygame.transform.scale(IMAGES[key], (w, h))
            image_center = self._center_coordinate(x, y, CELL_SIZE - w, CELL_SIZE - h)

            self.screen.blit(image, image_center)
    
    sticks_x, sticks_y, = (CELL_SIZE + MARGIN) * 11 + MARGIN, (CELL_SIZE + MARGIN) * 2 + MARGIN
    sticks_w, sticks_h  = get_length(CELL_SIZE, MARGIN, 1.5) , get_length(CELL_SIZE, MARGIN, 1.7)
    def draw_sticks(self):     
           
        image = pygame.transform.scale(IMAGES["sticks"], (self.sticks_w , self.sticks_h))
        image_center = self._center_coordinate(self.sticks_x, self.sticks_y, self.info_panel_w - self.sticks_w, self.info_panel_h - self.sticks_h)
        
        self.screen.blit(image, image_center)
    
    def draw_sticks_value(self, state:State):
        
        text = str(state.sticks)
        text_surface = self.sticks_font.render(text, True, COLORS['brown'])
        
        r, c = POSITIONS[31][0], POSITIONS[31][1]
        x, y = self._get_coordinate(r, c)
        cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        text_rect = text_surface.get_rect(center=cell_rect.center)
        
        self.screen.blit(text_surface, text_rect)
        
        
    def is_clicked(self, event):
        if self.rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # 1 is left click
                return True
        return False
    
    def get_cell_from_mouse(self, x, y):

        col, row = self._get_row_and_col(x, y)
        
        if (row, col) in REVERSE_POSITIONS.keys():
            return REVERSE_POSITIONS[(row, col)]
        else:
            return None