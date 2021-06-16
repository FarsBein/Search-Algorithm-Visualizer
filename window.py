import pygame
import sys
import random

# sys.path.append(".")
# from node_class import Node


pygame.init() # initialize all imported pygame modules. No exceptions will be raised if a module fails

WIDTH = 800; HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Algorithm Visualizer")

# colors
BLUE = (0, 150, 255)
PINK = (255,13,255)
GREEN = (81, 225, 13)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 87, 51)
CLAY = (63,176,172)

row = col = 20
row_width = WIDTH // row # for one box

col_height= HEIGHT// col # for one box

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = width * row
        self.y = width * col
        self.neighbor = []
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        
    def get_pos(self):
        return (self.row,self.col)
    
    def get_color(self):
        self.color = self.color
    
    def get_coord(self):
        return (self.x,self.y)
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN 
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == BLUE
    
    def is_end(self):
        return self.color == PINK
    
    def make_start(self):
        self.color = BLUE
    
    def make_end(self):
        self.color = PINK

    def make_barrier(self):
        self.color = BLACK  
        
    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED
    
    def reset(self):
        self.color = WHITE
        
    def make_path(self):
        self.color = CLAY
        
    def draw(self):
        pygame.draw.rect(SCREEN, RED, [self.x,self.y, self.width, self.width])
        
    def update_neighbor(self, grid):
        up       = grid[self.row][self.col-1]   if self.col > 0 else None
        down     = grid[self.row][self.col+1]   if self.col < total_rows else None
        left     = grid[self.row-1][self.col]   if self.row > 0 else None
        right    = grid[self.row+1][self.col]   if self.row < total_rows else None
        up_right = grid[self.row+1][self.col-1] if self.col > 0 and self.col < total_rows else None
        up_left  = grid[self.row-1][self.col-1] if self.col > 0 and self.col > 0 else None
        down_right=grid[self.row+1][self.col+1] if self.col < total_rows and self.col < total_rows else None
        down_left =grid[self.row-1][self.col+1] if self.col < total_rows and self.col > 0 else None
        list_of_all_directions = [up, down, left, right, up_right, up_left, down_right, down_left]

        for i in list_of_all_directions:
            if i:
                self.neighbor.append(i) 
                
        def __it__(self, other): # to avoid error when compared
            return False
            
def distance(p1,p2): # L shaped way of calculating distance
    x1, y1 = p1
    x2, y2 = p2
    
    return abs(x2-x1) + abs(y2-y1)

def make_grid(rows, width_of_screen):
    grid = []
    node_width = width_of_screen // rows
    
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i,j,node_width,rows)
            grid[i].append(node)
    
    return grid
            
def draw_grid(filled, rows, width_of_screen):
    
    x = y = 0    
    node_width = width_of_screen // rows
    
    for i in range(row):
        pygame.draw.line(SCREEN,WHITE, (0, i*node_width), (width_of_screen, i*node_width)) # start then end. (start, distance from the top)

    for i in range(col):
        pygame.draw.line(SCREEN,WHITE, (i*node_width, 0), (i*node_width, width_of_screen)) 
    
    for a,b in filled:      
        pygame.draw.rect(SCREEN, RED, [a,b, row_width+1, col_height+1])
    
        
def main():
    
    fps = 60
    fps_clock = pygame.time.Clock()
    
    clicked_pos = []
    
    rows  = 20
    
    while True:
        SCREEN.fill(BLACK)
        
        
        state = pygame.mouse.get_pressed()

        # if state != (0,0,0): print('state:', state)
        
        draw_grid(clicked_pos, rows, WIDTH)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                    print('LEFT event.pos:', event.pos)
                    
                    x,y = event.pos
                    x = int((x/row)*(row_width))
                    y = int(y/col)*(col_height)
                    print('rounded:', (x,y))
                    
                if event.button == 3: # right click
                    print('RIGHT event.pos:', event.pos)
                    
                    x,y = event.pos
                    x = int((x/row)*(row_width))
                    y = int(y/col)*(col_height)
                    print('rounded:', (x,y))
                    
        pygame.display.update()
    
main()