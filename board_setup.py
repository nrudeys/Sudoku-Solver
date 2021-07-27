import pygame 
from solve_dataset import *

def board_setup(screen):
    #Setting up 9x9 board (81 cells)
    pygame.draw.lines(screen, (0,0,0), False, [(0,0), (0, 540)], 4)

    pygame.draw.lines(screen, (0,0,0), False, [(0,0), (540, 0)], 4)

    for i in range(60,541, 60):

        #Creating bold lines to indicate sections for boxes
        if i==180 or i==360 or i==540:
            pygame.draw.lines(screen, (0,0,0), False, [(i,0), (i, 540)], 4)

            pygame.draw.lines(screen, (0,0,0), False, [(0,i), (540, i)], 4)
        else:
            #Drawing vertical lines for sudoku board
            pygame.draw.line(screen, (0,0,0), (i,0), (i, 540))

            #Drawing horizontal lines for sudoku board
            pygame.draw.line(screen, (0,0,0), (0, i), (540, i))
    
def fill_board(solved_grid, original_grid, screen, num_font, color):
    # if solved_grid != None:
    #     print("HERE")
    #     print_grid(original_grid)
    #     print("?")
    for i,row_idx in enumerate(grid_indices):
        for j,col_idx in enumerate(grid_indices):
            if solved_grid != None:
                if original_grid[row_idx][col_idx]==0:
                    screen.blit(num_font.render(str(solved_grid[row_idx][col_idx]) , True , color) , (25+(j*60), (25+(i*60))))
            else: 
                if original_grid[row_idx][col_idx]!=0:
                    screen.blit(num_font.render(str(original_grid[row_idx][col_idx]) , True , color) , (25+(j*60), (25+(i*60))))

#def check_for_entered_input(screen):

def reset_screen(screen, color):
    screen.fill(color)

def back_button(screen):
    pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(420, 550, 100, 30))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 30), 3)



def back_button_hover(screen):
    pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(420, 550, 100, 30))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 30), 3)

def startup(screen, mouse, font):
    reset_screen(screen, (204, 255, 255))

    if mouse[0] >= 215 and mouse[0] <= 335:
        if mouse[1] >= 180 and mouse[1] <= 220:
            pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(215, 180, 120, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 180, 120, 40), 3)
            pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(215, 250, 120, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 250, 120, 40), 3)
        elif mouse[1] >= 250 and mouse[1] <= 290:
            pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(215, 180, 120, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 180, 120, 40), 3)
            pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(215, 250, 120, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 250, 120, 40), 3)
        else:
            pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(215, 180, 120, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 180, 120, 40), 3)
            pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(215, 250, 120, 40))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 250, 120, 40), 3)
    else:
        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(215, 180, 120, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 180, 120, 40), 3)
        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(215, 250, 120, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(215, 250, 120, 40), 3)

    screen.blit(pygame.font.SysFont('Monotype', 30, bold=True).render('Sudoku Solver' , True , (0,0,0)) , (170, 80))    
    screen.blit(font.render('Start' , True , (0,0,0)) , (250, 188))
    screen.blit(font.render('Info' , True , (0,0,0)) , (255, 257))

def game_started_setup(screen, mouse):
    if mouse[1] >= 550 and mouse[1] <= 590 and mouse[0] >=30 and mouse[0]<=130:
        pygame.draw.rect(screen,(255, 204, 255), pygame.Rect(30, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(30, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(160, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(160, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(290, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(290, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(420, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)

    elif mouse[1] >= 550 and mouse[1] <= 590 and mouse[0] >=160 and mouse[0]<=260:
        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(30, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(30, 550, 100, 40), 3)

        pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(160, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(160, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(290, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(290, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(420, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)
    elif mouse[1] >= 550 and mouse[1] <= 590 and mouse[0] >=290 and mouse[0]<=390:
        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(30, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(30, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(160, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(160, 550, 100, 40), 3)

        pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(290, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(290, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(420, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)
    elif mouse[1] >= 550 and mouse[1] <= 590 and mouse[0] >=420 and mouse[0]<=520:
        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(30, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(30, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(160, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(160, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(290, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(290, 550, 100, 40), 3)

        pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(420, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)

    else:
        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(30, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(30, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(160, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(160, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(290, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(290, 550, 100, 40), 3)

        pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(420, 550, 100, 40))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 40), 3)

    screen.blit(pygame.font.SysFont('Monotype', 15).render('New Game' , True , (0,0,0)) , (45, 560))
    screen.blit(pygame.font.SysFont('Monotype', 15).render('Generate' , True , (0,0,0)) , (175, 555))
    screen.blit(pygame.font.SysFont('Monotype', 15).render('Solution' , True , (0,0,0)) , (175, 568))
    screen.blit(pygame.font.SysFont('Monotype', 15).render('Verify' , True , (0,0,0)) , (305, 555))
    screen.blit(pygame.font.SysFont('Monotype', 15).render('Solution' , True , (0,0,0)) , (305, 569))
    screen.blit(pygame.font.SysFont('Monotype', 15).render('Verify' , True , (0,0,0)) , (305, 555))
    screen.blit(pygame.font.SysFont('Monotype', 15).render('Back' , True , (0,0,0)) , (450, 560))

def get_instructions():
    file = open("instructions.txt", "r")
    return [line.replace("\n", "") for line in file.readlines()]