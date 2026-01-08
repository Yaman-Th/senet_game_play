import pygame
from game_state import State
from os.path import join

class Data:
    def __init__(self, cell, margin):
        self.cell = cell
        self.margin = margin
        self.module = cell + margin
        self.grid_c, self.grid_r = 1, 2
        self.grid_x, self.grid_y = self.get_coordinate(self.grid_r, self.grid_c)
        self.elements = {15: (1, 5), 26: (2, 5), 27: (2, 6), 28: (2, 7), 29: (2, 8), 30: (2, 9), 0: (2, 10)}
        self.colors = {
            'light': (221, 160, 98),
            'dark' : (240, 228, 216),
            'white': (255,252,242),
            'black': (27,18,4),
            'brown': (116,71,0),
            'green': (26,178,19)
        }
        self.positions = {
            0: (2, 10), 1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0, 4), 6: (0, 5), 7: (0, 6), 8: (0, 7), 9: (0, 8), 10: (0, 9),
            11: (1, 9), 12: (1, 8), 13: (1, 7), 14: (1, 6), 15: (1, 5), 16: (1, 4), 17: (1, 3), 18: (1, 2), 19: (1, 1), 20: (1, 0),
            21: (2, 0), 22: (2, 1), 23: (2, 2), 24: (2, 3), 25: (2, 4), 26: (2, 5), 27: (2, 6), 28: (2, 7), 29: (2, 8), 30: (2, 9), 31: (2, 11)
            }
        self.r_posistions = {
            (2, 10): 0, (0, 0): 1, (0, 1): 2, (0, 2): 3, (0, 3): 4, (0, 4): 5, (0, 5): 6, (0, 6): 7, (0, 7): 8, (0, 8): 9, (0, 9): 10,
            (1, 9): 11, (1, 8): 12, (1, 7): 13, (1, 6): 14, (1, 5): 15, (1, 4): 16, (1, 3): 17, (1, 2): 18, (1, 1): 19, (1, 0): 20,
            (2, 0): 21, (2, 1): 22, (2, 2): 23, (2, 3): 24, (2, 4): 25, (2, 5): 26, (2, 6): 27, (2, 7): 28, (2, 8): 29, (2, 9): 30, (2, 11): 31
        }
        
    def get_length(self, repeat):
        """
        to convert from squares to screen pixels
        :param repeat: number of squares
        """
        return self.module * repeat
    
    def get_length_cell(self, repeat):
        """
        to convert from squares to screen pixels
        :param repeat: number of squares
        """
        return self.cell * repeat
    
    def get_coordinate(self, r, c):
        """
        convert the index (row, col) to coordinates (x, y)
        :param r: row number
        :param c: col number
        """
        x, y = c * self.module , r * self.module
        return (x, y)
    
    def get_row_and_col(self, x, y):
        """
        convert coordinates (x, y) to index (row, col)
        :param x: x value
        :param y: y value
        """
        c, r = (x // self.module) - self.grid_c, (y // self.module) - self.grid_r
        return (c, r)
    
    def get_center(self, x, y, cell_w, cell_h):
        return (x + (cell_w // 2), y + (cell_h // 2))
    
    def move(self, coords:tuple):
        return coords[0] + self.grid_x, coords[1] + self.grid_y
    
    def set_image_size(self, f):
        return (self.cell * f, self.cell * f)
    
class Renderer:
    def __init__(self):
        # all static data
        self.data = Data(90, 9)
        
        # screen data
        self.screen_w = self.data.get_length(14)
        self.screen_h = self.data.get_length(6)
        self.screen = self.init_screen(self.screen_w, self.screen_h)
        
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.sticks_font = pygame.font.Font(None, int(self.data.cell // 1.5)) 
        self.playerRadius = int(self.data.cell // 4)
        self.IMAGES = {
            15      : pygame.image.load(join('images', 'start_1.png')).convert_alpha(),   # start
            26      : pygame.image.load(join('images', 'stop.png'   )).convert_alpha(),   # stop
            27      : pygame.image.load(join('images', 'return.png' )).convert_alpha(),   # return to start
            28      : pygame.image.load(join('images', 'three.png'  )).convert_alpha(),   # three steps
            29      : pygame.image.load(join('images', 'two.png'    )).convert_alpha(),   # two steps
            30      : pygame.image.load(join('images', 'go.png'     )).convert_alpha(),   # any step to go
             0      : pygame.image.load(join('images', 'target.png' )).convert_alpha(),   # final goal
            "sticks": pygame.image.load(join('images', 'stick.png'  )).convert_alpha(),   # 4 sticks 
            }
    
    def render(self, state, start_time):
        """
        rendering all screen elements
        
        :param state: state that rendered
        :param start_time: using to rendering elapsed time
        """
        self.screen.fill(self.data.colors['brown'])
        self.draw_grid()
        self.draw_elements()
        self.draw_players(state)
        self.draw_sticks()
        self.draw_sticks_value(state)
        pygame.display.update()
    
    def init_screen(self, w, h):
        """
        initilize the screen 
        
        :param w: screen width
        :param h: screen height
        """
        screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Senet Game")
        
        icon = pygame.image.load(join('images', 'logo.png')).convert_alpha()
        pygame.display.set_icon(icon)
        
        return screen
    
    def draw_grid(self):
        
        # Change color if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
                
        # draw cells
        for key, value in self.data.positions.items():
            r, c = value[0], value[1]
            x, y = self.data.get_coordinate(r, c)
            
            if (r + c) % 2 == 0:
                color = self.data.colors['light']
            else:
                color = self.data.colors['dark']
                
            rect = pygame.Rect(x, y, self.data.cell, self.data.cell).move(self.data.grid_x, self.data.grid_y)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=20)
            
            if rect.collidepoint(mouse_pos):
                # Draw only the outline (border)
                # The 3rd argument (LINE_WIDTH) makes it an outline instead of a solid fill
                pygame.draw.rect(self.screen, self.data.colors['green'], rect, 3, border_radius=20)
                
    def draw_players(self, state):
        
        for pos in state.white_positions :            
            r, c = self.data.positions[pos][0], self.data.positions[pos][1]
            x, y = self.data.move(self.data.get_coordinate(r, c))
            
            player_center =  self.data.get_center(x, y, self.data.cell, self.data.cell)
                       
            pygame.draw.circle(self.screen, self.data.colors['white'], player_center, self.playerRadius)
        
        for pos in state.black_positions :            
            r, c = self.data.positions[pos][0], self.data.positions[pos][1]
            x, y = self.data.move(self.data.get_coordinate(r, c))
            
            player_center = self.data.get_center(x, y, self.data.cell, self.data.cell)
                        
            pygame.draw.circle(self.screen, self.data.colors['black'], player_center, self.playerRadius)
    
    def draw_elements(self):
        for key, value in self.data.elements.items():
            r, c = value[0], value[1]
            x, y = self.data.move(self.data.get_coordinate(r, c))
            w, h = self.data.set_image_size(0.8)
            
            image = pygame.transform.scale(self.IMAGES[key], (w, h))
            image_center = self.data.get_center(x, y, self.data.cell - w, self.data.cell - h)

            self.screen.blit(image, image_center)
    
    def draw_sticks(self):
        
        info_panel_x, info_panel_y = self.data.get_coordinate(0, 10)
        info_panel_w, info_panel_h = self.data.get_length(1.93), self.data.get_length(1.93)
        
        rect = pygame.Rect(info_panel_x, info_panel_y, info_panel_w, info_panel_h).move(self.data.grid_x, self.data.grid_y)
        pygame.draw.rect(self.screen, self.data.colors['dark'], rect, border_radius=20)
        
        sticks_x, sticks_y, = self.data.move(self.data.get_coordinate(0, 10))
        sticks_w, sticks_h  = self.data.get_length(1.5) , self.data.get_length(1.7)
           
        image = pygame.transform.scale(self.IMAGES["sticks"], (sticks_w , sticks_h))
        image_center = self.data.get_center(sticks_x, sticks_y, info_panel_w - sticks_w, info_panel_h - sticks_h)
        
        self.screen.blit(image, image_center)
    
    def draw_sticks_value(self, state:State):
        text = str(state.sticks)
        text_surface = self.sticks_font.render(text, True, self.data.colors['brown'])
        
        r, c = self.data.positions[31][0], self.data.positions[31][1]
        x, y = self.data.move(self.data.get_coordinate(r, c))
        
        cell_rect = pygame.Rect(x, y, self.data.cell, self.data.cell)
        text_rect = text_surface.get_rect(center=cell_rect.center)
        
        self.screen.blit(text_surface, text_rect)
    
    def get_cell_from_mouse(self, x, y):
        col, row = self.data.get_row_and_col(x, y)
        
        if (row, col) in self.data.r_posistions.keys():
            return self.data.r_posistions[(row, col)]
        else:
            return None
    
    def handle_events(self, event, sticks):
        if event == 1:
            pos = pygame.mouse.get_pos()
            x, y = pos[0], pos[1]
            cell = self.get_cell_from_mouse(x, y)
            
            if cell == 31 and sticks == 0:
                return 0
            else:
                print(f"Pos:{pos}, Cell: {cell}")
                return cell

        
    
    
