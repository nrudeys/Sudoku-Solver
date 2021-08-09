#Sudoku Solver 
#By: Shahnur Syed

#Importing libraries
import pygame 
from vertify_validness import *
from board_setup import *
from tkinter import *
from tkinter import messagebox
import os

#Initializing game
pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,600])

#Setup font types to use
text_font = pygame.font.SysFont('Monotype', 18)
num_font = pygame.font.SysFont('Monotype', 20, bold=True)

#FLAGS
running = True
started = False
gen_sol = False
info = False
back = False
verify = False
blurred = False
moved_mouse = True
up_arr = False

#Initializing variables to be empty
mouse = ()
grid = []
grid_copy = []
last_key_loc = ()
solved_puzzle = []
prev = ()

while running: 
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEMOTION:
            moved_mouse = True
            
        if event.type == pygame.MOUSEBUTTONDOWN:

            ###Checking if start or info button is clicked###
            if mouse[0] >= 215 and mouse[0] <= 335:    
                #START BUTTON
                if mouse[1] >= 180 and mouse[1] <= 220 and not started:
                    screen.fill((255, 255, 255))

                    #Setting up board
                    board_setup(screen)
                    
                    #Generating a incomplete puzzle and filling the board with those values
                    grid = fill_grid()
                    used_locations = fill_board(None, grid, screen, num_font, (0,0,0))
                    used_locations_mod = [row[:] for row in used_locations]   
                    grid_copy = [row[:] for row in grid]

                    #Updating flags (game started, info and back not clicked)
                    started = True
                    back = False
                    info = False
                    blurred = False
                    verify=False
                    last_key_loc = ()

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
                    used_locations_mod = [row[:] for row in used_locations]   
                    grid_copy = [row[:] for row in grid]

                    verify=False
                    gen_sol = False
                    last_key_loc = ()
                    solved_puzzle = []
                  
                ##GENERATE SOLUTION BUTTON
                elif mouse[0] >=160 and mouse[0]<=260:
                    #Gen_sol already clicked
                    if gen_sol:
                        screen.fill((255, 255, 255))
                        board_setup(screen)
                        fill_board(None, grid, screen, num_font, (0,0,0))
                    gen_sol = True

                    
                    #No changes made or puzzle solved
                    if grid_copy == grid or solved_puzzle == grid_copy:
                        if verify:
                            #Remove diff
                            screen.fill((255,255,255))
                            
                            board_setup(screen)
                            verify = False
                            blurred=False
                        solved_puzzle = solve_puzzle([row[:] for row in grid_copy])
                        grid_copy = [row[:] for row in solved_puzzle]
                        fill_board(solved_puzzle, grid, screen, num_font, (255,0,0))
                        used_locations_mod = [row[:] for row in used_locations]   
                    else:
                        
                        #Remove diff 
                        screen.fill((255,255,255))
                        board_setup(screen)

                        verify=False
                        blurred=False

                        #Reset
                        grid_copy = [row[:] for row in grid]
                        solved_puzzle = solve_puzzle([row[:] for row in grid])
                        fill_board(solved_puzzle, grid, screen, num_font, (255,0,0))
                        used_locations_mod = [row[:] for row in used_locations]

                ##VERIFY SOLUTION BUTTON
                elif mouse[0] >=290 and mouse[0]<=390:
                    verify = True
                  

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
                screen.fill((255,255,255))
                image = pygame.image.load("current_grid.jpeg").convert_alpha()
                screen.blit(image, (0, 0))
                
                verify = False
                blurred = False

        #ENTERING NUMS FOR VERIFY
        if event.type == pygame.KEYDOWN:
            input_num = event.unicode    
            
            #Getting mouse position
            mouse = pygame.mouse.get_pos()

            #Indices
            if input_num.isnumeric() and int(input_num) >= 1 and int(input_num) <= 9:
                if moved_mouse:
                    if  not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations):
                        #No entry entered  
                        if last_key_loc != () and grid_copy[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)] == 0:
                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                            if prev == ():
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                screen.blit(num_font.render(str(solved_puzzle[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)]) , True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                            
                        
                        if prev != () and solved_puzzle != [] and last_key_loc != ():
                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                            screen.blit(num_font.render(str(solved_puzzle[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)]) , True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                            prev = ()
                        highlight_cell(screen, mouse, grid)
                        screen.blit(num_font.render(input_num , True , (255,0,0)) , (25+get_range(mouse[0]), (25+get_range(mouse[1]))))
                        grid_copy[int(get_range(mouse[1])/60)][int(get_range(mouse[0])/60)] = int(input_num)
                        used_locations_mod[int(get_range(mouse[1])/60)].append((get_range(mouse[0]), get_range(mouse[1]))) 
                        
                        last_key_loc = mouse
                else:
                    if not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations):
                        if solved_puzzle ==[]:
                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                            screen.blit(num_font.render(input_num , True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                            grid_copy[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)] = int(input_num)

                            used_locations_mod[int(get_range(last_key_loc[1])/60)].append((get_range(last_key_loc[0]), get_range(last_key_loc[1])))
                            prev = ()
                        else:
                            if any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod):
                                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))

                            screen.blit(num_font.render(input_num , True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                            grid_copy[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)] = int(input_num)
                            used_locations_mod[int(get_range(last_key_loc[1])/60)].append((get_range(last_key_loc[0]), get_range(last_key_loc[1])))
                            prev = ()
            else:
                prev = last_key_loc

            if event.key == pygame.K_DELETE:
                screen.fill((255,255,255))
                board_setup(screen)
                fill_board(None, grid, screen, num_font, (0,0,0))
                grid_copy = [row[:] for row in grid]
                used_locations_mod = [row[:] for row in used_locations]
                prev = ()
                last_key_loc = ()

                verify = False
                blurred = False
                moved_mouse = True
                gen_sol = False

            if event.key == pygame.K_BACKSPACE:
                if moved_mouse:
                    if not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations):
                        unhighlight_cell(screen, mouse, grid)
                        
                        if grid_copy[int(get_range(mouse[1])/60)][int(get_range(mouse[0])/60)] != 0:
                            used_locations_mod[int(get_range(mouse[1])/60)].remove((int(get_range(mouse[0])), int(get_range(mouse[1]))))
                        grid_copy[int(get_range(mouse[1])/60)][int(get_range(mouse[0])/60)] = 0
                       
                else:
                    if not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations):
                        pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                        
                        if grid_copy[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)] != 0:
                            used_locations_mod[int(get_range(last_key_loc[1])/60)].remove((get_range(last_key_loc[0]), get_range(last_key_loc[1])))
                        grid_copy[int(get_range(last_key_loc[1])/60)][int(get_range(last_key_loc[0])/60)] = 0
                        
            if event.key == pygame.K_UP:
                up_arr = True
              
            if event.key == pygame.K_DOWN:
                moved_mouse = False
                #First time up key is used
                if last_key_loc == ():
                    available_spot = not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations_mod)

                    if available_spot:
                        #Highlight available spot 
                        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(mouse[0])+3, get_range(mouse[1])+3, 56, 56))
                    
                    #Update last key loc
                    last_key_loc = (mouse[0], mouse[1])
                    prev = last_key_loc
                else:
                    if last_key_loc[1] != 480:
                        available_spot = not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])+60) in x for x in used_locations_mod)

                        #Spot is available, remove last highlighted spot and advance 
                        if available_spot:
                            if (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)
                                and grid[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)] == grid_copy[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]):
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))                           
                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(last_key_loc[0])+3, (get_range(last_key_loc[1])+60)+3, 56, 56))
                            
                            if solved_puzzle != [] and gen_sol and (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)):
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))

                            # if input_num != '':
                            #     grid_copy[int(get_range(mouse[1])/60)][int(get_range(mouse[0])/60)] = int(input_num)

                        #spot is unavailable, remove last highted spot and advance but do not hightlight
                        else:
                            if not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod) and not get_range(last_key_loc[1])+60 >480:
                                if solved_puzzle != [] and gen_sol:
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                    screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                                else:
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                            
                        if get_range(last_key_loc[1])+60 > 480:
                            last_key_loc = (get_range(last_key_loc[0]), 480)
                        else:
                            last_key_loc = (get_range(last_key_loc[0]), get_range(last_key_loc[1])+60)

            if event.key == pygame.K_LEFT:
                moved_mouse = False
               #First time up key is used
                if last_key_loc == ():
                    available_spot = not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations_mod)

                    if available_spot:
                        #Highlight available spot 
                        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(mouse[0])+3, get_range(mouse[1])+3, 56, 56))
                    
                    #Update last key loc
                    last_key_loc = (mouse[0], mouse[1])
                    prev = last_key_loc
                else:
                    if last_key_loc[0] != 0:
                        available_spot = not any((get_range(last_key_loc[0])-60, get_range(last_key_loc[1])) in x for x in used_locations_mod)

                        #Spot is available, remove last highlighted spot and advance 
                        if available_spot:
                            if (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)
                                and grid[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)] == grid_copy[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]):
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))                           
                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect((get_range(last_key_loc[0])-60)+3, (get_range(last_key_loc[1]))+3, 56, 56))

                            if solved_puzzle != [] and gen_sol and (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)):
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                        #spot is unavailable, remove last highted spot and advance but do not hightlight
                        else:
                            if not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod) and not get_range(last_key_loc[0])-60 <0:
                                if solved_puzzle != [] and gen_sol:
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                    screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                                else:
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                        if get_range(last_key_loc[0])-60 < 0:
                            last_key_loc = (0, get_range(last_key_loc[1]))
                        else:
                            last_key_loc = (get_range(last_key_loc[0])-60, get_range(last_key_loc[1]))
        
            if event.key == pygame.K_RIGHT:
                moved_mouse = False
                #First time up key is used
                if last_key_loc == ():
                    available_spot = not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations_mod)

                    if available_spot:
                        #Highlight available spot 
                        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(mouse[0])+3, get_range(mouse[1])+3, 56, 56))
                    
                    #Update last key loc
                    last_key_loc = (mouse[0], mouse[1])
                    prev = last_key_loc
                else:
                    if last_key_loc[0] != 480:
                        available_spot = not any((get_range(last_key_loc[0])+60, get_range(last_key_loc[1])) in x for x in used_locations_mod)

                        #Spot is available, remove last highlighted spot and advance 
                        if available_spot:
                            if (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)
                                and grid[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)] == grid_copy[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]):
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))                           
                            pygame.draw.rect(screen,(255, 204, 255), pygame.Rect((get_range(last_key_loc[0])+60)+3, (get_range(last_key_loc[1]))+3, 56, 56))

                            if solved_puzzle != [] and gen_sol and (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)):
                                pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))

                        #spot is unavailable, remove last highted spot and advance but do not hightlight
                        else:
                            
                            if not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod) and not get_range(last_key_loc[0])+60 > 480:
                                if solved_puzzle != [] and gen_sol:
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                                    screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                                else:
                                    pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))
                        if get_range(last_key_loc[0])+60 > 480:
                            last_key_loc = (480, get_range(last_key_loc[1]))
                        else:
                            last_key_loc = (get_range(last_key_loc[0])+60, get_range(last_key_loc[1]))

    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_UP]:
        
                
    #Getting mouse position
    mouse = pygame.mouse.get_pos()

    #Highlight mouse hover for all buttons
    if not started:
        startup(screen, mouse, text_font)
    else:
        game_started_setup(screen, mouse)

    #Load info screen
    if info:
        screen.fill((204,255,255))
        if mouse[0]>=420 and mouse[0]<=520 and mouse[1]>=550 and mouse[1]<=580:
            back_button_hover(screen)
        else:
            back_button(screen)
        screen.blit(pygame.font.SysFont('Monotype', 15).render('Back' , True , (0,0,0)) , (450, 555))
        for i,line in enumerate(get_instructions()):
            screen.blit(pygame.font.SysFont('Monotype', 15).render(line , True , (0,0,0)) , (30, 30+(i*25)))
    
    if back:
        startup(screen, mouse, text_font)

    if up_arr:
        moved_mouse = False
        up_arr = False
        #First time up key is used
        if last_key_loc == ():
            available_spot = not any((get_range(mouse[0]), get_range(mouse[1])) in x for x in used_locations_mod)

            if available_spot:
                #Highlight available spot 
                pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(mouse[0])+3, get_range(mouse[1])+3, 56, 56))
            
            #Update last key loc
            last_key_loc = (mouse[0], mouse[1])
            prev = last_key_loc
        else:
            if last_key_loc[1] != 0:
                available_spot = not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])-60) in x for x in used_locations_mod)

                #Spot is available, remove last highlighted spot and advance  
                if available_spot:
                    if (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)
                        and grid[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)] == grid_copy[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]):
                        pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))                          
                    pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(get_range(last_key_loc[0])+3, (get_range(last_key_loc[1])-60)+3, 56, 56))      
                    
                    if solved_puzzle != [] and gen_sol and (not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod)):
                        pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))                          
                        screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                
                #spot is unavailable, remove last highted spot and advance but do not hightlight
                else:
                    
                    if not any((get_range(last_key_loc[0]), get_range(last_key_loc[1])) in x for x in used_locations_mod) and not get_range(last_key_loc[1])-60 <0:
                        
                        if solved_puzzle != [] and gen_sol:
                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))                          
                            screen.blit(num_font.render(str(solved_puzzle[int((get_range(last_key_loc[1]))/60)][int((get_range(last_key_loc[0]))/60)]), True , (255,0,0)) , (25+get_range(last_key_loc[0]), (25+get_range(last_key_loc[1]))))
                        else:
                            pygame.draw.rect(screen,(255, 255, 255), pygame.Rect(get_range(last_key_loc[0])+3, get_range(last_key_loc[1])+3, 56, 56))

                if get_range(last_key_loc[1])-60 < 0:
                    last_key_loc = (get_range(last_key_loc[0]), 0)
                else:
                    last_key_loc = (get_range(last_key_loc[0]), get_range(last_key_loc[1])-60)
            
    if verify:
        if (solved_puzzle != [] and grid_copy == solved_puzzle) or (solved_puzzle != [] and grid_copy == grid):
            valid_sol = True
        else:
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


