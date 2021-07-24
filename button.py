import pygame 

pygame.init()

#Setting up drawing window
screen = pygame.display.set_mode([540,540])

pygame.display.flip()

font = pygame.font.SysFont('Monotype', 18)

running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse[0] >= 215 and mouse[0] <= 335:
                if mouse[1] >= 250 and mouse[1] <= 290:
                    running = False                    


    screen.fill((255, 255, 255))

    mouse = pygame.mouse.get_pos()
    
    #Highlight mouse hover
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

    
    screen.blit(font.render('Start' , True , (0,0,0)) , (250, 188))
    screen.blit(font.render('Quit' , True , (0,0,0)) , (255, 257))

    #Display
    pygame.display.flip()

#Close game
pygame.quit()