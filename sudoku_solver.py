#Sudoku Solver

#Importing and initializing pygame libary
import pygame 

pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,540])

#Run until user indiciates otherwise
running = True
while running: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))

    #Setting up 9x9 board (81 cells)
    for i in range(60,541, 60):

        #Creating bold lines to indicate sections for boxes
        if i==180 or i==360:
            pygame.draw.lines(screen, (0,0,0), False, [(i,0), (i, 540)], 3)

            pygame.draw.lines(screen, (0,0,0), False, [(0,i), (540, i)], 3)
        else:
            #Drawing vertical lines for sudoku board
            pygame.draw.line(screen, (0,0,0), (i,0), (i, 540))

            #Drawing horizontal lines for sudoku board
            pygame.draw.line(screen, (0,0,0), (0, i), (540, i))

    #Display
    pygame.display.flip()

#Close game
pygame.quit()
