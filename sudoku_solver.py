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
fps = 5
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
game_started = info = generate_sol = blurred = back = pos = \
               easy = medium = hard = default = mode_diff = \
               enter_board = False

entries_ent = dict.fromkeys([k for k in gh.get_cell_indices()], 0)

invalid = {}
sol_ent = False

# Colors
RED = (255, 0, 0)
L_BLUE = (204, 229, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
PINK = (255, 204, 204)
BLUE = (0, 0, 255)
VIOLET = (255, 204, 255)

game_setup.home_screen(screen, py.mouse.get_pos(), text_font)

assist = None
input_num = 0
pg = 1

lines = game_setup.get_lines()

# Setting positions for grid
x = y = x1 = y1 = 300

while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            # Exiting game
            running = False

        if event.type == py.MOUSEBUTTONUP:
            pos = curr_pos = py.mouse.get_pos()

            if (curr_pos[1] >= 180 and curr_pos[1] <= 220
                and not game_started
                and not enter_board):
                if curr_pos[0] >=  90 and curr_pos[0] <= 180:
                    # Starting game
                    if back or os.path.exists("curr_grid_enter.png"):
                        cond1 = (str(default).isnumeric() and default == mode_diff and not
                                easy and not medium and not hard)

                        cond2 = (str(mode_diff).isnumeric() and mode_diff == 0 and easy)

                        cond3 = (mode_diff == 1 and medium)
                        
                        cond4 = (mode_diff == 2 and hard)
                        
                        cond5 = os.path.exists("curr_grid.png")
                        
                        if (cond1 or cond2 or cond3 or cond4) and cond5:
                            # Load previous Sudoku puzzle 
                            img = py.image.load("curr_grid.png")
                            screen.blit(img, (0, 0))        

                            for k in invalid.keys():
                                val = str(invalid[k])

                                py.draw.rect(screen, WHITE, py.Rect(
                                    k[0] + 3, k[1] + 3, 56, 56)
                                )

                                if assist:
                                    if k == (x, y):
                                        py.draw.rect(screen, PINK, py.Rect(
                                            k[0] + 3, k[1] + 3, 56, 56)
                                        )
                                    screen.blit(
                                        num_font.render(val, True, RED), 
                                        (25 + k[0], 25 + k[1])
                                    )
                                else:
                                    if k == (x, y):
                                        py.draw.rect(screen, L_BLUE, py.Rect(
                                            k[0] + 3, k[1] + 3, 56, 56)
                                        )

                                    screen.blit(
                                        num_font.render(val, True, BLUE), 
                                        (25 + k[0], 25 + k[1])
                                    )   
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

                                given_clues = game_setup.insert_values(screen, grid)
                                
                                entries = (
                                    gh.set_ents_dicts(given_clues)
                                )
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

                                given_clues = game_setup.insert_values(screen, grid)   

                                entries = (
                                            gh.set_ents_dicts(given_clues)
                                        )
                                invalid = {}
                            x = y = 300
                       
                            game_started = True
                            info = blurred = back = pos = enter_board = False                    
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

                        given_clues = game_setup.insert_values(screen, grid)   

                        entries = (
                                    gh.set_ents_dicts(given_clues)
                                )
                        invalid = {}

                        x = y = 300
                    
                    game_started = True
                    info = blurred = back = pos = enter_board = False   

                    input_num = 0
                elif (curr_pos[0] >= 350 and curr_pos[0] <= 440 and 
                      not enter_board):
                    # Info button clicked 
                    info = True
                    game_started = back = False
                elif (curr_pos[0] >= 220  and curr_pos[0] <= 310 and 
                      not enter_board):
                    # Enter button clicked
                    if not all(x == 0 for x in entries_ent.values()):
                        # Enter board previously visited
                        img = py.image.load("curr_grid_enter.png")
                        screen.blit(img, (0, 0))
                    else:
                        indices = [k for k in gh.get_cell_indices()]
                        entries_ent = dict.fromkeys(indices, 0)
                        
                        game_setup.create_empty_board(screen)
                    
                    enter_board = True
                    info = back = pos = False     
            elif (curr_pos[0] >= 420 and curr_pos[0] <= 520 and 
                curr_pos[1] >= 550 and curr_pos[1] <= 580 and info):
                # Back button in info screen clicked
                info = False
                pg = 1
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
 
                    given_clues = game_setup.insert_values(screen, grid)
                    entries = gh.set_ents_dicts(given_clues)

                    generate_sol = blurred = False
                    invalid = {}

                    x = y = 300
                    input_num = 0
                elif curr_pos[0] >= 160 and curr_pos[0] <= 260:   
                    # Generate solution button clicked
                    sol = solve_data.solve_puzzle(np.copy(grid))

                    game_setup.create_empty_board(screen)
                    
                    game_setup.insert_values(screen, grid, sol)
                    entries = {(x, y): sol[(y // 60, x // 60)] if (x, y) not in given_clues 
                        else True for x, y in entries}

                    generate_sol = True
                    blurred = False
                elif curr_pos[0] >= 290 and curr_pos[0] <= 390:
                    # Verify button clicked

                    grid_vals = gh.get_curr_grid_vals(entries, given_clues,
                                    grid)
                    
                    if gen_data.verify.verify_validness(grid_vals):
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
                    
                    if not blurred:
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
                    elif default:
                        mode_diff = default

            elif curr_pos[1] >= 550 and curr_pos[1] <= 590 and enter_board:
                # Clear button clicked
                if curr_pos[0] >= 20 and curr_pos[0] <= 120:
                    game_setup.create_empty_board(screen)

                    indices = [key for key in gh.get_cell_indices()]
                    
                    entries_ent = dict.fromkeys(indices, 0)
                    
                    game_setup.insert_values(screen, np.reshape(list(entries_ent.values()), (9, 9)))
                    
                    sol_ent = False
                
                # Solved button clicked
                if curr_pos[0] >= 220 and curr_pos[0] <= 320:
                    grid_vals = gh.get_curr_grid_vals(entries_ent)
                    
                    sol_ent = False
                    error_occur = False
                    err_message = ""

                    try:
                        sol_ent = solve_data.solve_puzzle(np.copy(grid_vals))
                    except ValueError as err:
                        error_occur = True
                        err_message = str(err)
                        
                    if type(sol_ent) == np.ndarray:
                        game_setup.create_empty_board(screen)

                        game_setup.insert_values(screen, np.copy(grid_vals), 
                            sol_ent)
                 
                    if error_occur:
                        if not blurred:
                            py.image.save(screen, "curr_grid_enter.png")
                            game_setup.blur_background(screen, 
                                "curr_grid_enter.png")
                            blurred = True
                        
                        game_setup.display_message(screen)
                        if err_message == "Has Duplicates":
                            screen.blit(display_font.render(err_message, True,
                             BLACK), (175, 175))
                        elif err_message == "Not Enough Clues":
                            screen.blit(display_font.render(err_message, True,
                             BLACK), (155, 175))
                        else:
                            screen.blit(display_font.render(err_message, True,
                                BLACK), (190, 175))
                                   
                # Back button clicked
                elif curr_pos[0] >= 420 and curr_pos[0] <= 520:
                    enter_board = False
                    py.image.save(screen, "curr_grid_enter.png")             
            elif not (curr_pos[1] >= 550 and curr_pos[1] <= 590) and blurred:
                # Clicked outside of display message, return to 
                # previous screen

                if enter_board:
                    img = py.image.load("curr_grid_enter.png")
                else:
                    img = py.image.load("curr_grid.png")
                
                screen.blit(img, (0, 0))
                
                blurred = pos = False
            elif (not game_started and curr_pos[1] >= 340 and 
                curr_pos[1] <= 380):
                # Clicked on difficulty mode
                
                if curr_pos[0] >= 90 and curr_pos[0] <= 180:
                    if easy: 
                        # Clicking twice will undo select mode
                        easy = False
                    else:
                        easy = True

                    medium = hard = default = False
                elif curr_pos[0] >= 220 and curr_pos[0] <= 310:
                    if medium:
                        medium = False
                    else:
                        medium = True
                    
                    easy = hard = default = False
                elif curr_pos[0] >= 350 and curr_pos[0] <= 410:
                    if hard:
                        hard = False
                    else:
                        hard = True
                    
                    easy = medium = default = False
            elif (curr_pos[1] >= 470 and curr_pos[1] <= 510 and not
                game_started):
                # Clicked on an assist mode

                if curr_pos[0] >= 155 and curr_pos[0] <= 245:
                    if assist:
                        assist = None
                    else:
                        assist = True
                elif curr_pos[0] >= 285 and curr_pos[0] <= 375:
                    if assist == False:
                        assist = None
                    else:
                        assist = False  
            elif curr_pos[1] >= 555 and curr_pos[1] <= 575 and info:
                if curr_pos[0] >= 50 and curr_pos[0] <= 60 and pg != 1:
                    pg -= 1
                elif curr_pos[0] >= 115 and curr_pos[0] <= 125 and pg != 2:
                    pg += 1

        elif event.type == py.KEYDOWN:
            # Key is pressed down 
            if (game_started and str(entries[(x, y)]).isnumeric() or enter_board):
                input_num = event.unicode
            
            # Backspace key was pressed down
            if event.key == py.K_BACKSPACE:
                if assist:
                    # Get current entry
                    prev = entries[(x,y)]

                if game_started:
                    if str(entries[(x,y)]).isnumeric():
                        py.draw.rect(screen, L_BLUE, 
                            py.Rect(x + 3, y + 3, 56, 56))
                        entries[(x,y)] = 0

                        if assist:      
                            # Assist is on, check if removal removed
                            # any conflicts

                            curr_vals = gh.get_curr_grid_vals(entries, 
                                given_clues, grid)

                            col_count, row_count, sq_count = (
                                gh.count_occurrences(curr_vals, prev, x, y)
                            )

                            if (col_count == 1):
                                # Column is valid, check row and square

                                idx = np.where(curr_vals[:,x // 60] == prev)
                                idx = idx[0][0]


                                if str(entries[x, idx * 60]).isnumeric():
                                    sq = gh.get_square(curr_vals, x, idx)
                                    
                                    if (not np.count_nonzero(curr_vals[idx,:]
                                        == prev) > 1 and not 
                                        np.count_nonzero(sq == prev) > 1 and 
                                        (y != idx * 60)): 

                                        if (x, idx * 60) in invalid.keys():
                                            del invalid[(x, idx * 60)] 
                                        py.draw.rect(screen, WHITE, 
                                            py.Rect(x + 3, (idx * 60) + 3, 56, 56))
                                        

                                        screen.blit(num_font.render(
                                            str(entries[x, (idx * 60)]), True,
                                            BLUE), (25 + x, 25 + (idx * 60)))
                         
                            if (row_count == 1):
                                idx = np.where((curr_vals[y // 60,:]) == prev)
                                idx = idx[0][0]

                                if str(entries[(idx * 60), y]).isnumeric():
                                    sq = gh.get_square(curr_vals, idx, y)
                                    
                                    if ((not np.count_nonzero(curr_vals[:,idx] 
                                        == prev) > 1 and not 
                                        np.count_nonzero(sq == prev) > 1) and
                                        (x != idx * 60)):

                                        if ((idx * 60), y) in invalid.keys():
                                            del invalid[(idx * 60, y)]  
                                
                                        py.draw.rect(screen, WHITE, 
                                            py.Rect((idx * 60) + 3, y + 3, 56, 56))

                                        screen.blit(num_font.render(
                                            str(entries[(idx * 60), y]), True,
                                            BLUE), (25 + (idx * 60), 25 + y))
                        
                        if (x, y) in invalid.keys():
                            del invalid[(x, y)]

                elif enter_board:
                    if str(entries_ent[(x1, y1)]).isnumeric():
                        py.draw.rect(screen, WHITE, py.Rect(x1 + 3, y1 + 3, 
                            56, 56))
                        
                        entries_ent[(x1, y1)] = 0

                        py.draw.rect(screen, L_BLUE, py.Rect(x1 + 3, y1 + 3,
                            56, 56))

            # Delete key was pressed down
            if event.key == py.K_DELETE:
                game_setup.create_empty_board(screen)

                indices = [key for key in gh.get_cell_indices()]
                
                invalid = {}
                
                if not enter_board:
                    entries = dict.fromkeys(indices, 0)
                    entries = {k: entries[k] if k not in given_clues else True 
                        for k in entries} 
                    
                    game_setup.insert_values(screen, grid)
                    
                    generate_sol = blurred = False
                else:
                    entries_ent = dict.fromkeys(indices, 0)
                    
                    game_setup.insert_values(screen, np.reshape(list(entries_ent.values()), (9, 9)))
                    
                    sol_ent = False

    if game_started:
        game_setup.game_screen(screen, py.mouse.get_pos())  
    
        keys_pressed = py.key.get_pressed()
     
        if keys_pressed[py.K_LEFT]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist
            
                gh.advance(screen, (x, y, WHITE), grid, entries, invalid_ent)
                
                x = gh.set_num(x, -60)

                invalid_ent = (x, y) in invalid.keys() and assist
                
                if invalid_ent:
                    gh.advance(screen, (x, y, PINK), grid, entries, invalid_ent)
                else:
                    gh.advance(screen, (x, y, L_BLUE), grid, entries, invalid_ent)
                                     
        if keys_pressed[py.K_RIGHT]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist
                gh.advance(screen, (x, y, WHITE), grid, entries, invalid_ent)
                
                
                x = gh.set_num(x, 60)
                invalid_ent = (x, y) in invalid.keys() and assist
                if invalid_ent:
                    gh.advance(screen, (x, y, PINK), grid, entries, invalid_ent)
                else:
                    gh.advance(screen, (x, y, L_BLUE), grid, entries, invalid_ent)
      
        if keys_pressed[py.K_UP]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist
                gh.advance(screen, (x, y, WHITE), grid, entries, invalid_ent)
                
                y = gh.set_num(y, -60)
                
                invalid_ent = (x, y) in invalid.keys() and assist
                if invalid_ent:
                    gh.advance(screen, (x, y, PINK), grid, entries, invalid_ent)
                else:
                    gh.advance(screen, (x, y, L_BLUE), grid, entries, invalid_ent)

        if keys_pressed[py.K_DOWN]:
            if not blurred:
                invalid_ent = (x, y) in invalid.keys() and assist
                
                gh.advance(screen, (x, y, WHITE), grid, entries, invalid_ent)
                
                y = gh.set_num(y, 60)
                
                invalid_ent = (x, y) in invalid.keys() and assist
                if invalid_ent:
                    gh.advance(screen, (x, y, PINK), grid, entries, invalid_ent)
                else:
                    gh.advance(screen, (x, y, L_BLUE), grid, entries, invalid_ent)

        if pos and not (pos[1] >= 550 and pos[1] <= 590):
            # A cell was clicked
    
            idx =  (gh.round_num(pos[0]), gh.round_num(pos[1]))
            
            curr_x = gh.round_num(pos[0])
            curr_y = gh.round_num(pos[1])
            
            if (curr_x, curr_y) != (x, y) and (
                str(entries[(x, y)]).isnumeric() 
                and entries[(x, y)] != 0): 
                py.draw.rect(screen, WHITE, py.Rect(x + 3, y + 3, 56, 56))
                if (x, y) in invalid.keys() and assist:
                    screen.blit(num_font.render(str(entries[(x, y)]), True, RED),
                    (25 + x, 25 + y))
                else:
                    screen.blit(num_font.render(str(entries[(x, y)]), True, BLUE),
                    (25 + x, 25 + y))
           
            if assist and str(entries[idx]).isnumeric() and entries[idx] != 0:
                curr_vals = gh.get_curr_grid_vals(entries, given_clues, grid)
                square = gh.get_square(curr_vals, curr_x, curr_y)

                num = entries[(curr_x, curr_y)]

                (col_count, row_count, sq_count) = (
                    gh.count_occurrences(curr_vals, num, curr_x, curr_y)
                )
                
                if col_count > 1 or row_count > 1 or sq_count > 1:  
                    py.draw.rect(screen, PINK, py.Rect(curr_x + 3, 
                        curr_y + 3, 56, 56))
                else:
                    py.draw.rect(screen, L_BLUE, py.Rect(curr_x + 3, 
                        curr_y + 3, 56, 56))
            else:    
                py.draw.rect(screen, L_BLUE, py.Rect(curr_x + 3, curr_y + 3,
                    56, 56))
                if not str(entries[(curr_x, curr_y)]).isnumeric():

                    if (x, y) in invalid.keys() and assist:
                        screen.blit(num_font.render(str(grid[(curr_y // 60, curr_x // 60)]), 
                        True, BLACK), (25 + curr_x, 25 + curr_y))
                    else:
                       screen.blit(num_font.render(str(grid[(curr_y // 60, curr_x // 60)]), 
                        True, BLACK), (25 + curr_x, 25 + curr_y))


            if (entries[(x,y)] == 0 or not str(entries[(x,y)]).isnumeric()):
                if (x, y) != (curr_x, curr_y):
                    py.draw.rect(screen, WHITE, py.Rect(x + 3, y + 3, 56, 56))
                
                if not str(entries[(x,y)]).isnumeric():
                    screen.blit(num_font.render(str(grid[(y //60, x // 60)]),
                        True, BLACK), (25 + x, 25 + y))
            
            #After generating sol, only replace values w/ new entry
            if (generate_sol and entries[(x,y)] == sol[(y // 60, x // 60)] 
                and str(entries[(x,y)]).isnumeric()):
                py.draw.rect(screen, WHITE, py.Rect(x + 3, y + 3, 56, 56))
                
                if (x, y) in invalid.keys() and assist:
                    screen.blit(num_font.render(str(entries[(x, y)]), True, RED),
                    (25 + x, 25 + y))
                else:
                    screen.blit(num_font.render(str(entries[(x, y)]), True, BLUE),
                    (25 + x, 25 + y))

            (x,y) = (curr_x, curr_y)
            
            if str(entries[(x,y)]).isnumeric() and entries[(x,y)] != 0:
                if (x, y) in invalid.keys() and assist:
                    
                    screen.blit(num_font.render(str(entries[(x,y)]), True, RED),
                    (25 + x, 25 + y))
                else:
                    screen.blit(num_font.render(str(entries[(x,y)]), True, BLUE),
                    (25 + x, 25 + y))
            
        if (str(input_num).isnumeric() and int(input_num) >= 1 and 
            int(input_num) <= 9 and str(entries[(x,y)]).isnumeric()):
            # Enter input

                py.draw.rect(screen, WHITE, py.Rect(x + 3, y + 3, 
                         56, 56))
                
                prev = entries[(x, y)]
                entries[(x, y)] = num = int(input_num)
        
                curr_vals = gh.get_curr_grid_vals(entries, given_clues,
                    grid)

                square = gh.get_square(curr_vals, x, y)

                (col_count, row_count, sq_count) = gh.count_occurrences(
                    curr_vals, num, x, y
                )
              
                # Number is already used in row, col, sq (or all)
                if col_count > 1 or row_count > 1 or sq_count > 1:              
                    if col_count > 1:
                        idx = np.where(curr_vals[:,x // 60] == num)[0] 
                        num_col_entries = [(x, idx[i] * 60) for i, val in enumerate(idx)]
                        
                        for elem in num_col_entries:
                            if str(entries[elem]).isnumeric():
                                invalid[elem] = num
                                if assist:
                                    py.draw.rect(screen, WHITE, py.Rect(x + 3,
                                        elem[1] + 3, 56, 56))
                                    screen.blit(num_font.render(str(entries[elem]), True, RED), 
                                                    (25 + x, 25 + (elem[1]))
                                                )
            
                    if row_count > 1:
                        idx = np.where(curr_vals[y // 60,:] == num)[0] 
                        num_row_entries = [(idx[i] * 60, y) for i, val in enumerate(idx)]
                        
                        for elem in num_row_entries:
                            if str(entries[elem]).isnumeric():
                                invalid[elem] = num
                                if assist:
                                    py.draw.rect(screen, WHITE, py.Rect(elem[0] + 3,
                                        y + 3, 56, 56))
                                    screen.blit(num_font.render(str(entries[elem]), True, RED), 
                                                    (25 + elem[0], 25 + y)
                                                )

                    if sq_count > 1:
                        idx = np.where(square == num)

                        x_idx = idx[1]
                        y_idx = idx[0]
                        
                        num_sq_entries = [(((x_idx[i] + 3 * round(((x // 60) - 1) / 3)) * 60),
                                            (y_idx[i] + 3 * round(((y // 60) - 1) / 3)) * 60) 
                                           for i in range(len(x_idx))]
                                    
                        for elem in num_sq_entries:
                            if str(entries[elem]).isnumeric():
                                invalid[elem] = num
                                if assist:
                                    py.draw.rect(screen, WHITE, py.Rect(elem[0] + 3,
                                        elem[1] + 3, 56, 56))
                                    screen.blit(num_font.render(str(entries[elem]), True, RED), 
                                                    (25 + elem[0], 25 + elem[1])
                                                )
                else:
                    if (x, y) in invalid.keys():
                        del invalid[(x, y)] 

                # Count occurrences to check if the change to prev 
                # entry make another entry valid
                (col_count, row_count, sq_count) = gh.count_occurrences(
                    curr_vals, prev, x, y
                )
    
                if (col_count == 1) and prev != 0:
                    # Change color of prev to indicate it is valid, 
                    # locate its position and check the sq and row
                    # for duplicates
                    idx = np.where(curr_vals[:,x // 60] == prev)
                    idx = idx[0][0]
                    
                    if (str(entries[x, idx * 60]).isnumeric() and 
                        str(prev).isnumeric()):
                        
                        sq = gh.get_square(curr_vals, idx * 60, x) 
          
                        if (not np.count_nonzero(curr_vals[idx,:] == prev)
                            > 1 and not np.count_nonzero(sq == prev) > 1
                            and (y != idx * 60)): 

                            if (x, idx * 60) in invalid.keys():
                                del invalid[(x, (idx * 60))] 

                            if assist:
                                py.draw.rect(screen, WHITE, py.Rect(x + 3,
                                    (idx * 60) + 3, 56, 56))
                                
                                if (x, idx * 60) in invalid.keys():
                                    screen.blit(num_font.render(str(entries[x, 
                                        (idx * 60)]), True, RED), 
                                        (25 + x, 25 + (idx * 60))
                                    )
                                else:
                                    screen.blit(num_font.render(str(entries[x, 
                                        (idx * 60)]), True, BLUE), 
                                        (25 + x, 25 + (idx * 60))
                                    )  
                if (row_count == 1) and prev != 0:
                    idx = np.where(curr_vals[y // 60,:] == prev)
                    idx = idx[0][0]
                    
                    if (str(entries[(idx * 60), y]).isnumeric() and 
                        str(prev).isnumeric()):

                        sq = gh.get_square(curr_vals, idx * 60, y)
                    
                        if (not np.count_nonzero(curr_vals[:,idx] == prev) > 1
                            and not np.count_nonzero(sq == prev) > 1 
                            and (x != idx * 60)):
                            if ((idx * 60), y) in invalid.keys():
                                del invalid[((idx * 60), y)] 
                      
                            if assist:                           
                                py.draw.rect(screen, WHITE, py.Rect((idx * 60) + 3, 
                                    y + 3, 56, 56)
                                )

                                if ((idx * 60), y) in invalid.keys():
                                    screen.blit(num_font.render(
                                        str(entries[(idx * 60), y]), True, RED),
                                        (25 + (idx * 60), 25 + y)
                                    )   
                                else:
                                    screen.blit(num_font.render(
                                        str(entries[(idx * 60), y]), True, BLUE),
                                        (25 + (idx * 60), 25 + y)
                                    )                         
                if (sq_count == 1) and prev != 0:
                    idx = np.where(square == prev)
                    x_idx = idx[1][0] + 3 * round(((x // 60) - 1) / 3)
                    y_idx = idx[0][0] + 3 * round(((y // 60) - 1) / 3)
                    
                    cell_idx = (x_idx * 60, y_idx * 60) 
                
                    if (str(entries[cell_idx]).isnumeric() and 
                        str(prev).isnumeric()):
                        
                        if (not (np.count_nonzero(curr_vals[y_idx,:] == prev) 
                            > 1) and not (np.count_nonzero(curr_vals[:,x_idx] 
                            == prev) > 1) and 
                            (x, y) != (x_idx * 60, y_idx * 60)):

                            if cell_idx in invalid.keys():
                                del invalid[cell_idx] 

                            if assist:
                                py.draw.rect(screen, WHITE, 
                                py.Rect(cell_idx[0] + 3, cell_idx[1] + 3, 56, 56))
                                if (25 + cell_idx[0], 25 + cell_idx[1]) in invalid.keys():
                                    screen.blit(num_font.render(str(
                                    entries[cell_idx]), True, RED), 
                                    (25 + cell_idx[0], 25 + cell_idx[1])
                                )
                                else:
                                    
                                    screen.blit(num_font.render(str(
                                    entries[cell_idx]), True, BLUE), 
                                    (25 + cell_idx[0], 25 + cell_idx[1])
                                )           

                if (x, y) in invalid.keys() and assist:
                    py.draw.rect(screen, PINK, py.Rect(x + 3,
                                    y + 3, 56, 56))
                    screen.blit(num_font.render(input_num, True, RED), 
                        (25 + x, 25 + y)
                    )
                else:
                    py.draw.rect(screen, L_BLUE, py.Rect(x + 3,
                                    y + 3, 56, 56))
                    screen.blit(num_font.render(input_num, True, BLUE), 
                        (25 + x, 25 + y)
                    )
            
                #Reset
                input_num = 0

        pos = False
    elif enter_board:
        game_setup.enter_board_screen(screen, py.mouse.get_pos())
   
        keys_pressed = py.key.get_pressed()
         
        if keys_pressed[py.K_LEFT]:
            if not blurred:
                # Erase previous empty square
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                # Advance in given dir
                x1 = gh.set_num(x1, -60)
                
                # Highlight new pos
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent)

        if keys_pressed[py.K_RIGHT]:
            if not blurred:
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                x1 = gh.set_num(x1, 60)
                
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent)

        if keys_pressed[py.K_UP]:
            if not blurred:
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                y1 = gh.set_num(y1, -60)
                
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent)

        if keys_pressed[py.K_DOWN]:
            if not blurred:
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                y1 = gh.set_num(y1, 60)
                
                if type(sol_ent) == np.ndarray:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent, sol_ent)
                else:
                    gh.enter_board_adv(screen, (x1, y1, L_BLUE), entries_ent)
                  
        if (pos and not(pos[1] >= 550 and pos[1] <= 590)):
            curr_idx = (gh.round_num(pos[0]), gh.round_num(pos[1]))

            if type(sol_ent) == bool:
                py.draw.rect(screen, L_BLUE, py.Rect(curr_idx[0] + 3, 
                    curr_idx[1] + 3, 56, 56))
    
                # Click
                if not curr_idx == (x1, y1):
                    py.draw.rect(screen, WHITE, py.Rect(x1 + 3, y1 + 3, 
                        56, 56))
                    if entries_ent[(x1, y1)] != 0:
                        if (str(entries_ent[(x1, y1)]).isnumeric() and 
                            entries_ent[(x1, y1)] != 0):

                            screen.blit(num_font.render(str(entries_ent[(x1, y1)]), 
                                True, BLACK), (25 + x1, 25 + y1))


                (x1, y1) = curr_idx
                
                if (str(entries_ent[curr_idx]).isnumeric() and 
                    entries_ent[curr_idx] != 0):

                    screen.blit(num_font.render(str(entries_ent[curr_idx]), 
                        True, BLACK), (25 + x1, 25 + y1))

        if (str(input_num).isnumeric() and int(input_num) >= 1 and 
            int(input_num) <= 9 and str(entries_ent[(x1, y1)]).isnumeric()): 
            # Enter input
            
            if type(sol_ent) == bool:    
            
                #py.draw.rect(screen, L_BLUE, py.Rect(x1 + 3, y1 + 3, 56, 56))
                
                # if sum(i == 0 for i in entries_ent.values()) == 81:
                #     # Delete pressed, need to re-highlight cell
                #     py.draw.rect(screen, L_BLUE, py.Rect(x1 + 3, y1 + 3, 56, 56))
                #     print("!!")
                
                # if (entries_ent[(x1, y1)] != 0 or (gh.round_num(curr_pos[0]), 
                #     gh.round_num(curr_pos[1])) == (x1,y1)):
                #     # Spot is used (need to re-highlight)
                #     py.draw.rect(screen, L_BLUE, py.Rect(x1 + 3, y1 + 3, 56, 56))
                
                # Update entry for pos and display
                entries_ent[(x1, y1)] = int(input_num)

                if entries_ent[(x1, y1)] != 0:
                    py.draw.rect(screen, L_BLUE, py.Rect(x1 + 3, y1 + 3, 56, 56))

                screen.blit(num_font.render(input_num, True, BLACK), (25 + x1, 25 + y1))
            
            # Reset
            input_num = 0
        pos = False
    elif not info:
        game_setup.home_screen(screen, py.mouse.get_pos(), text_font)

        try: curr_pos
        except NameError: curr_pos = None

        # Keep highlight on clicked button
        
        if easy or (str(default).isnumeric() and default == 0):
            py.draw.rect(screen, VIOLET, py.Rect(90, 340, 90, 40))
            py.draw.rect(screen, BLACK, py.Rect(90, 340, 90, 40), 3)
            screen.blit(text_font.render('EASY', True, BLACK), (110, 350))
        elif medium or (default == 1):
            py.draw.rect(screen, VIOLET, py.Rect(220, 340, 90, 40))
            py.draw.rect(screen, BLACK, py.Rect(220, 340, 90, 40), 3)
            screen.blit(text_font.render('MEDIUM', True, BLACK), (232, 350))
        elif hard or (default == 2):
            py.draw.rect(screen, VIOLET, py.Rect(350, 340, 90, 40))
            py.draw.rect(screen, BLACK, py.Rect(350, 340, 90, 40), 3)
            screen.blit(text_font.render('HARD', True, BLACK), (370, 350))
   
        if assist:
            py.draw.rect(screen, VIOLET, py.Rect(155, 470, 90, 40))
            py.draw.rect(screen, BLACK, py.Rect(155, 470, 90, 40), 3)

            screen.blit(text_font.render('On', True, BLACK), (190, 480))
            screen.blit(text_font.render('Off', True, BLACK), (315, 480))
        elif assist == False or (assist is None and back):

            py.draw.rect(screen, VIOLET, py.Rect(285, 470, 90, 40))
            py.draw.rect(screen, BLACK, py.Rect(285, 470, 90, 40), 3)  

            screen.blit(text_font.render('On', True, BLACK), (190, 480))    
            screen.blit(text_font.render('Off', True, BLACK), (315, 480))
        
    if info:
        if pg == 1:
            game_setup.info_screen(screen, py.mouse.get_pos(), lines[:20], pg)
        elif pg == 2:
            game_setup.info_screen(screen, py.mouse.get_pos(), lines[20:], pg)
            

    # Display
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