import numpy as np
from PIL import Image, ImageFilter
import pygame as py
import os
import sys
from colors import Colors


def create_empty_board(screen):
    """Creating an empty board

    Args:
        screen (py.Surface): the visual representation of game
    """

    screen.fill(Colors.WHITE)

    for i in range(0, 541, 60):
        if i % 180 == 0:
            # Creating bold lines to indicate square sections
            py.draw.lines(screen, Colors.BLACK,
                          False, [(i, 0), (i, 540)], 4)
            py.draw.lines(screen, Colors.BLACK, False, [(0, i), (540, i)], 4)
        else:
            # Drawing vertical/horizontal lines
            py.draw.line(screen, Colors.BLACK, (i, 0), (i, 540))
            py.draw.line(screen, Colors.BLACK, (0, i), (540, i))


def insert_values(screen, original_grid, solved_grid=None):
    """Inserts values onto screen game board

    This function returns a list of indices of given clues

    Args:
        screen (py.Surface): the visual representation of game
        num_font (py.font): render values in font type onto screen
        original_grid (numpy.ndarray)): 2D list that stores unmodified
        Sudoku puzzle
        solved_grid (numpy.ndarray)): 2D list that stores a Sudoku 
        puzzle solution
    """
    zero_x_indices, zero_y_indices = np.nonzero(original_grid == 0)
    nonzero_x_indices, nonzero_y_indices = np.nonzero(original_grid)

    used_spots = list(zip(nonzero_x_indices, nonzero_y_indices))
    num_font = py.font.SysFont('Monotype', 20, bold=True)

    if solved_grid is not None:
        for cell in list(zip(zero_x_indices, zero_y_indices)):
            # Color is displayed as red to help differentiate between
            # generated solution values and provided clues
            screen.blit(num_font.render(str(solved_grid[cell]), True,
                                        Colors.BLUE), (25 + (cell[1] * 60),
                                                       25 + (cell[0] * 60)))

    for cell in used_spots:
        screen.blit(num_font.render(str(original_grid[cell]), True,
                                    Colors.BLACK), (25 + (cell[1] * 60),
                                                    (25 + (cell[0] * 60))))

    return [(y * 60, x * 60) for x, y in used_spots]


def button_highlight(screen, color, rect_coords):
    """Changes the color of a button out of a grouping of buttons

    This function highlights a button depending on mouse position, it
    leaves all other buttons in its grouping unhighlighted.

    Args:
        screen (py.Surface): the visual representation of game
        color (tuple): color of button
        x_shift (bool): represents if buttons are presented vertically
        or horizontally 
        rect_coord (tuple): rectangular coordinates for button
    """

    py.draw.rect(screen, color, py.Rect(rect_coords))
    py.draw.rect(screen, Colors.BLACK, py.Rect(rect_coords), 3)


def create_buttons(screen, rect_coords, r=None):
    """Creating multiple buttons

    Args:
        screen (py.Surface): the visual representation of game
        rect_coord (tuple): rectangular coordinates for button
        r (range): range that buttons span across screen
        x_shift (bool): represents if buttons are presented vertically
        or horizontally 

    """

    (hover, constant_coord, width, height) = rect_coords

    for shifting_coord in r:
        if shifting_coord != hover:
            # No button will be highlighted
            button_highlight(screen, Colors.GRAY,
                             (shifting_coord, constant_coord, width, height))
        else:
            # A button will be highlighted
            button_highlight(screen, Colors.PINK,
                             (shifting_coord, constant_coord, width, height))


def home_screen(screen, mouse, font):
    """Setting home screen for game

    Args:
        screen (py.Surface): the visual representation of game
        rect_coord (tuple): rectangular coordinates for button
        mouse (py.mouse): current mouse position on game screen
        font (py.font): font type used to render text

    """

    if getattr(sys, 'frozen', False):
        wd = sys._MEIPASS
        img = py.image.load(os.path.join(wd, '.', "background.png")).convert()
    else:
        wd = ''
        img = py.image.load("background.png")

    screen.blit(img, (0, 0))

    s = py.Surface((420, 480))
    s.set_alpha(128)
    s.fill(Colors.MAYA_BLUE)
    screen.blit(s, (60, 60))
    py.draw.rect(screen, Colors.BLACK, py.Rect(60, 60, 420, 480), 3)

    if mouse[1] >= 180 and mouse[1] <= 220:
        # Buttons for start, info, and enter
        if mouse[0] >= 90 and mouse[0] <= 180:
            create_buttons(screen, (90, 180, 90, 40), range(90, 351, 130))
        elif mouse[0] >= 220 and mouse[0] <= 310:
            create_buttons(screen, (220, 180, 90, 40), range(90, 351, 130))
        elif mouse[0] >= 350 and mouse[0] <= 440:
            create_buttons(screen, (350, 180, 90, 40), range(90, 351, 130))
        else:
            create_buttons(screen, (None, 180, 90, 40), range(90, 351, 130))
    else:
        create_buttons(screen, (None, 180, 90, 40), range(90, 351, 130))

    if mouse[1] >= 340 and mouse[1] <= 380:
        # Buttons for game difficulty (easy, medium, hard)
        if mouse[0] >= 90 and mouse[0] <= 180:
            create_buttons(screen, (90, 340, 90, 40), range(90, 351, 130))
        elif mouse[0] >= 220 and mouse[0] <= 310:
            create_buttons(screen, (220, 340, 90, 40), range(90, 351, 130))
        elif mouse[0] >= 350 and mouse[0] <= 440:
            create_buttons(screen, (350, 340, 90, 40), range(90, 351, 130))
        else:
            create_buttons(screen, (None, 340, 90, 40), range(90, 351, 130))
    else:
        create_buttons(screen, (None, 340, 90, 40), range(90, 351, 130))

    if mouse[1] >= 470 and mouse[1] <= 510:
        # Buttons for assist on/off
        if mouse[0] >= 155 and mouse[0] <= 245:
            create_buttons(screen, (155, 470, 90, 40), range(155, 286, 130))
        elif mouse[0] >= 285 and mouse[0] <= 375:
            create_buttons(screen, (285, 470, 90, 40), range(155, 286, 130))
        else:
            create_buttons(screen, (None, 470, 90, 40), range(155, 286, 130))
    else:
        create_buttons(screen, (None, 470, 90, 40), range(155, 286, 130))

    header = py.font.SysFont('Monotype', 35, bold=True)
    sub_titles = py.font.SysFont('Monotype', 25, bold=True)

    screen.blit(header.render('SUDOKU SOLVER', True, Colors.BLACK), (135, 90))

    screen.blit(font.render('START', True, Colors.BLACK), (105, 190))
    screen.blit(font.render('ENTER', True, Colors.BLACK), (238, 190))
    screen.blit(font.render('INFO', True, Colors.BLACK), (370, 190))

    screen.blit(sub_titles.render('SELECT MODE', True, Colors.BLACK),
                (183, 275))

    screen.blit(font.render('EASY', True, Colors.BLACK), (110, 350))
    screen.blit(font.render('MEDIUM', True, Colors.BLACK), (232, 350))
    screen.blit(font.render('HARD', True, Colors.BLACK), (370, 350))

    screen.blit(sub_titles.render('ASSIST MODE', True, Colors.BLACK),
                (183, 420))

    screen.blit(font.render('On', True, Colors.BLACK), (190, 480))
    screen.blit(font.render('Off', True, Colors.BLACK), (315, 480))


def info_screen(screen, mouse, lines, pg):
    """Setting info screen for game

    Args:
        screen (py.Surface): the visual representation of game
        mouse (py.mouse): current mouse position on game screen
    """

    screen.fill(Colors.SKY_BLUE)
    font = py.font.SysFont('Monotype', 15)
    header_font = py.font.SysFont('Monotype', 18, bold=True)

    i = 0

    for line in lines:
        # Headers all end with "S"
        if len(line) != 0 and line[-1] == "S":
            screen.blit(header_font.render(
                line, True, Colors.BLACK), (30, 30 + (i * 25)))
        else:
            screen.blit(font.render(line, True, Colors.BLACK),
                        (30, 30 + (i * 25)))
        i += 1

    if (mouse[1] >= 550 and mouse[1] <= 585 and mouse[0] >= 420 and
            mouse[0] <= 520):
        # Highlight button
        py.draw.rect(screen, Colors.PINK, py.Rect(420, 550, 100, 35))
        py.draw.rect(screen, Colors.BLACK, py.Rect(420, 550, 100, 35), 3)
    else:
        py.draw.rect(screen, Colors.GRAY, py.Rect(420, 550, 100, 35))
        py.draw.rect(screen, Colors.BLACK, py.Rect(420, 550, 100, 35), 3)

    if mouse[1] >= 555 and mouse[1] <= 575:
        if mouse[0] >= 50 and mouse[0] <= 60:
            # Highlight button
            if pg != 1:
                py.draw.polygon(screen, Colors.PINK,
                                ((60, 555), (60, 575), (50, 565)))
                py.draw.polygon(screen, Colors.BLACK,
                                ((60, 555), (60, 575), (50, 565)), 2)

            if pg != 2:
                py.draw.polygon(screen, Colors.BLACK,
                                ((115, 555), (115, 575), (125, 565)))

        elif mouse[0] >= 115 and mouse[0] <= 125:
            if pg != 1:
                py.draw.polygon(screen, Colors.BLACK,
                                ((60, 555), (60, 575), (50, 565)))

            if pg != 2:
                py.draw.polygon(screen, Colors.PINK,
                                ((115, 555), (115, 575), (125, 565)))
                py.draw.polygon(screen, Colors.BLACK,
                                ((115, 555), (115, 575), (125, 565)), 2)

        else:
            if pg != 1:
                py.draw.polygon(screen, Colors.BLACK,
                                ((60, 555), (60, 575), (50, 565)))
            if pg != 2:
                py.draw.polygon(screen, Colors.BLACK,
                                ((115, 555), (115, 575), (125, 565)))
    else:
        if pg != 1:
            py.draw.polygon(screen, Colors.BLACK,
                            ((60, 555), (60, 575), (50, 565)))

        if pg != 2:
            py.draw.polygon(screen, Colors.BLACK,
                            ((115, 555), (115, 575), (125, 565)))

    py.draw.rect(screen, (255, 255, 255), py.Rect(73, 555, 30, 25))
    screen.blit(font.render(str(pg), True, Colors.BLACK), (83, 560))
    screen.blit(font.render('Back', True, Colors.BLACK), (450, 560))


def game_screen(screen, mouse):
    """Creating screen for a started game

    Args:
        screen (py.Surface): the visual representation of game
        mouse (py.mouse): current mouse position on game screen
    """

    # Creating game buttons
    if mouse[1] >= 550 and mouse[1] <= 590:
        if mouse[0] >= 30 and mouse[0] <= 130:
            create_buttons(screen, (30, 550, 100, 40),
                           range(30, 421, 130))
        elif mouse[0] >= 160 and mouse[0] <= 260:
            create_buttons(screen, (160, 550, 100, 40),
                           range(30, 421, 130))
        elif mouse[0] >= 290 and mouse[0] <= 390:
            create_buttons(screen, (290, 550, 100, 40),
                           range(30, 421, 130))
        elif mouse[0] >= 420 and mouse[0] <= 520:
            create_buttons(screen, (420, 550, 100, 40),
                           range(30, 421, 130))
        else:
            create_buttons(screen, (None, 550, 100, 40),
                           range(30, 421, 130))
    else:
        create_buttons(screen, (None, 550, 100, 40),
                       range(30, 421, 130))

    font = py.font.SysFont('Monotype', 15)

    screen.blit(font.render('New Game', True, Colors.BLACK), (45, 560))
    screen.blit(font.render('Generate', True, Colors.BLACK), (175, 555))
    screen.blit(font.render('Solution', True, Colors.BLACK), (175, 568))
    screen.blit(font.render('Verify', True, Colors.BLACK), (305, 555))
    screen.blit(font.render('Solution', True, Colors.BLACK), (305, 569))
    screen.blit(font.render('Back', True, Colors.BLACK), (450, 560))


def enter_board_screen(screen, mouse):
    """Creating screen for ENTER game

    Args:
        screen (py.Surface): the visual representation of game
        mouse (py.mouse): current mouse position on game screen
    """

    if mouse[1] >= 550 and mouse[1] <= 590:
        if mouse[0] >= 20 and mouse[0] <= 120:
            create_buttons(screen, (20, 550, 100, 40),
                           range(20, 421, 200))
        elif mouse[0] >= 220 and mouse[0] <= 320:
            create_buttons(screen, (220, 550, 100, 40),
                           range(20, 421, 200))
        elif mouse[0] >= 420 and mouse[0] <= 520:
            create_buttons(screen, (420, 550, 100, 40),
                           range(20, 421, 200))
        else:
            create_buttons(screen, (None, 550, 100, 40),
                           range(20, 421, 200))
    else:
        create_buttons(screen, (None, 550, 100, 40),
                       range(20, 421, 200))

    font = py.font.SysFont('Monotype', 15)

    screen.blit(font.render('CLEAR', True, Colors.BLACK), (45, 560))
    screen.blit(font.render('SOLVE', True, Colors.BLACK), (245, 560))
    screen.blit(font.render('BACK', True, Colors.BLACK), (450, 560))


def display_message(screen):
    """Display message on screen

    Args:
        screen (py.Surface): the visual representation of game
    """

    py.draw.rect(screen, Colors.GRAY, py.Rect(125, 150, 300, 80))
    py.draw.rect(screen, Colors.BLACK, py.Rect(125, 150, 300, 80), 3)


def blur_background(screen, name):
    """Blur screen background 

    Args:
        screen (py.Surface): the visual representation of game
        name (str): name of image
    """
    py.image.save(screen, name)

    OriImage = Image.open(name)
    blurImage = OriImage.filter(ImageFilter.BLUR)
    blurImage.save('blur_image.jpg')
    image = py.image.load("blur_image.jpg").convert_alpha()
    screen.blit(image, (0, 0))


def get_lines():
    """Get lines from instructions.txt and return lines in an array
    """

    try:
        # Pyinstaller path
        wd = sys._MEIPASS
    except AttributeError:
        wd = os.getcwd()

    file_path = os.path.join(wd, "instructions.txt")
    text_file = open(file_path, "r")
    lines = [line.replace("\n", "") for line in text_file.readlines()]
    text_file.close()

    return lines


def advance(screen, cell, grid, entries, invalid_ent=False):
    """Move on screen and highlight cell accordingly to given args

    This function is for movement across the board in START mode

    Args:
        screen (py.Surface): the visual representation of game
        cell (tuple): details of given cell x, y coordinates and color
        grid (numpy.ndarray): representation of Sudoku puzzle 
        entries(dict): tracking record of entries given by user 
        (position coords, num)
        invalid_ent (dict): tracking record of invalid entries given by
        user (position coordinates, num). Default value is False.
    """

    num_font = py.font.SysFont('Monotype', 20, bold=True)

    (x, y, color) = cell
    cell_idx = (x, y)
    idx = (y // 60, x // 60)

    py.draw.rect(screen, color, py.Rect(x + 3, y + 3, 56, 56))

    if str(entries[cell_idx]).isnumeric() and entries[cell_idx] != 0:
        if invalid_ent:
            screen.blit(num_font.render(str(entries[cell_idx]), True,
                                        Colors.RED),
                        (25 + x, 25 + y)
                        )
        else:
            screen.blit(num_font.render(str(entries[cell_idx]), True,
                                        Colors.BLUE),
                        (25 + x, 25 + y)
                        )
    elif not str(entries[cell_idx]).isnumeric():
        screen.blit(num_font.render(str(grid[idx]), True, Colors.BLACK),
                    (25 + x, 25 + y)
                    )


def enter_board_adv(screen, cell, entries_ent, sol_ent=False):
    """Move on screen and highlight cell accordingly to given args

    This function is for movement across the board in ENTER mode 

    Args:
        screen (py.Surface): the visual representation of game
        cell (tuple): details of given cell x, y coordinates and color
        entries_ent(dict): tracking record of entries given by user 
        (position coords, num)
        sol_ent (dict): tracking record of generated solution of the
        Sodoku puzzle (position coordinates, num). Default value is False.
    """

    (x1, y1, color) = cell
    num_font = py.font.SysFont('Monotype', 20, bold=True)

    # Erase previous empty square
    py.draw.rect(screen, color, py.Rect(x1 + 3, y1 + 3, 56, 56))

    if type(sol_ent) == np.ndarray and entries_ent[(x1, y1)] == 0:
        screen.blit(num_font.render(str(sol_ent[(y1//60, x1//60)]),
                                    True, Colors.BLUE),
                    (25 + x1, 25 + y1)
                    )
    else:
        if entries_ent[(x1, y1)] != 0:
            screen.blit(num_font.render(str(entries_ent[(x1, y1)]),
                                        True, Colors.BLACK),
                        (25 + x1, 25 + y1)
                        )
