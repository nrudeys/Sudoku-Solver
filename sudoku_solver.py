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

invalid = invalid_spots_ent = {}
sol_ent = []

# Colors
RED = (255, 0, 0)
VIOLET = (255, 204, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
PINK = (255, 204, 204)

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

                            for k in invalid.keys():
                                val = str(invalid[k])
                                rect = py.Rect(k[0] + 3, k[1] + 3, 56, 56)

                                if assist:
                                    py.draw.rect(screen, PINK, rect)
                                else:
                                    py.draw.rect(screen, VIOLET, rect)

                                num = num_font.render(val, True, RED)
                                
                                screen.blit(num, (25 + k[0], 25 + k[1]))
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
                                
                                #sol = solve_data.solve_puzzle(np.copy(grid))
                                entries = (
                                    gh.set_ents_dicts(given_clues)
                                )

                                x = y = 300
                       
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

                        given_clues = game_setup.insert_values(screen, grid)   

                        #sol = solve_data.solve_puzzle(np.copy(grid))
                        entries = (
                                    gh.set_ents_dicts(given_clues)
                                )
                        invalid = {}

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
                                py.draw.rect(screen, PINK, rect)
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
                    grid_vals = game_setup.get_curr_grid_vals(entries_ent)
                    
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
            if (game_started and str(entries[(x, y)]).isnumeric() or enter_board):
                input_num = event.unicode
            
            # Backspace key was pressed down
            if event.key == py.K_BACKSPACE:
                if assist:
                    # Get current entry
                    prev = entries[(x,y)]

                if game_started:
                    if str(entries[(x,y)]).isnumeric():
                        py.draw.rect(screen, VIOLET, 
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


                                if str(entries[x, idx]).isnumeric():
                                    sq = gh.get_square(curr_vals, x, idx)
                                    
                                    if (not np.count_nonzero(curr_vals[idx,:]
                                        == prev) > 1 and not 
                                        np.count_nonzero(sq == prev) > 1 and 
                                        (y != idx * 60)): 

                                        if (x, idx * 60) in invalid.keys():
                                            del invalid[(x, idx * 60)] 
                                        if generate_sol:
                                            py.draw.rect(screen, WHITE, 
                                                py.Rect(x + 3, y + 3, 56, 56))
                                        else:
                                            py.draw.rect(screen, VIOLET, 
                                                py.Rect(x + 3, (idx * 60) + 3,
                                                56, 56))
                                        screen.blit(num_font.render(
                                            str(entries[x, (idx * 60)]), True,
                                            RED), (25 + x, 25 + (idx * 60)))
                            #ROW
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
                                        if generate_sol:
                                            py.draw.rect(screen, WHITE, 
                                                py.Rect(x + 3, y + 3, 56, 56))
                                        else:
                                            py.draw.rect(screen, VIOLET, 
                                                py.Rect((idx * 60) + 3, y + 3,
                                                56, 56))
                                        screen.blit(num_font.render(
                                            str(entries[(idx * 60), y]), True,
                                            RED), (25 + (idx * 60), 25 + y))
                        
                        if (x, y) in invalid.keys():
                            del invalid[(x, y)]

                elif enter_board:
                    if str(entries_ent[(x1, y1)]).isnumeric():
                        py.draw.rect(screen, WHITE, py.Rect(x1 + 3, y1 + 3, 
                            56, 56))
                        
                        entries_ent[(x1, y1)] = 0

                        py.draw.rect(screen, VIOLET, py.Rect(x1 + 3, y1 + 3,
                            56, 56))

                    if (x1, y1) in invalid_spots_ent.keys():
                        del invalid_spots_ent[(x1, y1)]

            # Delete key was pressed down
            if event.key == py.K_DELETE:
                game_setup.create_empty_board(screen)

                indices = [key for key in gh.get_cell_indices()]
                entries = entries_ent = dict.fromkeys(indices, 0)

                invalid = invalid_spots_ent = {}
    
                if not enter_board:
                    entries = {k: entries[k] if k not in given_clues else True 
                        for k in entries}

                    generate_sol = blurred = False
                else:
                    grid = np.reshape(list(entries.values()), (9, 9))
                    sol_ent = []

                game_setup.insert_values(screen, grid)        

    if game_started:
        game_setup.game_screen(screen, curr_pos)  

        keys_pressed = py.key.get_pressed()
        
        if keys_pressed[py.K_LEFT]:
            if not generate_sol:
                gh.advance(screen, (x, y, WHITE), grid, entries)
                
                x = gh.set_num(x, -60)
                
                gh.advance(screen, (x, y, VIOLET), grid, entries)
            elif not blurred:
                # Generate solution clicked and screen is not blurred

                gh.filled_board_advance(screen, (x, y, WHITE),
                     (grid, sol), entries)
                
                x = gh.set_num(x, -60)

                gh.filled_board_advance(screen, (x, y, VIOLET),
                     (grid, sol), entries)
                                    
        if keys_pressed[py.K_RIGHT]:
            if not generate_sol:
                gh.advance(screen, (x, y, WHITE), grid, entries)
                
                x = gh.set_num(x, 60)
                
                gh.advance(screen, (x, y, VIOLET), grid, entries) 
            elif not blurred:
                gh.filled_board_advance(screen, (x, y, WHITE),
                     (grid, sol), entries)
                
                x = gh.set_num(x, 60)

                gh.filled_board_advance(screen, (x, y, VIOLET),
                     (grid, sol), entries)

        if keys_pressed[py.K_UP]:
            if not generate_sol:
                gh.advance(screen, (x, y, WHITE), grid, entries)
                    
                y = gh.set_num(y, -60)
                
                gh.advance(screen, (x, y, VIOLET), grid, entries) 
            elif not blurred:
                gh.filled_board_advance(screen, (x, y, WHITE),
                     (grid, sol), entries)
                
                y = gh.set_num(y, -60)


                gh.filled_board_advance(screen, (x, y, VIOLET),
                     (grid, sol), entries)

        if keys_pressed[py.K_DOWN]:
            if not generate_sol:
                gh.advance(screen, (x, y, WHITE), grid, entries)
                
                y = gh.set_num(y, 60)
            
                gh.advance(screen, (x, y, VIOLET), grid, entries)
            elif not blurred:
                gh.filled_board_advance(screen, (x, y, WHITE),
                     (grid, sol), entries)
                
                y = gh.set_num(y, 60)

                gh.filled_board_advance(screen, (x, y, VIOLET),
                     (grid, sol), entries)

        if pos and not (pos[1] >= 550 and pos[1] <= 590):
            # A cell was clicked

            idx =  (gh.round_num(pos[0]), gh.round_num(pos[1]))
            
            curr_x = gh.round_num(pos[0])
            curr_y = gh.round_num(pos[1])

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
                    py.draw.rect(screen, VIOLET, py.Rect(curr_x + 3, 
                        curr_y + 3, 56, 56))
            else:    
                py.draw.rect(screen, VIOLET, py.Rect(curr_x + 3, curr_y + 3,
                    56, 56))
                if not str(entries[(curr_x, curr_y)]).isnumeric():
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
                
                screen.blit(num_font.render(str(entries[(x,y)]), True, RED),
                    (25 + x, 25 + y))

            (x,y) = (curr_x, curr_y)
            
            if str(entries[(x,y)]).isnumeric() and entries[(x,y)] != 0:
                screen.blit(num_font.render(str(entries[(x,y)]), True, RED),
                    (25 + x, 25 + y))
        
        if (str(input_num).isnumeric() and int(input_num) >= 1 and 
            int(input_num) <= 9 and str(entries[(x,y)]).isnumeric()):
            # Enter input

                # Del need to re-highlight
                if (sum(x == True for x in entries.values()) == 
                    len(given_clues)):
                    py.draw.rect(screen, VIOLET, py.Rect(x + 3, 
                        y + 3, 56, 56))

                # Spot is used (need to re-highlight)
                if ((gh.round_num(curr_pos[0]), gh.round_num(curr_pos[1])) 
                    == (x,y) or entries[(x,y)] != 0): 
                    py.draw.rect(screen, VIOLET, py.Rect(x + 3, y + 3, 
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
                    invalid[(x, y)] = num

                    if assist:
                        py.draw.rect(screen, PINK, py.Rect(
                            x + 3, y + 3, 56, 56)
                        )
                else:
                    if (x, y) in invalid.keys():
                        del invalid[(x, y)] 
                    if assist:
                        if generate_sol:
                            py.draw.rect(screen, WHITE, py.Rect(x + 3, y + 3,
                                56, 56))
                        else:
                            py.draw.rect(screen, VIOLET, py.Rect(x + 3, y + 3,
                                56, 56))
                
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
                        
                        sq = gh.get_square(curr_vals, x, idx)                       
                        
                        if (not np.count_nonzero(curr_vals[idx,:] == prev)
                            > 1 and not np.count_nonzero(sq == prev) > 1
                            and (y != idx * 60)): 
                        
                           
                            if (x, idx * 60) in invalid.keys():
                                del invalid[(x, (idx * 60))] 

                            if assist:
                                if generate_sol:
                                    py.draw.rect(screen, WHITE, py.Rect(x + 3,
                                        y + 3, 56, 56))
                                else:
                                    py.draw.rect(screen, VIOLET,
                                        py.Rect(x + 3, (idx * 60) + 3, 56, 56)
                                    )
                            
                                screen.blit(num_font.render(str(entries[x, 
                                    (idx * 60)]), True, RED), 
                                    (25 + x, 25 + (idx * 60))
                                )

                if (row_count == 1) and prev != 0:
                    idx = np.where(curr_vals[y // 60,:] == prev)
                    idx = idx[0][0]
                    
                    if (str(entries[(idx * 60), y]).isnumeric() and 
                        str(prev).isnumeric()):
                        
                        sq = gh.get_square(curr_vals, idx, y)
                    
                        if (not np.count_nonzero(curr_vals[:,idx] == prev) > 1
                            and not np.count_nonzero(sq == prev) > 1 
                            and (x != idx * 60)):
                            if ((idx * 60), y) in invalid.keys():
                                del invalid[((idx * 60), y)] 
                            if assist: 
                                if generate_sol:
                                    py.draw.rect(screen, WHITE, py.Rect(x + 3, 
                                        y + 3, 56, 56)
                                    )
                                else:
                                    py.draw.rect(screen, VIOLET, 
                                        py.Rect((idx * 60) + 3, y + 3, 56, 56)
                                    )
                        
                                screen.blit(num_font.render(
                                    str(entries[(idx * 60), y]), True, RED),
                                    (25 + (idx * 60), 25 + y)
                                )                    
            
                if (sq_count == 1) and prev != 0:
                    idx = np.where(square == prev)
                    x_idx = idx[1][0] + 3 * round(((x // 60) - 1) / 3)
                    y_idx = idx[0][0] + 3 * round(((y // 60) - 1) / 3)
                    
                    cell_idx = (x_idx * 60, y_idx * 60) 
                
                    if (str(entries[cell_idx]).isnumeric() and 
                        str(prev).isnumeric()):
                        
                        if (not (np.count_nonzero(curr_vals[:,y_idx] == prev) 
                            > 1) and not (np.count_nonzero(curr_vals[x_idx,:] 
                            == prev) > 1) and 
                            (x, y) != (x_idx * 60, y_idx * 60)):
                            
                            if cell_idx in invalid.keys():
                                del invalid[cell_idx] 

                            if assist:
                                if generate_sol:
                                    py.draw.rect(screen, WHITE, 
                                    py.Rect(x + 3, y + 3, 56, 56))
                            else:
                                py.draw.rect(screen, VIOLET, py.Rect(
                                    cell_idx[0] + 3, cell_idx[1] + 3,
                                    56, 56)
                                )

                            screen.blit(num_font.render(str(
                                entries[cell_idx]), True, RED), 
                                (25 + cell_idx[0], 25 + cell_idx[1])
                            )
            
                screen.blit(num_font.render(input_num, True, RED), 
                    (25 + x, 25 + y)
                )
            
                #Reset
                input_num = 0

        pos = False
    elif enter_board:
        game_setup.enter_board_screen(screen, curr_pos)
        
        keys_pressed = py.key.get_pressed()
         
        if keys_pressed[py.K_LEFT]:
            if not blurred:
                # Erase previous empty square
                gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                # Advance in given dir
                x1 = gh.set_num(x1, -60)
                
                # Highlight new pos
                gh.enter_board_adv(screen, (x1, y1, VIOLET), entries_ent)

        if keys_pressed[py.K_RIGHT]:
            if not blurred:
                gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                x1 = gh.set_num(x1, 60)
                
                gh.enter_board_adv(screen, (x1, y1, VIOLET), entries_ent)

        if keys_pressed[py.K_UP]:
            if not blurred:
                gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                y1 = gh.set_num(y1, -60)
                
                gh.enter_board_adv(screen, (x1, y1, VIOLET), entries_ent)

        if keys_pressed[py.K_DOWN]:
            if not blurred:
                gh.enter_board_adv(screen, (x1, y1, WHITE), entries_ent)
                
                y1 = gh.set_num(y1, 60)
                
                gh.enter_board_adv(screen, (x1, y1, VIOLET), entries_ent)
        
        if ((pos and not(pos[1] >= 550 and pos[1] <= 590) and 
            str(entries_ent[gh.round_num(pos[0]), 
                gh.round_num(pos[1])]).isnumeric())):

            curr_idx = (gh.round_num(pos[0]), gh.round_num(pos[1]))

            if sol_ent == []:
                py.draw.rect(screen, VIOLET, py.Rect(curr_idx[0] + 3, 
                    curr_idx[1] + 3, 56, 56))
    
                # Click
                if entries_ent[(x1, y1)] == 0 and not curr_idx == (x1, y1):
                    py.draw.rect(screen, WHITE, py.Rect(x1 + 3, y1 + 3, 
                        56, 56))

                (x1, y1) = curr_idx
                
                if (str(entries_ent[curr_idx]).isnumeric() and 
                    entries_ent[curr_idx] != 0):

                    screen.blit(num_font.render(str(entries_ent[curr_idx]), 
                        True, BLACK), (25 + x1, 25 + y1))

        if (str(input_num).isnumeric() and int(input_num) >= 1 and 
            int(input_num) <= 9 and str(entries_ent[(x1, y1)]).isnumeric()): 
            # Enter input
            
            if sol_ent == []:    
                
                if sum(i == 0 for i in entries_ent.values()) == 81:
                    # Delete pressed, need to re-highlight cell
                    py.draw.rect(screen, VIOLET, py.Rect(x1 + 3, y1 + 3, 56, 56))
      
                if (entries_ent[(x1, y1)] != 0 or (gh.round_num(curr_pos[0]), 
                    gh.round_num(curr_pos[1])) == (x1,y1)):
                    # Spot is used (need to re-highlight)
                    py.draw.rect(screen, VIOLET, py.Rect(x1 + 3, y1 + 3, 56, 56))
                
                # Update entry for pos and display
                entries_ent[(x1, y1)] = int(input_num)

                screen.blit(num_font.render(input_num, True, BLACK), (25 + x1, 25 + y1))
                
                # Reset
                input_num = 0
        pos = False
    else:
        game_setup.home_screen(screen, py.mouse.get_pos(), text_font)
        
        # Keep highlight on clicked button
        if easy:
            py.draw.rect(screen, VIOLET, py.Rect(50, 410, 100, 40))
            py.draw.rect(screen, BLACK, py.Rect(50, 410, 100, 40), 3)
            screen.blit(text_font.render('EASY', True, BLACK), (75, 420))
        elif medium:
            py.draw.rect(screen, VIOLET, py.Rect(210, 410, 100, 40))
            py.draw.rect(screen, BLACK, py.Rect(210, 410, 100, 40), 3)
            screen.blit(text_font.render('MEDIUM', True, BLACK), (228, 420))
        elif hard:
            py.draw.rect(screen, VIOLET, py.Rect(370, 410, 100, 40))
            py.draw.rect(screen, BLACK, py.Rect(370, 410, 100, 40), 3)
            screen.blit(text_font.render('HARD', True, BLACK), (398, 420))

        if assist:
            py.draw.rect(screen, VIOLET, py.Rect(130, 515, 100, 40))
            py.draw.rect(screen, BLACK, py.Rect(130, 515, 100, 40), 3)

            screen.blit(text_font.render('On', True, BLACK), (168, 525))
            screen.blit(text_font.render('Off', True, BLACK), (330, 525))
        elif assist == False:
            py.draw.rect(screen, VIOLET, py.Rect(300, 515, 100, 40))
            py.draw.rect(screen, BLACK, py.Rect(300, 515, 100, 40), 3)  

            screen.blit(text_font.render('On', True, BLACK), (168, 525))    
            screen.blit(text_font.render('Off', True, BLACK), (330, 525))

    if info:
        # Load info screen
        game_setup.info_screen(screen, py.mouse.get_pos())
        
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