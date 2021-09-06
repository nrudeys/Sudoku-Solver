# Sudoku Solver 
# By: Shahnur Syed

# Importing libraries
import numpy as np
import os
import pygame as py
import random
import sys
import game_helpers as gh
import game_modes as modes
import game_setup
import gen_dataset as gen_data 
import solve_dataset as solve_data

#Setting clock
fps = 4.5
fpsclock = py.time.Clock()

#Initializing game
py.init()

#Setting up drawing window
screen = py.display.set_mode([540,600])

#Setup font types to use
text_font = py.font.SysFont('Monotype', 18)
num_font = py.font.SysFont('Monotype', 20, bold=True)
display_font = py.font.SysFont('Monotype', 25)

#Flags
running = True
game_started = info = generate_sol = blurred = back = back_enter = pos = \
               easy = medium = hard = default = mode_diff = \
               enter_board = False

entries_ent = dict.fromkeys([k for k in gh.get_cell_indices()], 0)

invalid_spots = invalid_spots_ent = {}
sol_ent = []

#colors
RED = (255, 0, 0)
VIOLET = (255, 204, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
YELLOW = (255, 255, 204)

game_setup.home_screen(screen, py.mouse.get_pos(), text_font)

assist = None
input_num = 0

# Setting positions for grid
x = y = x1 = y1 = 300

while running:
    for event in py.event.get():
        
        if event.type == py.QUIT:
            # Exiting game
            running = False

        if event.type == py.MOUSEBUTTONUP:
            pos = curr_pos = py.mouse.get_pos()
           
            if curr_pos[0] >= 215 and curr_pos[0] <= 335 and not game_started:
                if (curr_pos[1] >= 130 and curr_pos[1] <= 170 and 
                    not enter_board):
                    # Starting game
                    if back or back_enter:
                        if (str(default).isnumeric() and 
                            default == mode_diff):
                            # Load previous Sudoku puzzle 
                            img = py.image.load("curr_grid.png")
                            screen.blit(img, (0, 0))
                        else:
                            # A mode was selected
                            if easy:
                                grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
                            elif medium:
                                grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
                            elif hard:
                                grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)

                            if easy or medium or hard:
                                game_setup.create_empty_board(screen)

                                used_spots = game_setup.insert_values(screen, grid)
                                
                                sol = solve_data.solve_puzzle(np.copy(grid))
                                sol_entries, entries = (
                                    gh.set_ents_dicts(sol, used_spots)
                                )

                                x = y = 300
                            else:
                                # Default mode, check if assist mode switched
                                img = py.image.load("curr_grid.png")
                                screen.blit(img, (0, 0))
    
                                for k in invalid_spots_ent.keys():
                                    val = str(invalid_spots_ent[k])
                                    rect = py.Rect(k[0] + 3, k[1] + 3, 56, 56)

                                    if assist:
                                        py.draw.rect(screen, YELLOW, rect)
                                    else:
                                        py.draw.rect(screen, VIOLET, rect)

                                    num = num_font.render(val, True, RED)
                                    
                                    screen.blit(num, (25 + k[0], 25 + k[1]))
                                
                            game_started = True
                            info = blurred = back = back_enter = pos = enter_board = False                    
                            input_num = 0   
                    else:
                        if easy:
                            grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
                        elif medium:
                            grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
                        elif hard: 
                            grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)
                        else:
                            choices = modes.Mode.get_choices(modes.Mode)
                            default = random.choice(choices)

                            if default == modes.Mode.EASY:
                                grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
                            elif default == modes.Mode.MEDIUM:
                                grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
                            else:
                                grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)

                        game_setup.create_empty_board(screen)

                        used_spots = game_setup.insert_values(screen, grid)   

                        sol = solve_data.solve_puzzle(np.copy(grid))
                        sol_entries, entries = (
                                    gh.set_ents_dicts(sol, used_spots)
                                )
                        invalid_spots = {}

                        x = y = 300
                    
                    game_started = True
                    info = blurred = back = back_enter = pos = \
                           enter_board = False   

                    input_num = 0
                elif (curr_pos[1] >= 200 and curr_pos[1] <= 240 and 
                      not enter_board):
                    # Info button clicked 
                    info = True
                    game_started = back = back_enter = False
                elif (curr_pos[1] >= 270 and curr_pos[1] <= 310 and 
                      not enter_board):
                    # Enter button clicked
                    if not all(x == 0 or x == True for x in 
                               entries_ent.values()):
                        # Enter board previously visited
                        img = py.image.load("curr_grid_enter.png")
                        screen.blit(img, (0, 0))

                        for k in invalid_spots_ent.keys():
                            val = str(invalid_spots_ent[k])
                            rect = py.Rect(k[0] + 3, k[1] + 3, 56, 56)

                            if assist:
                                py.draw.rect(screen, YELLOW, rect)
                            else:
                                py.draw.rect(screen, VIOLET, rect)

                            screen.blit(num_font.render(val, True, RED), 
                                        (25 + k[0], 25 + k[1]))
                    else:
                        indices = [k for k in gh.get_cell_indices()]
                        entries_ent = dict.fromkeys(indices, 0)
                        
                        game_setup.create_empty_board(screen)
                        
                        invalid_spots_ent = {}
                    
                    enter_board = True
                    info = back = back_enter = False     
            elif (curr_pos[0] >= 420 and curr_pos[0] <= 520 and 
                curr_pos[1] >= 550 and curr_pos[1] <= 580 and info):
                # Back button in info screen clicked
                info = False
                back = True
            elif curr_pos[1] >= 550 and curr_pos[1] <= 590 and game_started:
                # Game started
                if curr_pos[0] >= 30 and curr_pos[0] <= 130:
                    # New game button clicked
                    
                    game_setup.create_empty_board(screen)
        
                    if easy or (str(default).isnumeric() and 
                       default == modes.Mode.EASY):
                        grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
                    elif medium or default == modes.Mode.MEDIUM:
                        grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
                    elif hard or default == modes.Mode.HARD: 
                        grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)
 
                    sol = solve_data.solve_puzzle(np.copy(grid))
                    used_spots = game_setup.insert_values(screen, grid)
                    sol_entries, entries = gh.set_ents_dicts(sol, used_spots)

                    generate_sol = blurred = False
                    invalid_spots = {}

                    x = y = 300
                    input_num = 0
                elif curr_pos[0] >= 160 and curr_pos[0] <= 260:   
                    # Generate solution button clicked

                    game_setup.create_empty_board(screen)
                    game_setup.insert_values(screen, grid, sol)
                    entries = {k: sol_entries[k] for k in entries}

                    generate_sol = True
                elif curr_pos[0] >= 290 and curr_pos[0] <= 390:
                    # Verify button clicked

                    grid_vals = gh.get_curr_grid_vals(entries, used_spots,
                                    sol)

                    if gen_data.verify_validness(grid_vals):
                        valid_sol = True
                    else:
                        valid_sol = False

                    if not blurred:
                        py.image.save(screen, "curr_grid.png")
                        game_setup.blur_background(screen, "curr_grid.png")
                        blurred = True

                    game_setup.display_message(screen)

                    if valid_sol:
                        screen.blit(display_font.render("You Win!", True,
                                    BLACK), (220, 170))
                    else:
                        screen.blit(display_font.render("Try Again!", True,
                                    BLACK), (200, 170))
                elif (curr_pos[0] >= 420 and curr_pos[0] <= 520 
                      and game_started):
                    # Back button in game screen clicked
                    
                    py.image.save(screen, "curr_grid.png")
                    
                    back = True
                    game_started = blurred  = False

                    # Saving previous difficulty mode
                    if easy:
                        mode_diff = modes.Mode.EASY
                    elif medium:
                        mode_diff = modes.Mode.MEDIUM
                    elif hard:
                        mode_diff = modes.Mode.HARD
                    else:
                        mode_diff = default
                    
                    easy = medium = hard = False
            elif curr_pos[1] >= 550 and curr_pos[1] <= 590 and enter_board: 
                # Solved button clicked
                if curr_pos[0] >= 220 and curr_pos[0] <= 320:
                    grid_vals = game_setup.get_curr_grid_vals(entries_ent, 
                                    used_spots, sol)
                    
                    sol_ent = []
                    error_occur = False

                    try:
                        sol_ent = solve_data.solve_puzzle(np.copy(grid_vals))
                    except:
                        error_occur = True
                        
                    if sol_ent != []:
                        game_setup.create_empty_board(screen)

                        game_setup.insert_values(screen, np.copy(grid_vals), 
                            sol_ent)
                        
                        entries_ent = dict(((key, sol_ent[key]) 
                            for key in gh.get_cell_indices()))
                        

                    if error_occur:
                        if not blurred:
                            py.image.save(screen, "curr_grid_enter.png")
                            game_setup.blur_background(screen, 
                                "curr_grid_enter.png")
                            blurred = True
                        
                        game_setup.message_button(screen)
                        screen.blit(display_font.render("Invalid Input", True,
                             BLACK), (165, 175))
                       
                
                # Back button clicked
                elif curr_pos[0] >= 420 and curr_pos[0] <= 520:
                    enter_board = False
                    back_enter = True
            elif not (curr_pos[1] >= 550 and curr_pos[1] <= 590) and blurred:
                # Clicked outside of display message, return to 
                # previous screen

                if enter_board:
                    img = py.image.load("curr_grid_enter.png")
                else:
                    img = py.image.load("curr_grid.png")
                
                screen.blit(img, (0, 0))
                
                blurred = pos = False
            elif (not game_started and curr_pos[1] >= 410 and 
                curr_pos[1] <= 450):
                # Clicked on difficulty mode

                if curr_pos[0] >= 50 and curr_pos[0] <= 150:
                    if easy:
                        # Clicking twice will undo select mode
                        easy = False
                    else:
                        easy = True

                    medium = hard = default = False
                elif curr_pos[0] >= 210 and curr_pos[0] <= 310:
                    if medium:
                        medium = False
                    else:
                        medium = True
                    
                    easy = hard = default = False
                elif curr_pos[0] >= 370 and curr_pos[0] <= 470:
                    if hard:
                        hard = False
                    else:
                        hard = True
                    
                    easy = medium = default = False
            elif (curr_pos[1] >= 515 and curr_pos[1] <= 555 and not 
                game_started):
                # Clicked on an assist mode

                if curr_pos[0] >= 130 and curr_pos[0] <= 230:
                    assist = True
                elif curr_pos[0] >= 300 and curr_pos[0] <= 400:
                    assist = False      
        elif event.type == py.KEYDOWN:
            # Key is pressed down 
            if game_started and str(entries[(x,y)]).isnumeric():
                input_num = event.unicode
            elif enter_board and str(entries_ent[(x,y)]).isnumeric():
                input_num = event.unicode

            
            # Backspace key was pressed down
            if event.key == py.K_BACKSPACE:
                if assist:
                    #get prev entry
                    prev = entries[(x,y)]


                if game_started:
                    if str(entries[(x,y)]).isnumeric():
                        #used to erase but think u could prob remove and just re-order
                        py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                        entries[(x,y)] = 0
                        py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))

                        if assist:      
                            vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in range(9)] for col in range(9)]
                            np_grid = np.array(vals) 
                            sq_x_init = 3*round((int(x/60)-1)/3)
                            sq_y_init = 3*round((int(y/60)-1)/3)
                            square = np_grid[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                            col_count = np.count_nonzero(np_grid[:,int(x/60)] == prev)
                            row_count = np.count_nonzero(np_grid[int(y/60),:] == prev)
                            sq_count = np.count_nonzero(square == prev)

                            #COL
                            if (col_count == 1):

                                ind = np.where((np_grid[:,int(x/60)]) == prev)

                                if str(entries[x,(ind[0][0]*60)]).isnumeric():
                                    t = np_grid[3*round((int(x/60)-1)/3):(3*round((int(x/60)-1)/3)+3), 3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3]

                                    if (not np.count_nonzero(np_grid[ind[0][0],:] == prev) > 1 and 
                                        not np.count_nonzero(t == prev) > 1) and (y != ind[0][0]*60): 
                                        if (x,(ind[0][0]*60)) in invalid_spots.keys():
                                            del invalid_spots[(x,(ind[0][0]*60))] 
                                        if generate_sol:
                                            py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                                        else:
                                            py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,(ind[0][0]*60)+3, 56, 56))
                                        screen.blit(num_font.render(str(entries[x, (ind[0][0]*60)]) , True , (255,0,0)), (25+x, 25+((ind[0][0]*60))))
                            #ROW
                            if (row_count == 1):
                                ind = np.where((np_grid[int(y/60),:]) == prev)

                                if str(entries[(ind[0][0]*60),y]).isnumeric():
                                
                                    t = np_grid[3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3, 3*round((int(y/60)-1)/3):(3*round((int(y/60)-1)/3)+3)]
                                    
                                    if (not np.count_nonzero(np_grid[:,ind[0][0]] == prev) > 1 and 
                                        not np.count_nonzero(t == prev) > 1) and (x != ind[0][0]*60):
                                        if ((ind[0][0]*60),y) in invalid_spots.keys():
                                            del invalid_spots[((ind[0][0]*60),y)]  
                                        if generate_sol:
                                            py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                                        else:
                                            py.draw.rect(screen,(255, 204, 255), py.Rect((ind[0][0]*60)+3,y+3, 56, 56))
                                        screen.blit(num_font.render(str(entries[(ind[0][0]*60), y]) , True , (255,0,0)), (25+(ind[0][0]*60), 25+y))
                        
                        if (x,y) in invalid_spots.keys():
                            del invalid_spots[(x,y)]

                elif enter_board:
                        if str(entries_ent[(x1,y1)]).isnumeric():
                            py.draw.rect(screen,(255, 255, 255), py.Rect(x1+3,y1+3, 56, 56))
                            entries_ent[(x1,y1)] = 0
                            py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))

                        if (x1,y1) in invalid_spots_ent.keys():
                            del invalid_spots_ent[(x1,y1)]

            # Delete key was pressed down
            if event.key == py.K_DELETE:
                game_setup.create_empty_board(screen)
                entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
    
                if not enter_board:
                    entries = {k: entries[k] if k not in used_spots else True for k in entries}
                    generate_sol = blurred = False
                    invalid_spots = {}
                else:
                    sol_ent = []
                    grid = np.reshape(list(entries.values()), (9, 9))
                    entries_ent = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)

                    invalid_spots_ent = {}
                game_setup.insert_values(screen, grid)
   
    ##EMPTY BOARD FOR INPUT
    if enter_board:
        mouse = py.mouse.get_pos()
        if mouse[1] >= 550 and mouse[1] <= 590:
            if mouse[0] >= 220 and mouse[0] <= 320:
                py.draw.rect(screen, (255,204,255), py.Rect(220, 550, 100, 40))
                py.draw.rect(screen, (0, 0, 0), py.Rect(220, 550, 100, 40), 3)

                py.draw.rect(screen, (192,192,192), py.Rect(420, 550, 100, 40))
                py.draw.rect(screen, (0, 0, 0), py.Rect(420, 550, 100, 40), 3)
            elif mouse[0] >= 420 and mouse[0] <= 520:
                py.draw.rect(screen, (192,192,192), py.Rect(220, 550, 100, 40))
                py.draw.rect(screen, (0, 0, 0), py.Rect(220, 550, 100, 40), 3)

                py.draw.rect(screen, (255,204,255), py.Rect(420, 550, 100, 40))
                py.draw.rect(screen, (0, 0, 0), py.Rect(420, 550, 100, 40), 3)
            else:
                py.draw.rect(screen, (192,192,192), py.Rect(220, 550, 100, 40))
                py.draw.rect(screen, (0, 0, 0), py.Rect(220, 550, 100, 40), 3)

                py.draw.rect(screen, (192,192,192), py.Rect(420, 550, 100, 40))
                py.draw.rect(screen, (0, 0, 0), py.Rect(420, 550, 100, 40), 3)
        else:
            py.draw.rect(screen, (192,192,192), py.Rect(220, 550, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(220, 550, 100, 40), 3)

            py.draw.rect(screen, (192,192,192), py.Rect(420, 550, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(420, 550, 100, 40), 3)

        screen.blit(py.font.SysFont('Monotype', 15).render('Solve' , True , (0,0,0)) , (245, 560))
        screen.blit(py.font.SysFont('Monotype', 15).render('Back' , True , (0,0,0)) , (450, 560))

    ##CHECKING FOR BUTTON EVENTS
    if game_started:
        #Get highlight feature to work without making buttons everytime
        game_setup.game_screen(screen, py.mouse.get_pos())  

         #Checking which keys are being pressed (used for holding feature)
        keys_pressed = py.key.get_pressed()

        if keys_pressed[py.K_LEFT]:
            if not generate_sol:
                #Erase previous empty square
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                #Advance in given dir
                x = gh.set_num(x, -60)
                #Highlight new pos
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
            elif not blurred:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
                
                x = gh.set_num(x, -60)

                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                if str(sol_entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))

        if keys_pressed[py.K_RIGHT]:
            if not generate_sol:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                x = gh.set_num(x, 60)
                
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
            elif not blurred:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
                
                x = gh.set_num(x, 60)

                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                if str(sol_entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))

        if keys_pressed[py.K_UP]:
            if not generate_sol:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                y = gh.set_num(y, -60)
                
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
            elif not blurred:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
               
                y = gh.set_num(y, -60)

                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                if str(sol_entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))

        if keys_pressed[py.K_DOWN]:
            if not generate_sol:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                y = gh.set_num(y, 60)
                
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
            elif not blurred:
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
                
                y = gh.set_num(y, 60)
                if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric():
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56)) 

                    if not str(entries[(x,y)]).isnumeric():
                        screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))
                
                if str(sol_entries[(x,y)]).isnumeric() and entries[(x,y)] == sol_entries[(x,y)]:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
    
        #Click pos
        if (pos and not(pos[1] >= 550 and pos[1] <= 590)):
            #and str(entries[gh.round_num(pos[0]), gh.round_num(pos[1])]).isnumeric()):
            if assist and str(entries[((gh.round_num(pos[0]), gh.round_num(pos[1])))]).isnumeric() and entries[((gh.round_num(pos[0]), gh.round_num(pos[1])))] != 0:
                vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in range(9)] for col in range(9)]
                sq_x_init = 3*round((int(gh.round_num(pos[0])/60)-1)/3)
                sq_y_init = 3*round((int(gh.round_num(pos[1])/60)-1)/3)
                np_grid = np.array(vals) 
                square = np.reshape(vals, (9, 9))[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                num = entries[((gh.round_num(pos[0]), gh.round_num(pos[1])))]
                
                if (np.count_nonzero(np_grid[int(gh.round_num(pos[1])/60),:] == num) > 1 or
                    np.count_nonzero(np_grid[:,int(gh.round_num(pos[0])/60)] == num) > 1
                    or np.count_nonzero(square == num) > 1):  
                        py.draw.rect(screen,(255, 255, 204), py.Rect(gh.round_num(pos[0])+3,gh.round_num(pos[1])+3, 56, 56))
                else:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(gh.round_num(pos[0])+3,gh.round_num(pos[1])+3, 56, 56))
            else:    
                py.draw.rect(screen,(255, 204, 255), py.Rect(gh.round_num(pos[0])+3,gh.round_num(pos[1])+3, 56, 56))
                if not str(entries[((gh.round_num(pos[0]), gh.round_num(pos[1])))]).isnumeric():
                    screen.blit(num_font.render(str(grid[gh.round_num(pos[0])//60][gh.round_num(pos[1])//60]), True , (0,0,0)), (25+gh.round_num(pos[0]), 25+gh.round_num(pos[1])))


            #Before gen sol 
            if entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric() and not ((gh.round_num(pos[0]), gh.round_num(pos[1])) == (x,y)):
                py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                if not str(entries[(x,y)]).isnumeric():
                    screen.blit(num_font.render(str(grid[x//60][y//60]), True , (0,0,0)), (25+x, 25+y))

            if generate_sol and entries[(x,y)] == sol_entries[(x,y)] and str(entries[(x,y)]).isnumeric():
                py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))

            (x,y) = (gh.round_num(pos[0]), gh.round_num(pos[1]))
            
            if str(entries[(x,y)]).isnumeric() and entries[(x,y)]!= 0:
                screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))

        #Enter input
        if str(input_num).isnumeric() and int(input_num) >= 1 and int(input_num) <= 9 and str(entries[(x,y)]).isnumeric():
                curr_pos = py.mouse.get_pos()

                #del need to re-highlight
                if sum(x == True for x in entries.values()) == len(used_spots):
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))

                #Spot is used (need to re-highlight)
                if (entries[(x,y)] != 0) or ((gh.round_num(curr_pos[0]), gh.round_num(curr_pos[1])) == (x,y)): 
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
                

                #Checking if assist is on
                if assist:
                    
                    #get prev entry
                    prev = entries[(x,y)]

                    entries[(x,y)] = int(input_num)
          
                    vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in range(9)] for col in range(9)]
                    np_grid = np.array(vals) 
                    sq_x_init = 3*round((int(x/60)-1)/3)
                    sq_y_init = 3*round((int(y/60)-1)/3)
                    square = np_grid[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                    num = int(input_num)
                
                    if (np.count_nonzero(np_grid[:,int(x/60)] == num) > 1 or
                        np.count_nonzero(np_grid[int(y/60),:] == num) > 1
                        or np.count_nonzero(square == num) > 1):
                        invalid_spots[(x,y)] = num
                        py.draw.rect(screen,(255, 255, 204), py.Rect(x+3,y+3, 56, 56))
                    else:
                        if (x,y) in invalid_spots.keys():
                            del invalid_spots[(x,y)] 
                        if generate_sol:
                            py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                        else:
                            py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,y+3, 56, 56))
                             
                    col_count = np.count_nonzero(np_grid[:,int(x/60)] == prev)
                    row_count = np.count_nonzero(np_grid[int(y/60),:] == prev)
                    sq_count = np.count_nonzero(square == prev)
                           
                    #COL
                    if (col_count == 1):
                        ind = np.where((np_grid[:,int(x/60)]) == prev)

                        if str(entries[x,(ind[0][0]*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            t = np_grid[3*round((int(x/60)-1)/3):(3*round((int(x/60)-1)/3)+3), 3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3]
                       
                            if (not np.count_nonzero(np_grid[ind[0][0],:] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (y != ind[0][0]*60): 
                                if (x,(ind[0][0]*60)) in invalid_spots.keys():
                                    del invalid_spots[(x,(ind[0][0]*60))] 
                                if generate_sol:
                                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                                else:
                                    py.draw.rect(screen,(255, 204, 255), py.Rect(x+3,(ind[0][0]*60)+3, 56, 56))
                             
                                screen.blit(num_font.render(str(entries[x, (ind[0][0]*60)]) , True , (255,0,0)), (25+x, 25+((ind[0][0]*60))))

                    #ROW
                    if (row_count == 1):
                        ind = np.where((np_grid[int(y/60),:]) == prev)

                        if str(entries[(ind[0][0]*60),y]).isnumeric() and str(prev).isnumeric() and prev != 0:
                           
                            t = np_grid[3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3, 3*round((int(y/60)-1)/3):(3*round((int(y/60)-1)/3)+3)]
               
                            if (not np.count_nonzero(np_grid[:,ind[0][0]] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (x != ind[0][0]*60):
                                if ((ind[0][0]*60),y) in invalid_spots.keys():
                                    del invalid_spots[((ind[0][0]*60),y)]  
                                if generate_sol:
                                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                                else:
                                    py.draw.rect(screen,(255, 204, 255), py.Rect((ind[0][0]*60)+3,y+3, 56, 56))
                         
                                screen.blit(num_font.render(str(entries[(ind[0][0]*60), y]) , True , (255,0,0)), (25+(ind[0][0]*60), 25+y))                    
                
                    #SQ
                    if (sq_count == 1):
                        ind = np.where(square == prev)
                        
                        if str(entries[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            if (not np.count_nonzero(np_grid[:,ind[0][0]+sq_y_init] == prev) > 1 and 
                                not np.count_nonzero(np_grid[ind[1][0]+sq_x_init,:] == prev) > 1 and 
                                (x,y) != ((ind[1][0]+sq_x_init)*60, (ind[0][0]+sq_y_init)*60)):
                                if ((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60) in invalid_spots.keys():
                                    del invalid_spots[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]  
                                if generate_sol:
                                    py.draw.rect(screen,(255, 255, 255), py.Rect(x+3,y+3, 56, 56))
                                else:
                                    py.draw.rect(screen,(255, 204, 255), py.Rect(((ind[1][0]+sq_x_init)*60)+3,((ind[0][0]+sq_y_init)*60)+3, 56, 56))

                                screen.blit(num_font.render(str(entries[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]) , True , (255,0,0)), (25+((ind[1][0]+sq_x_init)*60), 25+((ind[0][0]+sq_y_init)*60)))
                            #ind[0][0]+sq_y_init, ind[1][0]+sq_x_init
                else:
                    #Update entry for pos and display
                    prev = entries[(x,y)]
                    
                    entries[(x,y)] = int(input_num)   
                    
                    num = int(input_num)

                    vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in range(9)] for col in range(9)]
                    np_grid = np.array(vals) 
                    sq_x_init = 3*round((int(x/60)-1)/3)
                    sq_y_init = 3*round((int(y/60)-1)/3)
                    square = np_grid[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3] 

                    if (np.count_nonzero(np_grid[:,int(x/60)] == num) > 1 or
                        np.count_nonzero(np_grid[int(y/60),:] == num) > 1
                        or np.count_nonzero(square == num) > 1):  
                        invalid_spots[(x,y)] = num
                    else:
                        if (x,y) in invalid_spots.keys():
                            del invalid_spots[(x,y)] 
                    col_count = np.count_nonzero(np_grid[:,int(x/60)] == prev)
                    row_count = np.count_nonzero(np_grid[int(y/60),:] == prev)
                    sq_count = np.count_nonzero(square == prev)
            
                    #COL
                    if (col_count == 1):
                        ind = np.where((np_grid[:,int(x/60)]) == prev)

                        if str(entries[x,(ind[0][0]*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            t = np_grid[3*round((int(x/60)-1)/3):(3*round((int(x/60)-1)/3)+3), 3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3]
                            if (not np.count_nonzero(np_grid[ind[0][0],:] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (y != ind[0][0]*60): 
                                if (x,(ind[0][0]*60)) in invalid_spots.keys():
                                    del invalid_spots[(x,(ind[0][0]*60))] 

                    #ROW
                    if (row_count == 1):
                        ind = np.where((np_grid[int(y/60),:]) == prev)

                        if str(entries[(ind[0][0]*60),y]).isnumeric() and str(prev).isnumeric() and prev != 0:
                           
                            t = np_grid[3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3, 3*round((int(y/60)-1)/3):(3*round((int(y/60)-1)/3)+3)]
                           
                            if (not np.count_nonzero(np_grid[:,ind[0][0]] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (x != ind[0][0]*60):
                                if ((ind[0][0]*60),y) in invalid_spots.keys():
                                    del invalid_spots[((ind[0][0]*60),y)]  

                    if (sq_count == 1):
                        ind = np.where(square == prev)
                        
                        if str(entries[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            if (not np.count_nonzero(np_grid[:,ind[0][0]+sq_y_init] == prev) > 1 and 
                                not np.count_nonzero(np_grid[ind[1][0]+sq_x_init,:] == prev) > 1 and 
                                (x,y) != ((ind[1][0]+sq_x_init)*60, (ind[0][0]+sq_y_init)*60)):
                                if ((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60) in invalid_spots.keys():
                                    del invalid_spots[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]  

                screen.blit(num_font.render(input_num , True , (255,0,0)), (25+x, 25+y))
                
                #Reset
                input_num = 0
        pos = False
    elif enter_board:
        #Checking which keys are being pressed (used for holding feature)
        keys_pressed = py.key.get_pressed()

        if keys_pressed[py.K_LEFT]:
            if not blurred:
                #Erase previous empty square
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x1+3,y1+3, 56, 56)) 
                #Advance in given dir
                x1 = gh.set_num(x1, -60)
                #Highlight new pos
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))

        if keys_pressed[py.K_RIGHT]:
            if not blurred:
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x1+3,y1+3, 56, 56))
                
                x1 = gh.set_num(x1, 60)
                
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))

        if keys_pressed[py.K_UP]:
            if not blurred:
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x1+3,y1+3, 56, 56))
                
                y1 = gh.set_num(y1, -60)
                
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))

        if keys_pressed[py.K_DOWN]:
            if not blurred:
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x1+3,y1+3, 56, 56))
                
                y1 = gh.set_num(y1, 60)
                
                if entries_ent[(x1,y1)] == 0:
                    py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))
          
    
        if (pos and not(pos[1] >= 550 and pos[1] <= 590) and str(entries_ent[gh.round_num(pos[0]), gh.round_num(pos[1])]).isnumeric()):
            if sol_ent == []:
                py.draw.rect(screen,(255, 204, 255), py.Rect(gh.round_num(pos[0])+3,gh.round_num(pos[1])+3, 56, 56))
    
                #click
                if entries_ent[(x1,y1)] == 0 and not ((gh.round_num(pos[0]), gh.round_num(pos[1])) == (x1,y1)):
                    py.draw.rect(screen,(255, 255, 255), py.Rect(x1+3,y1+3, 56, 56))

                (x1,y1) = (gh.round_num(pos[0]), gh.round_num(pos[1]))
                
                if str(entries_ent[(x1,y1)]).isnumeric() and entries_ent[(x1,y1)]!= 0:
                    screen.blit(num_font.render(str(entries_ent[(x1,y1)]), True , (0,0,0)), (25+x1, 25+y1))

        #Enter input
        if str(input_num).isnumeric() and int(input_num) >= 1 and int(input_num) <= 9 and str(entries_ent[(x1,y1)]).isnumeric():
                if sol_ent == []:
                    curr_pos = py.mouse.get_pos()
                    
                    #del need to re-highlight
                    if sum(i == 0 for i in entries_ent.values()) == 81:
                        py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))

                    #Spot is used (need to re-highlight)
                    if (entries_ent[(x1,y1)] != 0) or ((gh.round_num(curr_pos[0]), gh.round_num(curr_pos[1])) == (x1,y1)):
                        py.draw.rect(screen,(255, 204, 255), py.Rect(x1+3,y1+3, 56, 56))
                    
                    #Update entry for pos and display
                    entries_ent[(x1,y1)] = int(input_num)

                    screen.blit(num_font.render(input_num , True , (0,0,0)), (25+x1, 25+y1))
                    
                    #Reset
                    input_num = 0
        pos = False
    else:
        game_setup.home_screen(screen, py.mouse.get_pos(), text_font)
        
        if easy:
            py.draw.rect(screen, (255,204,255), py.Rect(50, 410, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(50, 410, 100, 40), 3)
            screen.blit(text_font.render('EASY' , True , (0,0,0)) , (75, 420))
        elif medium:
            py.draw.rect(screen, (255,204,255), py.Rect(210, 410, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(210, 410, 100, 40), 3)
            screen.blit(text_font.render('MEDIUM' , True , (0,0,0)) , (228, 420))
        elif hard:
            py.draw.rect(screen, (255,204,255), py.Rect(370, 410, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(370, 410, 100, 40), 3)
            screen.blit(text_font.render('HARD' , True , (0,0,0)) , (398, 420))

        if assist:
            py.draw.rect(screen, (255, 204, 255), py.Rect(130, 515, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(130, 515, 100, 40), 3)

            screen.blit(text_font.render('On' , True , (0,0,0)) , (168, 525))
            screen.blit(text_font.render('Off' , True , (0,0,0)) , (330, 525))
        elif assist == False:
            py.draw.rect(screen, (255, 204, 255), py.Rect(300, 515, 100, 40))
            py.draw.rect(screen, (0, 0, 0), py.Rect(300, 515, 100, 40), 3)  

            screen.blit(text_font.render('On' , True , (0,0,0)) , (168, 525))    
            screen.blit(text_font.render('Off' , True , (0,0,0)) , (330, 525))

        game_started = False
    
    if info:
        # Load info screen
        game_setup.info_screen(screen, py.mouse.get_pos())
        
    #Display
    py.display.flip()
    fpsclock.tick(fps)
    
#Removing screenshot as its not needed anymore
if os.path.exists("curr_grid.png"): 
    os.remove("curr_grid.png")
if os.path.exists("blur_image.jpg"):
    os.remove("blur_image.jpg")
if os.path.exists("curr_grid_enter.png"): 
    os.remove("curr_grid_enter.png")

py.quit()