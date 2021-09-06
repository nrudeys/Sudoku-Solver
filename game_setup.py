import numpy as np
from PIL import Image, ImageFilter
import pygame
import os 
import sys

def create_empty_board(screen):
    """Creating an empty board

    Args:
        screen (pygame.Surface): the visual representation of game
    """

    screen.fill((255, 255, 255))

    for i in range(0, 541, 60):
        if i % 180 == 0:
            # Creating bold lines to indicate square sections
            pygame.draw.lines(screen, (0, 0, 0), False, [(i, 0), (i, 540)], 4)
            pygame.draw.lines(screen, (0, 0, 0), False, [(0, i), (540, i)], 4)
        else:
            # Drawing vertical/horizontal lines
            pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, 540))
            pygame.draw.line(screen, (0, 0, 0), (0, i), (540, i))
    

def insert_values(screen, original_grid, solved_grid=None):
    """Inserts values onto screen game board

    This function returns a list of indices of given clues

    Args:
        screen (pygame.Surface): the visual representation of game
        num_font (pygame.font): render values in font type onto screen
        original_grid (numpy.ndarray)): 2D list that stores unmodified
        Sudoku puzzle
        solved_grid (numpy.ndarray)): 2D list that stores a Sudoku 
        puzzle solution
    """
    zero_x_indices, zero_y_indices = np.nonzero(original_grid == 0)
    nonzero_x_indices, nonzero_y_indices = np.nonzero(original_grid)

    used_spots = list(zip(nonzero_x_indices, nonzero_y_indices))
    num_font = pygame.font.SysFont('Monotype', 20, bold=True)

    if solved_grid is not None:
        for cell in list(zip(zero_x_indices, zero_y_indices)):
            # Color is displayed as red to help differentiate between
            # generated solution values and provided clues
            screen.blit(num_font.render(str(solved_grid[cell]), True,
            (255, 0, 0)), (25 + (cell[1] * 60), 25 + (cell[0] * 60)))

    for cell in used_spots:
        screen.blit(num_font.render(str(original_grid[cell]), True,
        (0, 0, 0)), (25 + (cell[1] * 60), (25 + (cell[0] * 60))))
    
    return [tuple(entry * 60 for entry in element) for element in used_spots] 


def button_highlight(screen, color, x_shift, rect_coords):
    """Changes the color of a button out of a grouping of buttons

    This function highlights a button depending on mouse position, it
    leaves all other buttons in its grouping unhighlighted.

    Args:
        screen (pygame.Surface): the visual representation of game
        color (tuple): color of button
        x_shift (bool): represents if buttons are presented vertically
        or horizontally 
        rect_coord (tuple): rectangular coordinates for button
    """

    if x_shift:
        # Creating buttons horizontally
        pygame.draw.rect(screen, color, pygame.Rect(rect_coords))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(rect_coords), 3)
    else:
        # Creating button vertically (x-axis does not shift)
        (y, x, w, h) = rect_coords

        pygame.draw.rect(screen, color, pygame.Rect(x, y, w, h))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x, y, w, h), 3)


def create_buttons(screen, rect_coords, r=None, x_shift=False):
    """Creating multiple buttons

    Args:
        screen (pygame.Surface): the visual representation of game
        rect_coord (tuple): rectangular coordinates for button
        r (range): range that buttons span across screen
        x_shift (bool): represents if buttons are presented vertically
        or horizontally 
        
    """

    (hover, constant_coord, width, height) = rect_coords

    for shifting_coord in r:
        if shifting_coord != hover:
            # No button will be highlighted
            button_highlight(screen, (192,192,192), x_shift,
            (shifting_coord, constant_coord, width, height))
        else:
            # A button will be highlighted
            button_highlight(screen, (255,204,255), x_shift,
            (shifting_coord, constant_coord, width, height))


def home_screen(screen, mouse, font):
    """Setting home screen for game

    Args:
        screen (pygame.Surface): the visual representation of game
        rect_coord (tuple): rectangular coordinates for button
        mouse (pygame.mouse): current mouse position on game screen
        font (pygame.font): font type used to render text
        
    """

    screen.fill((204, 255, 255))

    # Buttons for start, info, and enter
    if mouse[0] >= 215 and mouse[0] <= 335:
        if mouse[1] >= 130 and mouse[1] <= 170:
            create_buttons(screen, (130, 215, 120, 40), range(130, 271, 70))
        elif mouse[1] >= 200 and mouse[1] <= 240:
            create_buttons(screen, (200, 215, 120, 40), range(130, 271, 70))
        elif mouse[1] >= 270 and mouse[1] <= 310:
            create_buttons(screen, (270, 215, 120, 40), range(130, 271, 70))
        else:
            create_buttons(screen, (None, 215, 120, 40), range(130, 271, 70))
    else:
        create_buttons(screen, (None, 215, 120, 40), range(130, 271, 70))

    # Buttons for game difficulty (easy, medium, hard)
    if mouse[1] >= 410 and mouse[1] <= 450:
        if mouse[0] >= 50 and mouse[0] <= 150:
            create_buttons(screen, (50, 410, 100, 40), range(50, 371, 160), x_shift=True)
        elif mouse[0] >= 210 and mouse[0] <= 310:
            create_buttons(screen,(210, 410, 100, 40), range(50, 371, 160), x_shift=True)
        elif mouse[0] >= 370 and mouse[0] <= 470:
            create_buttons(screen, (370, 410, 100, 40), range(50, 371, 160), x_shift=True)
        else:
            create_buttons(screen, (None, 410, 100, 40), range(50, 371, 160), x_shift=True)
    else:
        create_buttons(screen, (None, 410, 100, 40), range(50, 371, 160), x_shift=True)

    # Buttons for assist on/off
    if mouse[1] >= 515 and mouse[1] <= 555:
        if mouse[0] >= 130 and mouse[0] <= 230:
            create_buttons(screen, (130, 515, 100, 40), range(130, 301, 170), x_shift=True)
        elif mouse[0] >= 300 and mouse[0] <= 400:
            create_buttons(screen, (300, 515, 100, 40), range(130, 301, 170), x_shift=True)
        else:
            create_buttons(screen, (None, 515, 100, 40), range(130, 301, 170), x_shift=True)
    else:   
        create_buttons(screen, (None, 515, 100, 40), range(130, 301, 170), x_shift=True)

    header = pygame.font.SysFont('Monotype', 30, bold=True)
    sub_titles = pygame.font.SysFont('Monotype', 25) 
    
    screen.blit(header.render('Sudoku Solver', True, (0, 0, 0)), (170, 60))
    
    screen.blit(font.render('Start', True, (0, 0, 0)), (250, 140))
    screen.blit(font.render('Info', True, (0, 0, 0)), (255, 210))
    screen.blit(font.render('Enter', True, (0, 0, 0)), (248, 280))

    screen.blit(sub_titles.render('Assist Mode', True, (0, 0, 0)), (183, 475))
    screen.blit(font.render('On', True, (0, 0, 0)), (168, 525))
    screen.blit(font.render('Off', True, (0, 0, 0)), (330, 525))

    screen.blit(sub_titles.render('Select Mode', True, (0, 0, 0)), (183, 355))
    screen.blit(font.render('EASY', True, (0, 0, 0)), (75, 420))
    screen.blit(font.render('MEDIUM', True, (0, 0, 0)), (228, 420))
    screen.blit(font.render('HARD', True, (0, 0, 0)), (398, 420))


def info_screen(screen, mouse):
    """Setting info screen for game

    Args:
        screen (pygame.Surface): the visual representation of game
        mouse (pygame.mouse): current mouse position on game screen
    """

    screen.fill((204,255,255))
    font = pygame.font.SysFont('Monotype', 15)

    try:
        # Pyinstaller path
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()

    file_path = os.path.join(wd,"instructions.txt")
    text_file = open(file_path, "r")
    lines = [line.replace("\n", "") for line in text_file.readlines()]
    text_file.close()

    for i, line in enumerate(lines):
        screen.blit(font.render(line, True, (0, 0, 0)), (30, 30 + (i * 25)))

    if mouse[1] >= 550 and mouse[1] <= 585 and mouse[0] >= 420 and mouse[0] <= 520:
       # Highlight button
       pygame.draw.rect(screen, (255, 204, 255), pygame.Rect(420, 550, 100, 35))
       pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 35), 3)            
    else:
        pygame.draw.rect(screen, (192,192,192), pygame.Rect(420, 550, 100, 35))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(420, 550, 100, 35), 3)


    screen.blit(font.render('Back', True, (0, 0, 0)), (450, 560))


def game_screen(screen, mouse):
    """Creating screen for a started game

    Args:
        screen (pygame.Surface): the visual representation of game
        mouse (pygame.mouse): current mouse position on game screen
    """

    # Creating game buttons
    if mouse[1] >= 550 and mouse[1] <= 590:
        if mouse[0] >= 30 and mouse[0] <= 130:
            create_buttons(screen, (30, 550, 100, 40),
            range(30, 421, 130), True)
        elif mouse[0] >= 160 and mouse[0] <= 260:
            create_buttons(screen, (160, 550, 100, 40),
            range(30, 421, 130), True)
        elif mouse[0] >= 290 and mouse[0] <= 390:
            create_buttons(screen, (290, 550, 100, 40),
            range(30, 421, 130), True)
        elif mouse[0] >= 420 and mouse[0] <= 520:
            create_buttons(screen, (420, 550, 100, 40),
            range(30, 421, 130), True)
        else:
            create_buttons(screen, (None, 550, 100, 40),
            range(30, 421, 130), True)
    else:
        create_buttons(screen, (None, 550, 100, 40),
        range(30, 421, 130), True)

    font = pygame.font.SysFont('Monotype', 15)

    screen.blit(font.render('New Game', True, (0, 0, 0)), (45, 560))
    screen.blit(font.render('Generate', True, (0, 0, 0)), (175, 555))
    screen.blit(font.render('Solution', True, (0, 0, 0)), (175, 568))
    screen.blit(font.render('Verify', True, (0, 0, 0)), (305, 555))
    screen.blit(font.render('Solution', True, (0, 0, 0)), (305, 569))
    screen.blit(font.render('Back', True, (0, 0, 0)), (450, 560))


def display_message(screen):
    """Display message on screen

    Args:
        screen (pygame.Surface): the visual representation of game
    """

    pygame.draw.rect(screen, (192, 192, 192), pygame.Rect(125, 150, 300, 80))
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(125, 150, 300, 80), 3)


def blur_background(screen, name):
    """Blur screen background 

    Args:
        screen (pygame.Surface): the visual representation of game
        name (str): name of image
    """
    pygame.image.save(screen, name)

    OriImage = Image.open(name)
    blurImage = OriImage.filter(ImageFilter.BLUR)
    blurImage.save('blur_image.jpg')
    image = pygame.image.load("blur_image.jpg").convert_alpha()
    screen.blit(image, (0, 0))