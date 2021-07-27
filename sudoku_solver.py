#Sudoku Solver

#Importing and initializing pygame libary
import pygame 
from vertify_validness import *
from board_setup import *

pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,600])

#image = pygame.image.load("otherother.jpg").convert_alpha()

#Setup font
font = pygame.font.SysFont('Monotype', 18)
num_font = pygame.font.SysFont('Monotype', 20, bold=True)
#screen.blit(image, (0, 0))

screen.fill((204, 255, 255))

#Run until user indiciates otherwise
running = True
started = False
gen_sol = False
info = False
back = False

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            ###Checking if start or info button is clicked###
            if mouse[0] >= 215 and mouse[0] <= 335:

                #START BUTTON
                if mouse[1] >= 180 and mouse[1] <= 220:
                    reset_screen(screen, (255, 255, 255))

                    #Updating flags (game started, info and back not clicked)
                    started = True
                    back = False
                    info = False

                    #Setting up board
                    board_setup(screen)
                    
                    #Generating a incomplete puzzle and filling the board with those values
                    grid = fill_grid()     
                    fill_board(None, grid, screen, num_font, (0,0,0))

                #INFO BUTTON
                elif mouse[1] >= 250 and mouse[1] <= 290:
                    #Updating flags (game info selected, start and back not clicked)
                    info = True
                    start = False
                    back = False
            
            ###Started game buttons###
            if mouse[1] >= 550 and mouse[1] <= 590:

                ##NEW GAME BUTTON
                if mouse[0] >=30 and mouse[0]<=130:
                    screen.fill((255, 255, 255))
                    board_setup(screen)

                    grid = fill_grid()     
                    fill_board(None, grid, screen, num_font, (0,0,0))
                
                ##GENERATE SOLUTION BUTTON
                elif mouse[0] >=160 and mouse[0]<=260:
                    grid_copy = [row[:] for row in grid]
                    solved_puzzle = solve_puzzle(grid_copy)
                    fill_board(solved_puzzle, grid, screen, num_font, (255,0,0))
                
                ##VERIFY SOLUTION BUTTON
                elif mouse[0] >=290 and mouse[0]<=390:
                    if 0 not in grid:
                        screen.fill((255, 255, 255))
                        board_setup(screen)
                        fill_board(None, grid, screen, num_font, (0,0,0))  
                
                #BACK BUTTON
                elif mouse[0] >=420 and mouse[0]<=520 and not info and started:
                    back = True
                    started = False  
            
            #BACK BUTTON IN INFO SCREEN (info selected and back selected)
            if mouse[0]>=420 and mouse[0]<=520 and mouse[1]>=550 and mouse[1]<=580 and info:
                back = True
                info = False    
                started = False
                    
    #Getting mouse position
    mouse = pygame.mouse.get_pos()

    #Highlight mouse hover for all buttons
    if not started:
        startup(screen, mouse, font)
    else:
        game_started_setup(screen, mouse)

    #Load info screen
    if info:
        reset_screen(screen, (204, 255, 255))
        if mouse[0]>=420 and mouse[0]<=520 and mouse[1]>=550 and mouse[1]<=580:
            back_button_hover(screen)
        else:
            back_button(screen)
        screen.blit(pygame.font.SysFont('Monotype', 15).render('Back' , True , (0,0,0)) , (450, 555))
        for i,line in enumerate(get_instructions()):
            screen.blit(pygame.font.SysFont('Monotype', 15).render(line , True , (0,0,0)) , (30, 30+(i*25)))
    
    if back:
        startup(screen, mouse, font)
        
    #Display
    pygame.display.flip()

#Close game
pygame.quit()
