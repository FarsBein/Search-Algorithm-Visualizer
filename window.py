import pygame
import sys
import random


pygame.init() # initialize all imported pygame modules. No exceptions will be raised if a module fails

WIDTH = 800; HEIGHT = 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Search Algorithm Visualizer")

# colors
BLUE = (0, 150, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 87, 51)

row = col = 20
row_width = WIDTH // row # for one box
col_height= HEIGHT// col # for one box

def draw_grid(filled):
    
    x = y = 0    
    
    for i in range(row):
        x += row_width
        pygame.draw.line(SCREEN,WHITE, (x, 0), (x, HEIGHT))

    for i in range(col):
        y += col_height
        pygame.draw.line(SCREEN,WHITE, (0, y), (WIDTH, y))
    
    for a,b in filled:      
        pygame.draw.rect(SCREEN, RED, [a,b, row_width+1, col_height+1])
    
        
def main():
    
    fps = 60
    fps_clock = pygame.time.Clock()
    
    clicked_pos = []
    while True:
        SCREEN.fill(BLACK)
        
        
        state = pygame.mouse.get_pressed()

        # if state != (0,0,0): print('state:', state)
        
        draw_grid(clicked_pos)
        
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