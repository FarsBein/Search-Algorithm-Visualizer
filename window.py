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
        pygame.draw.rect(SCREEN, self.color, [self.x,self.y, self.width, self.width])
        
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

    def __str__(self): 
        return '(row: ' + str(self.row) + ' ,col: ' + str(self.col) + ' ) ' + '(x: ' + str(self.x) + ' ,y: ' + str(self.x) + ' ) '

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
            
def draw_grid(rows, width_of_screen):
    x = y = 0    
    node_width = width_of_screen // rows
    
    for i in range(rows):
        pygame.draw.line(SCREEN,BLACK, (0, i*node_width), (width_of_screen, i*node_width)) # start then end. (start/end, distance from the top)
    
    for j in range(rows):
        pygame.draw.line(SCREEN,BLACK, (j*node_width, 0), (j*node_width, width_of_screen)) # start then end. (distance from the left, start/end)
    

def draw(grid, rows, width_of_screen):
    SCREEN.fill(WHITE)
    
    # draw the nodes first before lines to see lines
    for row in grid:
        for node in row:
            node.draw()
    
    # draw lines
    draw_grid(rows, WIDTH)
    
    pygame.display.update() # Called only once per frame.
    

def get_node(coordinate, grid, rows, width_of_screen):
    x, y = coordinate
    node_width = width_of_screen // rows
    
    x = x//node_width
    y = y//node_width
    
    return grid[x][y]
   
def main():
    
    fps = 60
    fps_clock = pygame.time.Clock()
    
    rows  = 20
    grid = make_grid(rows, WIDTH)
    
    start = False
    end = False
    
    while True:
        # state = pygame.mouse.get_pressed()
        # if state != (0,0,0): print('state:', state)
        
        draw(grid, rows, WIDTH)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]: # left click
                node = get_node(event.pos, grid, rows, WIDTH)
                print('LEFT: ',node)
                if not start: 
                    start = True
                    node.make_start()
                elif not end: 
                    end = True
                    node.make_end()
                else: 
                    node.make_barrier()

            if pygame.mouse.get_pressed()[2]: # right click
                node = get_node(event.pos, grid, rows, WIDTH)
                print('RIGHT: ',node)
                if node.is_start(): 
                    start = False
                elif node.is_end(): 
                    end = False
                node.reset()
                    
                    
        pygame.display.update()
    
main()