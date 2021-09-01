#Sudoku Solver 
#By: Shahnur Syed

#Importing libraries
import pygame
import os
import sys
from board_setup import *
from vertify_validness import *
from mode import *
import random
import numpy as np

#Setting clock
fps = 4
fpsclock = pygame.time.Clock()

#Initializing game
pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,600])

#Setup font types to use
text_font = pygame.font.SysFont('Monotype', 18)
num_font = pygame.font.SysFont('Monotype', 20, bold=True)

pygame.mixer.init()
songs = ['foo.mp3', 'oingoboingo.mp3', 'heroscomeback.mp3', 'blackcatcher.mp3', 'jujutsuop1.mp3', 'stardustop.mp3', 'letmehear.mp3', 'touchoff.mp3']
pygame.mixer.music.load(songs[0])
pygame.mixer.music.play()

running = True

pause = resume = backwards = forward = False
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

game_started = info = generate_sol = blurred = back = back_enter = pos = easy = medium = hard = default = mode_diff = enter_board = False
entries_enter = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
invalid_spots = invalid_spots_ent = {}

startup(screen, pygame.mouse.get_pos(), text_font)
assist = None
input_num = 0

#Setting positions for grid
x = y = x1 = y1 = 300

while running:
    for event in pygame.event.get():
        ##QUIT##
        if event.type == pygame.QUIT:
            running = False

        #SONG END
        if event.type == SONG_END:
            songs = songs[1:] + [songs[0]] # move current song to the back of the list
            pygame.mixer.music.load(songs[0])
            pygame.mixer.music.play()

        ##CLICK##
        if event.type == pygame.MOUSEBUTTONUP:
            pos = curr_pos = pygame.mouse.get_pos()
           
            if not game_started and curr_pos[0] >= 215 and curr_pos[0] <= 335:
                #START BUTTON
                if curr_pos[1] >= 130 and curr_pos[1] <= 170 and not enter_board:
                    if back or back_enter: 
                        #EASY
                        if str(mode_diff).isnumeric() and mode_diff == 0:
                            if (str(default).isnumeric() and default == mode_diff):
                                img = pygame.image.load("curr_grid.png")
                                screen.blit(img, (0, 0))
                            else:
                                
                                if easy:
                                    grid = fill_grid(0, 2, 4, 5, 42)
                                if medium:
                                    grid = fill_grid(3, 5, 5, 6, 53)
                                elif hard:
                                    grid = fill_grid(6, 8, 6, 7, 64)    


                                if easy or medium or hard:
                                    screen.fill((255,255,255))
                                    board_setup(screen)

                                    filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))
                                    
                                    solution = solve_puzzle([row[:] for row in grid])
                                    solution_entries = dict(((j*60,i*60), solution[i][j]) for i in range(0,9) for j in range(0,9))
                                    solution_entries = {k: solution_entries[k] if k not in filled_spots else True for k in solution_entries}
                                    entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                                    entries = {k: entries[k] if k not in filled_spots else True for k in entries}
                                    x = y = 300
                                else:
                                    if not assist or (invalid_spots == {}):
                                        img = pygame.image.load("curr_grid.png")
                                        screen.blit(img, (0, 0))

                                        if invalid_spots != {}:
                                            for k in invalid_spots.keys():
                                                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                                screen.blit(num_font.render(str(invalid_spots[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                                  
                                    else:
                                        img = pygame.image.load("curr_grid.png")
                                        screen.blit(img, (0, 0))
                                        
                                        for k in invalid_spots.keys():
                                            pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                            screen.blit(num_font.render(str(invalid_spots[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                                    
                                    easy = True

                                game_started = True
                                info = blurred = back = pos = enter_board = False                    
                                input_num = 0    
                        #MED
                        elif mode_diff == 1:
                            if (str(default).isnumeric() and default == mode_diff):
                                img = pygame.image.load("curr_grid.png")
                                screen.blit(img, (0, 0))
                            else:
                                if easy:
                                    grid = fill_grid(0, 2, 4, 5, 42)
                                #reset when back to startup, if no new mode select return to org otherwise new game
                                if medium:
                                    grid = fill_grid(3, 5, 5, 6, 53)
                                elif hard:
                                    grid = fill_grid(6, 8, 6, 7, 64)

                                if easy or medium or hard:
                                    screen.fill((255,255,255))
                                    board_setup(screen)
                                    filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))
                                    
                                    solution = solve_puzzle([row[:] for row in grid])
                                    solution_entries = dict(((j*60,i*60), solution[i][j]) for i in range(0,9) for j in range(0,9))
                                    solution_entries = {k: solution_entries[k] if k not in filled_spots else True for k in solution_entries}
                                    entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                                    entries = {k: entries[k] if k not in filled_spots else True for k in entries}
                                    x = y = 300
                                else:
                                    if not assist or (invalid_spots == {}):
                                        img = pygame.image.load("curr_grid.png")
                                        screen.blit(img, (0, 0))

                                        if invalid_spots != {}:
                                            for k in invalid_spots.keys():
                                                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                                screen.blit(num_font.render(str(invalid_spots[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                                  
                                    else:
                                        img = pygame.image.load("curr_grid.png")
                                        screen.blit(img, (0, 0))
                                        
                                        for k in invalid_spots.keys():
                                            pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                            screen.blit(num_font.render(str(invalid_spots[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                                    medium = True

                                game_started = True
                                info = blurred = back = back_enter = pos = enter_board = False                    
                                input_num = 0   
                        #HARD
                        elif mode_diff == 2:
                            if (str(default).isnumeric() and default == mode_diff):
                                img = pygame.image.load("curr_grid.png")
                                screen.blit(img, (0, 0))
                            else:
                                if easy:
                                    grid = fill_grid(0, 2, 4, 5, 42)
                                elif medium:
                                    grid = fill_grid(3, 5, 5, 6, 53)
                                elif hard:
                                    grid = fill_grid(6, 8, 6, 7, 64)

                                if easy or medium or hard:
                                    screen.fill((255,255,255))
                                    board_setup(screen)

                                    filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))
                                    
                                    solution = solve_puzzle([row[:] for row in grid])
                                    solution_entries = dict(((j*60,i*60), solution[i][j]) for i in range(0,9) for j in range(0,9))
                                    solution_entries = {k: solution_entries[k] if k not in filled_spots else True for k in solution_entries}
                                    entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                                    entries = {k: entries[k] if k not in filled_spots else True for k in entries}
                                    x = y = 300
                                else:
                                    if not assist or (invalid_spots == {}):
                                        img = pygame.image.load("curr_grid.png")
                                        screen.blit(img, (0, 0))

                                        if invalid_spots != {}:
                                            for k in invalid_spots.keys():
                                                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                                screen.blit(num_font.render(str(invalid_spots[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                                  
                                    else:
                                        img = pygame.image.load("curr_grid.png")
                                        screen.blit(img, (0, 0))
                                        
                                        for k in invalid_spots.keys():
                                            pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                            screen.blit(num_font.render(str(invalid_spots[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                                    hard = True
                                    
                                    
                                game_started = True
                                info = blurred = back = back_enter = pos = enter_board = False                    
                                input_num = 0   
                        #DEFAULT
                        else:
                            screen.fill((255,255,255))
                            board_setup(screen)

                            if easy:
                                grid = fill_grid(0, 2, 4, 5, 42)
                            elif medium:
                                grid = fill_grid(3, 5, 5, 6, 53)
                            elif hard: 
                                grid = fill_grid(6, 8, 6, 7, 64)
                            else:
                                choices = [mode.EASY, mode.MEDIUM, mode.HARD]
                                default = random.choice(choices)

                                if default == mode.EASY:
                                    grid = fill_grid(0, 2, 4, 5, 42)
                                elif default == mode.MEDIUM:
                                    grid = fill_grid(3, 5, 5, 6, 53)
                                else:
                                    grid = fill_grid(6, 8, 6, 7, 64)

                            filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))
                            
                            solution = solve_puzzle([row[:] for row in grid])
                            solution_entries = dict(((j*60,i*60), solution[i][j]) for i in range(0,9) for j in range(0,9))
                            solution_entries = {k: solution_entries[k] if k not in filled_spots else True for k in solution_entries}
                            entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                            entries = {k: entries[k] if k not in filled_spots else True for k in entries}
                            x = y = 300
                    else:
                        screen.fill((255,255,255))
                        board_setup(screen)

                        if easy:
                            grid = fill_grid(0, 2, 4, 5, 42)
                        elif medium:
                            grid = fill_grid(3, 5, 5, 6, 53)
                        elif hard: 
                            grid = fill_grid(6, 8, 6, 7, 64)
                        else:
                            choices = [mode.EASY, mode.MEDIUM, mode.HARD]
                            default = random.choice(choices)

                            if default == mode.EASY:
                                grid = fill_grid(0, 2, 4, 5, 42)
                            elif default == mode.MEDIUM:
                                grid = fill_grid(3, 5, 5, 6, 53)
                            else:
                                grid = fill_grid(6, 8, 6, 7, 64)
                        filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))
                        
                        solution = solve_puzzle([row[:] for row in grid])
                        solution_entries = dict(((j*60,i*60), solution[i][j]) for i in range(0,9) for j in range(0,9))
                        solution_entries = {k: solution_entries[k] if k not in filled_spots else True for k in solution_entries}
                        entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                        entries = {k: entries[k] if k not in filled_spots else True for k in entries}
                        x = y = 300
                        invalid_spots = {}
                    
                    game_started = True
                    info = blurred = back = back_enter = pos = enter_board = False                    
                    input_num = 0
                #INFO BUTTON
                elif curr_pos[1] >= 200 and curr_pos[1] <= 240 and not enter_board:
                    info = True
                    game_started = back = back_enter = False
                #ENTER BUTTON
                elif curr_pos[1] >= 270 and curr_pos[1] <= 310 and not enter_board:
                    if all(x == 0 or x == True for x in entries_enter.values()) == False:
                        if not assist or (invalid_spots_ent == {}):
                            img = pygame.image.load("curr_grid_enter.png")
                            screen.blit(img, (0, 0))

                            if invalid_spots_ent != {}:
                                for k in invalid_spots_ent.keys():
                                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                    screen.blit(num_font.render(str(invalid_spots_ent[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                        
                        else:
                            img = pygame.image.load("curr_grid_enter.png")
                            screen.blit(img, (0, 0))
                            
                            for k in invalid_spots_ent.keys():
                                pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(k[0]+3,k[1]+3, 56, 56))
                                screen.blit(num_font.render(str(invalid_spots_ent[k]) , True , (255,0,0)), (25+k[0], 25+k[1]))
                    else:
                        entries_enter = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                        screen.fill((255,255,255))
                        board_setup(screen)
                        invalid_spots_ent = {}
                    
                    enter_board = True
                    info = back = back_enter = False
                    
            #BACK BUTTON IN INFO SCREEN (info selected and back selected)
            if curr_pos[0]>=420 and curr_pos[0]<=520 and curr_pos[1]>=550 and curr_pos[1]<=580 and info:
                info = False
                back = True

            ###Started game buttons###
            if curr_pos[1] >= 550 and curr_pos[1] <= 590 and game_started:
                ##NEW GAME BUTTON
                if curr_pos[0] >=30 and curr_pos[0]<=130:
                    generate_sol = blurred = False
                    invalid_spots = {}

                    x = y = 300
                    input_num = 0
                    
                    screen.fill((255,255,255))
                    board_setup(screen)
        
                    if easy or (str(default).isnumeric() and default == 0):
                        grid = fill_grid(0, 2, 4, 5, 42)
                    elif medium or default == 1:
                        grid = fill_grid(3, 5, 5, 6, 53)
                    elif hard or default == 2: 
                        grid = fill_grid(6, 8, 6, 7, 64)
 
                    solution = solve_puzzle([row[:] for row in grid])
                    filled_spots = fill_board(None, grid, screen, num_font, (0,0,0))
                    solution_entries = dict(((j*60,i*60), solution[i][j]) for i in range(0,9) for j in range(0,9))
                    solution_entries = {k: solution_entries[k] if k not in filled_spots else True for k in solution_entries}
                    entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
                    entries = {k: entries[k] if k not in filled_spots else True for k in entries}

                ##GENERATE SOLUTION BUTTON
                elif curr_pos[0] >=160 and curr_pos[0]<=260:
                    #Gen_sol already clicked
                    if generate_sol:
                        screen.fill((255, 255, 255))
                        board_setup(screen)
                   
                    screen.fill((255, 255, 255))
                    board_setup(screen)
                    fill_board(solution, grid, screen, num_font, (255,0,0))
                    entries = {k: solution_entries[k] for k in entries}

                    generate_sol = True
               
                ##VERIFY BUTTON
                elif curr_pos[0] >=290 and curr_pos[0]<=390:
                    pygame.image.save(screen, "curr_grid.png")
                    entered_vals = [[entries[(i*60, j*60)] if str(entries[(i*60, j*60)]).isnumeric() else solution[j][i] for i in range(9)] for j in range(9)]
    
                    if solution_entries == entries or verify_validness(entered_vals):
                        valid_sol = True
                    else:
                        valid_sol = False

                    if not blurred:
                        blur_image(screen)
                        blurred = True

                    message_button(screen)

                    if valid_sol:
                        screen.blit(pygame.font.SysFont('Monotype', 25).render("You Win!" , True , (0,0,0)) , (220, 170))
                    else:
                        screen.blit(pygame.font.SysFont('Monotype', 25).render("Try Again!" , True , (0,0,0)) , (200, 170))

                #BACK BUTTON
                elif curr_pos[0] >=420 and curr_pos[0]<=520 and not info and game_started:
                    pygame.image.save(screen, "curr_grid.png")
                    back = True
                    game_started = blurred  = False

                    if easy:
                        mode_diff = mode.EASY
                    elif medium:
                        mode_diff = mode.MEDIUM
                    elif hard:
                        mode_diff = mode.HARD
                    else:
                        mode_diff = default
                    easy = medium = hard = False

            #ENTER OPT BUTTONS
            if curr_pos[1] >= 550 and curr_pos[1] <= 590 and enter_board: 
                pygame.image.save(screen, "curr_grid_enter.png")

                #CHECK
                if curr_pos[0] >= 220 and curr_pos[0] <= 320:

                    entered_vals = [[entries_enter[(i*60, j*60)] if str(entries_enter[(i*60, j*60)]).isnumeric() else solution[j][i] for i in range(9)] for j in range(9)]

                    if verify_validness(entered_vals):
                        valid_sol = True
                    else:
                        valid_sol = False

                    if not blurred:
                        blur_image(screen)
                        blurred = True

                    message_button(screen)

                    if valid_sol:
                        screen.blit(pygame.font.SysFont('Monotype', 25).render("Valid Solution" , True , (0,0,0)) , (165, 175))
                    else:
                        screen.blit(pygame.font.SysFont('Monotype', 25).render("Invalid Solution" , True , (0,0,0)) , (155, 175))
                #BACK
                elif curr_pos[0] >= 420 and curr_pos[0] <= 520:
                    enter_board = False
                    back_enter = True

            #Verify clicked, blurring
            if not (curr_pos[1] >= 550 and curr_pos[1] <= 590) and blurred:
                if enter_board:
                    img = pygame.image.load("curr_grid_enter.png")
                else:
                    img = pygame.image.load("curr_grid.png")
                screen.blit(img, (0, 0))
                blurred = pos = False

            #MODES
            if not game_started and curr_pos[1] >= 410 and curr_pos[1] <= 450:
                if curr_pos[0] >= 50 and curr_pos[0] <=150:
                    if easy:
                        easy = False
                    else:
                        easy = True
                    medium = hard = default = False
                elif curr_pos[0] >= 210 and curr_pos[0] <=310:
                    if medium:
                        medium = False
                    else:
                        medium = True
                    easy = hard = default = False
                elif curr_pos[0] >= 370 and curr_pos[0] <=470:
                    if hard:
                        hard = False
                    else:
                        hard = True
                    easy = medium = default = False
    
            #ASSIST MODE
            if curr_pos[1] >= 515 and curr_pos[1] <= 555 and not game_started:
                if curr_pos[0] >= 130 and curr_pos[0] <= 230:
                    assist = True
                
                if curr_pos[0] >= 300 and curr_pos[0] <= 400:
                    assist = False      

        ##ENTERING NUM OR DEL OR BACKSPACE##
        if event.type == pygame.KEYDOWN:
            input_num = event.unicode
            
            if event.key == pygame.K_p:
                if resume:
                    resume = False
                    pause = True
            
                else:
                    resume = True
                    pause = False
                    
            if event.key == pygame.K_b:
                backwards = True

            if event.key == pygame.K_f:
                forward = True

            #BACKSPACE KEY
            if event.key == pygame.K_BACKSPACE:
                if assist:
                    #get prev entry
                    prev = entries[(x,y)]


                if game_started:
                    if str(entries[(x,y)]).isnumeric():
                        #used to erase but think u could prob remove and just re-order
                        pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                        entries[(x,y)] = 0
                        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

                        if assist:      
                            vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in grid_indices] for col in grid_indices]
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
                                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                                        else:
                                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,(ind[0][0]*60)+3, 56, 56))
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
                                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                                        else:
                                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect((ind[0][0]*60)+3,y+3, 56, 56))
                                        screen.blit(num_font.render(str(entries[(ind[0][0]*60), y]) , True , (255,0,0)), (25+(ind[0][0]*60), 25+y))
                        
                        if (x,y) in invalid_spots.keys():
                            del invalid_spots[(x,y)]

                elif enter_board:
                        if str(entries_enter[(x1,y1)]).isnumeric():
                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                            entries_enter[(x1,y1)] = 0
                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))

                        if (x1,y1) in invalid_spots_ent.keys():
                            del invalid_spots_ent[(x1,y1)]

            #DEL KEY
            if event.key == pygame.K_DELETE:
                screen.fill((255,255,255))
                board_setup(screen)
                entries = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)
    
                if not enter_board:
                    entries = {k: entries[k] if k not in filled_spots else True for k in entries}
                    generate_sol = blurred = False
                    invalid_spots = {}
                else:
                    grid = np.reshape(list(entries.values()), (9, 9))
                    entries_enter = dict.fromkeys([(y*60,x*60) for x in range(0,9) for y in range(0,9)], 0)

                    invalid_spots_ent = {}
                fill_board(None, grid, screen, num_font, (0,0,0))
   
    ##EMPTY BOARD FOR INPUT
    if enter_board:
        mouse = pygame.mouse.get_pos()
        if mouse[1] >= 550 and mouse[1] <= 590:
            if mouse[0] >= 220 and mouse[0] <= 320:
                pygame.draw.rect(screen, (255,204,255), pygame.Rect(220, 550, 100, 40))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(220, 550, 100, 40), 3)

                pygame.draw.rect(screen, (192,192,192), pygame.Rect(420, 550, 100, 40))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)
            elif mouse[0] >= 420 and mouse[0] <= 520:
                pygame.draw.rect(screen, (192,192,192), pygame.Rect(220, 550, 100, 40))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(220, 550, 100, 40), 3)

                pygame.draw.rect(screen, (255,204,255), pygame.Rect(420, 550, 100, 40))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)
            else:
                pygame.draw.rect(screen, (192,192,192), pygame.Rect(220, 550, 100, 40))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(220, 550, 100, 40), 3)

                pygame.draw.rect(screen, (192,192,192), pygame.Rect(420, 550, 100, 40))
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)
        else:
            pygame.draw.rect(screen, (192,192,192), pygame.Rect(220, 550, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(220, 550, 100, 40), 3)

            pygame.draw.rect(screen, (192,192,192), pygame.Rect(420, 550, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)

        screen.blit(pygame.font.SysFont('Monotype', 15).render('Check' , True , (0,0,0)) , (245, 560))
        screen.blit(pygame.font.SysFont('Monotype', 15).render('Back' , True , (0,0,0)) , (450, 560))

    ##CHECKING FOR BUTTON EVENTS
    if game_started:
        #Get highlight feature to work without making buttons everytime
        game_started_button_setup(screen, pygame.mouse.get_pos())  

         #Checking which keys are being pressed (used for holding feature)
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            if not generate_sol:
                #Erase previous empty square
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56)) 
                #Advance in given dir
                x = set_x(x, -60)
                #Highlight new pos
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
            else:
                
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
                
                x = set_x(x, -60)

                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                if str(solution_entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

        if keys_pressed[pygame.K_RIGHT]:
            if not generate_sol:
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                x = set_x(x, 60)
                
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
            else:
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
                
                x = set_x(x, 60)

                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                if str(solution_entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

        if keys_pressed[pygame.K_UP]:
            if not generate_sol:
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                y = set_y(y, x, -60, screen, entries)
                
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
            else:
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
               
                y = set_y(y, x, -60, screen, entries)

                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                if str(solution_entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

        if keys_pressed[pygame.K_DOWN]:
            if not generate_sol:
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                y = set_y(y, x, 60, screen, entries)
                
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
            else:
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))

                if str(entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))
                
                y = set_y(y, x, 60, screen, entries)
                if entries[(x,y)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
                
                if str(solution_entries[(x,y)]).isnumeric() and entries[(x,y)] == solution_entries[(x,y)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
    
        #Click pos
        if (pos and not(pos[1] >= 550 and pos[1] <= 590) and str(entries[get_range(pos[0]), get_range(pos[1])]).isnumeric()):
            if assist and str(entries[((get_range(pos[0]), get_range(pos[1])))]).isnumeric() and entries[((get_range(pos[0]), get_range(pos[1])))] != 0:
                vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in grid_indices] for col in grid_indices]
                sq_x_init = 3*round((int(get_range(pos[0])/60)-1)/3)
                sq_y_init = 3*round((int(get_range(pos[1])/60)-1)/3)
                np_grid = np.array(vals) 
                square = np.reshape(vals, (9, 9))[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                num = entries[((get_range(pos[0]), get_range(pos[1])))]
                
                if (np.count_nonzero(np_grid[int(get_range(pos[1])/60),:] == num) > 1 or
                    np.count_nonzero(np_grid[:,int(get_range(pos[0])/60)] == num) > 1
                    or np.count_nonzero(square == num) > 1):  
                        pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))
                else:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))
            else:    
                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))

            #Before gen sol 
            if entries[(x,y)] == 0 and not ((get_range(pos[0]), get_range(pos[1])) == (x,y)):
                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))

            if generate_sol and  entries[(x,y)] == solution_entries[(x,y)] and str(entries[(x,y)]).isnumeric():
                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))

            (x,y) = (get_range(pos[0]), get_range(pos[1]))
            
            if str(entries[(x,y)]).isnumeric() and entries[(x,y)]!= 0:
                screen.blit(num_font.render(str(entries[(x,y)]), True , (255,0,0)), (25+x, 25+y))

        #Enter input
        if str(input_num).isnumeric() and int(input_num) >= 1 and int(input_num) <= 9 and str(entries[(x,y)]).isnumeric():
                curr_pos = pygame.mouse.get_pos()

                #del need to re-highlight
                if sum(x == True for x in entries.values()) == len(filled_spots):
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))

                #Spot is used (need to re-highlight)
                if (entries[(x,y)] != 0) or ((get_range(curr_pos[0]), get_range(curr_pos[1])) == (x,y)): 
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
                

                #Checking if assist is on
                if assist:
                    
                    #get prev entry
                    prev = entries[(x,y)]

                    entries[(x,y)] = int(input_num)
          
                    vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in grid_indices] for col in grid_indices]
                    np_grid = np.array(vals) 
                    sq_x_init = 3*round((int(x/60)-1)/3)
                    sq_y_init = 3*round((int(y/60)-1)/3)
                    square = np_grid[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                    num = int(input_num)
                
                    if (np.count_nonzero(np_grid[:,int(x/60)] == num) > 1 or
                        np.count_nonzero(np_grid[int(y/60),:] == num) > 1
                        or np.count_nonzero(square == num) > 1):
                        invalid_spots[(x,y)] = num
                        pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(x+3,y+3, 56, 56))
                    else:
                        if (x,y) in invalid_spots.keys():
                            del invalid_spots[(x,y)] 
                        if generate_sol:
                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                        else:
                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,y+3, 56, 56))
                             
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
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                                else:
                                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x+3,(ind[0][0]*60)+3, 56, 56))
                             
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
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                                else:
                                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect((ind[0][0]*60)+3,y+3, 56, 56))
                         
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
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x+3,y+3, 56, 56))
                                else:
                                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(((ind[1][0]+sq_x_init)*60)+3,((ind[0][0]+sq_y_init)*60)+3, 56, 56))

                                screen.blit(num_font.render(str(entries[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]) , True , (255,0,0)), (25+((ind[1][0]+sq_x_init)*60), 25+((ind[0][0]+sq_y_init)*60)))
                            #ind[0][0]+sq_y_init, ind[1][0]+sq_x_init
                else:
                    #Update entry for pos and display
                    prev = entries[(x,y)]
                    
                    entries[(x,y)] = int(input_num)   
                    
                    num = int(input_num)

                    vals = [[grid[col][row] if grid[col][row] != 0 else entries[(row*60, col*60)] for row in grid_indices] for col in grid_indices]
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
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            if not generate_sol:
                #Erase previous empty square
                if entries_enter[(x1,y1)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56)) 
                #Advance in given dir
                x1 = set_x(x1, -60)
                #Highlight new pos
                if entries_enter[(x1,y1)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))
            else:
                if str(entries_enter[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)] == solution_entries[(x1,y1)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                    screen.blit(num_font.render(str(entries_enter[(x1,y1)]), True , (255,0,0)), (25+x1, 25+y1))
                
                x1 = set_x(x1, -60)
                
                if str(solution_entries[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)] == solution_entries[(x1,y1)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))

        if keys_pressed[pygame.K_RIGHT]:
            if not generate_sol:
                if entries_enter[(x1,y1)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                
                x1 = set_x(x1, 60)
                
                if entries_enter[(x1,y1)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))
            else:
                if str(entries_enter[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)] == solution_entries[(x1,y1)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                    screen.blit(num_font.render(str(entries[(x1,y1)]), True , (255,0,0)), (25+x1, 25+y1))
                
                x1 = set_x(x1, 60)
                
                if str(solution_entries[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)] == solution_entries[(x1,y1)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))

        if keys_pressed[pygame.K_UP]:
            if entries_enter[(x1,y1)] == 0:
                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
            
            y1 = set_y(y1, x1, -60, screen, entries_enter)
            
            if entries_enter[(x1,y1)] == 0:
                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))

        if keys_pressed[pygame.K_DOWN]:
            if not generate_sol:
                if entries_enter[(x1,y1)] == 0:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                
                y1 = set_y(y1, x1, 60, screen, entries_enter)
                
                if entries_enter[(x1,y1)] == 0:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))
            else:
                if str(entries_enter[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)] == solution_entries[(x1,y1)]:
                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                    screen.blit(num_font.render(str(entries_enter[(x1,y1)]), True , (255,0,0)), (25+x1, 25+y1))
                
                y1 = set_y(y1, x1, 60, screen, entries_enter)
                
                if str(solution_entries[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)] == solution_entries[(x1,y1)]:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))
    
        if (pos and not(pos[1] >= 550 and pos[1] <= 590) and str(entries_enter[get_range(pos[0]), get_range(pos[1])]).isnumeric()):
            
            if assist and str(entries_enter[((get_range(pos[0]), get_range(pos[1])))]).isnumeric() and entries_enter[((get_range(pos[0]), get_range(pos[1])))] != 0:
                entered_vals = [[entries_enter[(i*60, j*60)] if str(entries_enter[(i*60, j*60)]).isnumeric() else solution[j][i] for i in range(9)] for j in range(9)]
                
                sq_x_init = 3*round((int(get_range(pos[0])/60)-1)/3)
                sq_y_init = 3*round((int(get_range(pos[1])/60)-1)/3)
                np_grid = np.array(entered_vals) 
                square = np.reshape(entered_vals, (9, 9))[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                num = entries_enter[((get_range(pos[0]), get_range(pos[1])))]
                
                if (np.count_nonzero(np_grid[int(get_range(pos[1])/60),:] == num) > 1 or
                    np.count_nonzero(np_grid[:,int(get_range(pos[0])/60)] == num) > 1
                    or np.count_nonzero(square == num) > 1):  
                        pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))
                else:
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))
            else:    
                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))

            
            #pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(pos[0])+3,get_range(pos[1])+3, 56, 56))
     
            #click
            if entries_enter[(x1,y1)] == 0 and not ((get_range(pos[0]), get_range(pos[1])) == (x1,y1)):
                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))

            (x1,y1) = (get_range(pos[0]), get_range(pos[1]))
            
            if str(entries_enter[(x1,y1)]).isnumeric() and entries_enter[(x1,y1)]!= 0:
                screen.blit(num_font.render(str(entries_enter[(x1,y1)]), True , (255,0,0)), (25+x1, 25+y1))

          #Enter input
        
        if str(input_num).isnumeric() and int(input_num) >= 1 and int(input_num) <= 9 and str(entries_enter[(x1,y1)]).isnumeric():
                curr_pos = pygame.mouse.get_pos()
                
                #Spot is used (need to re-highlight)
                if (entries_enter[(x1,y1)] != 0) or ((get_range(curr_pos[0]), get_range(curr_pos[1])) == (x1,y1)):
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                
                #Checking if assist is on
                if assist:
                    
                    #get prev entry
                    prev = entries_enter[(x1,y1)]
         
                    entries_enter[(x1,y1)] = int(input_num)
                    
                    
                    entered_vals = [[entries_enter[(i*60, j*60)] if str(entries_enter[(i*60, j*60)]).isnumeric() else 0 for i in range(9)] for j in range(9)]
                    np_grid = np.array(entered_vals) 
                    sq_x_init = 3*round((int(x1/60)-1)/3)
                    sq_y_init = 3*round((int(y1/60)-1)/3)
                    square = np_grid[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3]

                    num = int(input_num)
            
                    if (np.count_nonzero(np_grid[:,int(x1/60)] == num) > 1 or
                        np.count_nonzero(np_grid[int(y1/60),:] == num) > 1
                        or np.count_nonzero(square == num) > 1):
                        invalid_spots_ent[(x1,y1)] = num  
                        pygame.draw.rect(screen,(255, 255, 204), pygame.Rect(x1+3,y1+3, 56, 56))
                    else:
                        if (x1,y1) in invalid_spots_ent.keys():
                            del invalid_spots_ent[(x1,y1)] 
                        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                             
                    col_count = np.count_nonzero(np_grid[:,int(x1/60)] == prev)
                    row_count = np.count_nonzero(np_grid[int(y1/60),:] == prev)
                    sq_count = np.count_nonzero(square == prev)
                           
                    #COL
                    if (col_count == 1):
                        ind = np.where((np_grid[:,int(x1/60)]) == prev)

                        if str(entries_enter[x1,(ind[0][0]*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            t = np_grid[3*round((int(x1/60)-1)/3):(3*round((int(x1/60)-1)/3)+3), 3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3]
                            if (not np.count_nonzero(np_grid[ind[0][0],:] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (y1 != ind[0][0]*60):
                                if (x1,(ind[0][0]*60)) in invalid_spots_ent.keys():
                                    del invalid_spots_ent[(x1,(ind[0][0]*60))]   
                                  
                                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(x1+3,(ind[0][0]*60)+3, 56, 56))
                                screen.blit(num_font.render(str(entries[x1, (ind[0][0]*60)]) , True , (255,0,0)), (25+x1, 25+((ind[0][0]*60))))

                    #ROW
                    if (row_count == 1):
                        ind = np.where((np_grid[int(y1/60),:]) == prev)

                        if str(entries_enter[(ind[0][0]*60),y1]).isnumeric() and str(prev).isnumeric() and prev != 0:
                           
                            t = np_grid[3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3, 3*round((int(y1/60)-1)/3):(3*round((int(y1/60)-1)/3)+3)]
                           
                            if (not np.count_nonzero(np_grid[:,ind[0][0]] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (x1 != ind[0][0]*60):
                                if ((ind[0][0]*60),y1) in invalid_spots_ent.keys():
                                    del invalid_spots[((ind[0][0]*60),y1)]
                                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect((ind[0][0]*60)+3,y1+3, 56, 56))
                                screen.blit(num_font.render(str(entries[(ind[0][0]*60), y1]) , True , (255,0,0)), (25+(ind[0][0]*60), 25+y1))

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
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(x1+3,y1+3, 56, 56))
                                else:
                                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(((ind[1][0]+sq_x_init)*60)+3,((ind[0][0]+sq_y_init)*60)+3, 56, 56))

                                screen.blit(num_font.render(str(entries[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]) , True , (255,0,0)), (25+((ind[1][0]+sq_x_init)*60), 25+((ind[0][0]+sq_y_init)*60)))
                else:
                    #Update entry for pos and display
                    prev = entries_enter[(x1,y1)]

                    entries_enter[(x1,y1)] = int(input_num)
                    
                    num = int(input_num)

                    entered_vals = [[entries_enter[(i*60, j*60)] if str(entries_enter[(i*60, j*60)]).isnumeric() else 0 for i in range(9)] for j in range(9)]

                    np_grid = np.array(entered_vals) 
                    sq_x_init = 3*round((int(x1/60)-1)/3)
                    sq_y_init = 3*round((int(y1/60)-1)/3)
                    square = np_grid[sq_y_init:sq_y_init+3, sq_x_init:sq_x_init+3] 

                    if (np.count_nonzero(np_grid[:,int(x1/60)] == num) > 1 or
                        np.count_nonzero(np_grid[int(y1/60),:] == num) > 1
                        or np.count_nonzero(square == num) > 1):  
                        invalid_spots_ent[(x1,y1)] = num
                    else:
                        if (x,y) in invalid_spots_ent.keys():
                            del invalid_spots_ent[(x1,y1)] 
                    col_count = np.count_nonzero(np_grid[:,int(x1/60)] == prev)
                    row_count = np.count_nonzero(np_grid[int(y1/60),:] == prev)
                    sq_count = np.count_nonzero(square == prev)
            
                    #COL
                    if (col_count == 1):
                        ind = np.where((np_grid[:,int(x1/60)]) == prev)

                        if str(entries_enter[x,(ind[0][0]*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            t = np_grid[3*round((int(x/60)-1)/3):(3*round((int(x/60)-1)/3)+3), 3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3]
                            if (not np.count_nonzero(np_grid[ind[0][0],:] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (y1 != ind[0][0]*60): 
                                del invalid_spots_ent[(x1,(ind[0][0]*60))] 

                    #ROW
                    if (row_count == 1):
                        ind = np.where((np_grid[int(y/60),:]) == prev)

                        if str(entries_enter[(ind[0][0]*60),y1]).isnumeric() and str(prev).isnumeric() and prev != 0:
                           
                            t = np_grid[3*round((ind[0][0]-1)/3):3*round((ind[0][0]-1)/3)+3, 3*round((int(y1/60)-1)/3):(3*round((int(y1/60)-1)/3)+3)]
                           
                            if (not np.count_nonzero(np_grid[:,ind[0][0]] == prev) > 1 and 
                                not np.count_nonzero(t == prev) > 1) and (x1 != ind[0][0]*60):
                                del invalid_spots[((ind[0][0]*60),y1)]

                    #SQ
                    if (sq_count == 1):
                        ind = np.where(square == prev)
                        
                        if str(entries[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]).isnumeric() and str(prev).isnumeric() and prev != 0:
                            if (not np.count_nonzero(np_grid[:,ind[0][0]+sq_y_init] == prev) > 1 and 
                                not np.count_nonzero(np_grid[ind[1][0]+sq_x_init,:] == prev) > 1 and 
                                (x,y) != ((ind[1][0]+sq_x_init)*60, (ind[0][0]+sq_y_init)*60)):
                                if ((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60) in invalid_spots.keys():
                                    del invalid_spots[((ind[1][0]+sq_x_init)*60,(ind[0][0]+sq_y_init)*60)]  

                screen.blit(num_font.render(input_num , True , (255,0,0)), (25+x1, 25+y1))
                
                #Reset
                input_num = 0
        pos = False
    else:
        startup(screen, pygame.mouse.get_pos(), text_font)
        
        if easy:
            pygame.draw.rect(screen, (255,204,255), pygame.Rect(50, 410, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(50, 410, 100, 40), 3)
            screen.blit(text_font.render('EASY' , True , (0,0,0)) , (75, 420))
        elif medium:
            pygame.draw.rect(screen, (255,204,255), pygame.Rect(210, 410, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(210, 410, 100, 40), 3)
            screen.blit(text_font.render('MEDIUM' , True , (0,0,0)) , (228, 420))
        elif hard:
            pygame.draw.rect(screen, (255,204,255), pygame.Rect(370, 410, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(370, 410, 100, 40), 3)
            screen.blit(text_font.render('HARD' , True , (0,0,0)) , (398, 420))

        if assist:
            pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(130, 515, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(130, 515, 100, 40), 3)

            screen.blit(text_font.render('On' , True , (0,0,0)) , (168, 525))
            screen.blit(text_font.render('Off' , True , (0,0,0)) , (330, 525))
        elif assist == False:
            pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(300, 515, 100, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(300, 515, 100, 40), 3)  

            screen.blit(text_font.render('On' , True , (0,0,0)) , (168, 525))    
            screen.blit(text_font.render('Off' , True , (0,0,0)) , (330, 525))

        game_started = False

    #Load info screen
    if info:
        screen.fill((204,255,255))
        if pygame.mouse.get_pos()[0]>=420 and pygame.mouse.get_pos()[0]<=520 and pygame.mouse.get_pos()[1]>=550 and pygame.mouse.get_pos()[1]<=580:
            back_button_hover(screen)
        else:
            back_button(screen)
        screen.blit(pygame.font.SysFont('Monotype', 15).render('Back' , True , (0,0,0)) , (450, 555))

        #for i,line in enumerate(get_instructions()):
            #screen.blit(pygame.font.SysFont('Monotype', 15).render(line , True , (0,0,0)) , (30, 30+(i*25)))

    if back:
        startup(screen, pygame.mouse.get_pos(), text_font)
        click_mode(screen, text_font, easy, medium, hard) 

    if pause:
        pygame.mixer.music.pause()
    
    if resume:
        pygame.mixer.music.unpause()
    
    if backwards:
        songs = [songs[len(songs)-1]] + songs[:len(songs)-1]
        pygame.mixer.music.load(songs[0])
        pygame.mixer.music.play()
        backwards = False

    if forward:
        songs = songs[1:] + [songs[0]] # move current song to the back of the list
        pygame.mixer.music.load(songs[0])
        pygame.mixer.music.play()
        forward = False

    #Display
    pygame.display.flip()
    fpsclock.tick(fps)
    
#Removing screenshot as its not needed anymore
if os.path.exists("curr_grid.png"): 
    os.remove("curr_grid.png")
if os.path.exists("BlurImage.jpg"):
    os.remove("BlurImage.jpg")
if os.path.exists("curr_grid_enter.png"): 
    os.remove("curr_grid_enter.png")

pygame.quit()


#clean up code (STYLE)
#figure out dll load import numpy pyinstaller 
#sort music into folders
#create test files
#push into github and done


#------------
#enter board should be an input, then has a solve button instead 