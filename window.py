import pygame
import sys
import random
from queue import Queue
import time

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
        self.neighbors = []
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
    
    def is_empty(self):
        return self.color == WHITE
    
    def is_visited(self):
        return self.color == CLAY
        
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
    
    def make_visited(self):
        self.color = CLAY
    
    def reset(self):
        self.color = WHITE
        
    def make_path(self):
        self.color = CLAY
        
    def draw(self):
        pygame.draw.rect(SCREEN, self.color, [self.x,self.y, self.width, self.width])
        
    def update_neighbors(self, grid):
        up    = grid[self.row][self.col-1]   if self.col > 0                 else None
        down  = grid[self.row][self.col+1]   if self.col < self.total_rows-1 else None
        left  = grid[self.row-1][self.col]   if self.row > 0                 else None
        right = grid[self.row+1][self.col]   if self.row < self.total_rows-1 else None
        
        four_directions = [up, down, left, right]
        
        for node in four_directions:
            if node and not node.is_barrier():
                self.neighbors.append(node)
                # node.make_open() # for testing

    def __str__(self): 
        return '(row: ' + str(self.row) + ' ,col: ' + str(self.col) + ' ) ' + '(x: ' + str(self.x) + ' ,y: ' + str(self.x) + ' ) '

    def __lt__(self, other): # to avoid error when compared
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
    
def draw(grid, lambda_draw_grid):
    SCREEN.fill(WHITE)
    
    # draw the nodes first before lines to see lines
    for row in grid:
        for node in row:
            node.draw()
    
    # draw lines. All the needed argument already passed before call
    lambda_draw_grid()
    
    pygame.display.update() # Called only once per frame.
    
def get_node(coordinate, grid, rows, width_of_screen):
    x, y = coordinate
    node_width = width_of_screen // rows
    
    x = x//node_width
    y = y//node_width
    
    return grid[x][y]

def draw_path(lambda_draw, came_from, curr_node):
    while curr_node in came_from:
        curr_node = came_from[curr_node]
        curr_node.make_path()
        lambda_draw()

def BFS(lambda_draw, grid, start, end):
    
    queue = Queue()
    
    queue.put(start)

    came_from = {}
    
    curr_node = None
    
    while not queue.empty():
        # maintain the color of start and end nodes
        start.make_start()
        end.make_end()
        
        # exit while solving 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr_node = queue.get()
        
        if curr_node == end:
            draw_path(lambda_draw,came_from, curr_node) # curr_node = end, so either can work
            break
        
        for neighbor in curr_node.neighbors:
            if not neighbor.is_visited():
                neighbor.make_visited()
                queue.put(neighbor)
                lambda_draw()
        time.sleep(.03)

def DFS(lambda_draw, grid, start, end):
    
    stack = [start]
    
    came_from = {}
    
    curr_node = None
    
    while stack:
        # maintain the color of start and end nodes
        start.make_start()
        end.make_end()
        
        # exit while solving 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        curr_node = stack.pop()
        
        if curr_node == end or end in stack:
            draw_path(lambda_draw,came_from, curr_node) # curr_node = end, so either can work
            break
        
        for neighbor in curr_node.neighbors:
            if not neighbor.is_visited():
                neighbor.make_visited()
                stack.append(neighbor)
                lambda_draw()
            elif neighbor in stack:
                stack.pop(stack.index(neighbor))
                
        time.sleep(.03)

def main():
    fps = 60
    fps_clock = pygame.time.Clock()
    
    rows  = 20
    grid = make_grid(rows, WIDTH)
    
    start = None
    end   = None
    
    solving = False
    
    while True:
        
        draw(grid,lambda:draw_grid(rows, WIDTH))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if solving: 
                pass

            if pygame.mouse.get_pressed()[0]: # left click
                node = get_node(event.pos, grid, rows, WIDTH)
                print('LEFT:  ',node)
                if node.is_empty():
                    if not start: 
                        start = node
                        node.make_start()
                    elif not end: 
                        end = node
                        node.make_end()
                    else: 
                        node.make_barrier()

            if pygame.mouse.get_pressed()[2]: # right click
                node = get_node(event.pos, grid, rows, WIDTH)
                print('RIGHT: ',node)
                if node.is_start(): 
                    start = None
                elif node.is_end(): 
                    end = None
                node.reset()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not solving and start and end:
                    print('space!')
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    # BFS(lambda: draw(grid,lambda:draw_grid(rows, WIDTH)), grid, start, end)
                    DFS(lambda: draw(grid,lambda:draw_grid(rows, WIDTH)), grid, start, end)
        pygame.display.update()
    
main()