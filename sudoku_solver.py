#Sudoku Solver

#Importing and initializing pygame libary
import pygame 
from vertify_validness import *
from board_setup import *
from tkinter import *
from tkinter import messagebox
import os
from PIL import Image

#Initializing game
pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,600])

#image = pygame.image.load("otherother.jpg").convert_alpha()

#Setup font
font = pygame.font.SysFont('Monotype', 18)
num_font = pygame.font.SysFont('Monotype', 20, bold=True)

#Image for background
#screen.blit(image, (0, 0))

#Setting background color
screen.fill((204, 255, 255))

##FLAGS
running = True
started = False
gen_sol = False
info = False
back = False
verify = False
blurred = False

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            ###Checking if start or info button is clicked###
            if mouse[0] >= 215 and mouse[0] <= 335:
                #START BUTTON
                if mouse[1] >= 180 and mouse[1] <= 220 and not started:
                    reset_screen(screen, (255, 255, 255))

                    #Updating flags (game started, info and back not clicked)
                    started = True
                    back = False
                    info = False
                    blurred = False
                    verify=False

                    #Setting up board
                    board_setup(screen)
                    
                    #Generating a incomplete puzzle and filling the board with those values
                    grid = fill_grid()     
                    used_locations = fill_board(None, grid, screen, num_font, (0,0,0))
                    grid_copy = [row[:] for row in grid]

                #INFO BUTTON
                elif mouse[1] >= 250 and mouse[1] <= 290 and not started:
                    #Updating flags (game info selected, start and back not clicked)
                    info = True
                    start = False
                    back = False
                    blurred = False
                    verify=False
            
            ###Started game buttons###
            if mouse[1] >= 550 and mouse[1] <= 590:

                ##NEW GAME BUTTON
                if mouse[0] >=30 and mouse[0]<=130:
                    screen.fill((255, 255, 255))
                    board_setup(screen)

                    grid = fill_grid()     
                    used_locations = fill_board(None, grid, screen, num_font, (0,0,0))
                    grid_copy = [row[:] for row in grid]

                    verify=False
                
                ##GENERATE SOLUTION BUTTON
                elif mouse[0] >=160 and mouse[0]<=260:
                    #Changes made
                    if grid_copy == grid:
                        if verify:
                            #Remove diff
                            reset_screen(screen, (255,255,255))
                            board_setup(screen)
                            verify = False
                            blurred=False
                        solved_puzzle = solve_puzzle(grid_copy)
                        fill_board(solved_puzzle, grid, screen, num_font, (255,0,0))
                    else:
                        #Remove diff 
                        reset_screen(screen, (255,255,255))
                        board_setup(screen)

                        verify=False
                        blurred=False
 
                        #Reset
                        grid_copy = [row[:] for row in grid]
                        solved_puzzle = solve_puzzle(grid_copy)
                        fill_board(solved_puzzle, grid, screen, num_font, (255,0,0))

                ##VERIFY SOLUTION BUTTON
                elif mouse[0] >=290 and mouse[0]<=390:
                    verify = True
                    if 0 not in grid and gen_sol:
                        screen.fill((255, 255, 255))
                        board_setup(screen)
                        fill_board(None, grid, screen, num_font, (0,0,0))  

                #BACK BUTTON
                elif mouse[0] >=420 and mouse[0]<=520 and not info and started:
                    back = True
                    started = False 
                    blurred = False
                    verify=False
            
            #BACK BUTTON IN INFO SCREEN (info selected and back selected)
            if mouse[0]>=420 and mouse[0]<=520 and mouse[1]>=550 and mouse[1]<=580 and info:
                back = True
                info = False    
                started = False
                blurred = False
                verify=False
        
            if not (mouse[1] >= 550 and mouse[1] <= 590) and verify:
                reset_screen(screen, (255,255,255))
                image = pygame.image.load("current_grid.jpeg").convert_alpha()
                screen.blit(image, (0, 0))
                verify = False
                blurred = False

        #ENTERING NUMS FOR VERIFY
        if event.type == pygame.KEYDOWN:
            input_num = event.unicode

            #Indices
            if input_num.isnumeric() and int(input_num) >= 1 and int(input_num) <= 9 and not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations):
                highlight_cell(screen, mouse, grid)
                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(mouse[0]), get_range(mouse[1]), 0, 60))
                screen.blit(num_font.render(input_num , True , (255,0,0)) , (25+get_range(mouse[0]), (25+get_range(mouse[1]))))
                grid_copy[int(get_range(mouse[1])/60)][int(get_range(mouse[0])/60)] = int(input_num)

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

    if verify:
        valid_sol = verify_validness(grid_copy)
        
        if not blurred:
            blur_image(screen)
            blurred = True

        message_button(screen)

        if valid_sol:
            screen.blit(pygame.font.SysFont('Monotype', 25).render("You Win!" , True , (0,0,0)) , (220, 170))
        else:
            screen.blit(pygame.font.SysFont('Monotype', 25).render("Try Again!" , True , (0,0,0)) , (200, 170))
        
    #Display
    pygame.display.flip()

#Removing screenshot as its not needed anymore
if os.path.exists("current_grid.jpeg"): 
    os.remove("current_grid.jpeg")
    os.remove("BlurImage.jpg")

#Close game
pygame.quit()


