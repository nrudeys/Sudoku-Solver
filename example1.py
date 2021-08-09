from board_setup import *
import pygame 
import sys

#Setting clock
fps=4
fpsclock=pygame.time.Clock()

#Initializing game
pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,600])

#Filling empty board
screen.fill((255,255,255))
board_setup(screen)
grid = fill_grid()     

#Setting flags
running = True
pos = False

#Setting positions for grid
x = 300
y = 300

input_num = 0

#Font types
num_font = pygame.font.SysFont('Monotype', 20, bold=True)

#Fill board
filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))

#Empty dict to keep track of squares and their nums
arr = [(y*60,x*60) for x in range(0,9) for y in range(0,9)]
entries = dict.fromkeys(arr, 0)
entries = {k: entries[k] if k not in filled_spots else True for k in entries}

#Setting initial pos to -1 so we know that arrows haven't moved yet so we need to add highlight
#entries[(300,300)] = -1

while running:
    for event in pygame.event.get():
        
        ##QUIT##
        if event.type == pygame.QUIT:
            running = False

        ##ENTERING NUM##
        if event.type == pygame.KEYDOWN:
            input_num = event.unicode
        
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
    
    #Checking which keys are being pressed (used for holding feature)
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_LEFT]:
        #Erase previous empty square
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
        #Advance in given dir
        x = set_x(x, -60)
        #Highlight new pos
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

    if keys_pressed[pygame.K_RIGHT]:
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
        x = set_x(x, 60)
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

    if keys_pressed[pygame.K_UP]:
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
        y = set_y(y, x, -60, screen, entries)
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

    if keys_pressed[pygame.K_DOWN]:
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
        y = set_y(y, x, 60, screen, entries)
        if entries[(x,y)] == 0:
            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
    
    
    if pos and entries[get_range(pos[0]), get_range(pos[1])] != True:
        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))

        if entries[(x,y)] == 0 and not ((get_range(pos[0]), get_range(pos[1])) == (x,y)):
            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))

        x = get_range(pos[0])
        y = get_range(pos[1])
                
        if entries[(x,y)] != 0:
            screen.blit(num_font.render(entries[(x,y)] , True , (255,0,0)), (25+x, 25+y))
    
    #Enter input
    if str(input_num).isnumeric() and int(input_num) >= 1 and int(input_num) <= 9 and entries[(x,y)] != True:
            curr_pos = pygame.mouse.get_pos()

            #Spot is used (need to re-highlight)
    
            if (entries[(x,y)] != 0) or ((get_range(curr_pos[0]), get_range(curr_pos[1])) == (x,y)):
                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
            
            #Update entry for pos and display
            entries[(x,y)] = input_num
            screen.blit(num_font.render(input_num , True , (255,0,0)), (25+x, 25+y))
            
            #Reset
            input_num = 0
    pos = False
    
    #Display
    pygame.display.flip()
    fpsclock.tick(fps) 
pygame.quit()