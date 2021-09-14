import numpy as np
import pygame as py

def round_num(num):
    """Rounding number based on which range its falls in

    Args:
    num (int): number 
    """

    if num <= 59:
        return 0
    elif num >= 60 and num <= 119:
        return 60
    elif num >= 120 and num <= 179:
        return 120
    elif num >= 180 and num <= 239:
        return 180
    elif num >= 240 and num <= 299:
        return 240
    elif num >= 300 and num <= 359:
        return 300
    elif num >= 360 and num <= 419:
        return 360
    elif num >= 420 and num <= 479:
        return 420
    else:
        return 480


def set_num(num, dir):
    """Adds x and dir

    Args:
    num (int): number 
    """

    if num + dir > 480:
        # Exceeds, wrap back to 0
        return 0
    if num + dir < 0:
        # Negative, wrap back to 480
        return 480

    return num + dir


def get_cell_indices():
    """Return cell indices as multiples of 60
    """

    cell_indices = []

    for idx in np.ndindex(9, 9):
        cell_indices.append(tuple(t *60 for t in idx))

    return cell_indices


def set_ents_dicts(used_spots):
    """Set to dictionarys to keep track of a Sudoku puzzle solution
       and entries

    Args:
    sol (numpy.ndarray): solution of Sudoku puzzle
    used_spots (list):  indices of cells with given clues
    """

    entries = {}

    for idx in get_cell_indices():
        if idx not in used_spots:
            entries[idx] = 0
        else:
            entries[idx] = True

    return entries


def get_curr_grid_vals(entries, used_spots=None, grid=None):
    """Gets current values in Sudoku puzzle

    Args:
    sol (numpy.ndarray): solution of Sudoku puzzle
    used_spots (list):  indices of cells with given clues
    """
    curr_grid_vals = np.asarray(list(entries.values())).reshape((9, 9))
    curr_grid_vals = np.transpose(curr_grid_vals)

    if grid is not None:
        for key in used_spots:
            (x, y) = key
            idx = (y // 60, x // 60)
            curr_grid_vals[idx] = grid[idx]

    return curr_grid_vals


def get_square(curr_vals, x, y):
    sq_x_init = 3 * round(((x // 60) - 1) / 3)
    sq_y_init = 3 * round(((y // 60) - 1) / 3)
    
    return curr_vals[sq_y_init:sq_y_init + 3, sq_x_init:sq_x_init + 3]


def count_occurrences(curr_vals, num, x, y):
    square = get_square(curr_vals, x, y)

    col_count = np.count_nonzero(curr_vals[:,x // 60] == num)
    row_count = np.count_nonzero(curr_vals[y // 60,:] == num)
    sq_count = np.count_nonzero(square == num)

    return (col_count, row_count, sq_count)


def advance(screen, cell, grid, entries, invalid_ent=False):
    num_font = py.font.SysFont('Monotype', 20, bold=True)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)

    (x, y, color) = cell
    cell_idx = (x, y)
    idx = (y // 60, x // 60)

    py.draw.rect(screen, color, py.Rect(x + 3, y + 3, 56, 56)) 

    
    if str(entries[cell_idx]).isnumeric() and entries[cell_idx] != 0:
        if invalid_ent:
            screen.blit(num_font.render(str(entries[cell_idx]), True, RED),
                (25 + x, 25 + y)
            )
        else:
            screen.blit(num_font.render(str(entries[cell_idx]), True, BLUE),
                (25 + x, 25 + y)
            )
    elif not str(entries[cell_idx]).isnumeric():
        screen.blit(num_font.render(str(grid[idx]), True, BLACK),
            (25 + x, 25 + y)
        )

def enter_board_adv(screen, cell, entries_ent, sol_ent=False):
    (x1, y1, color) = cell
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    num_font = py.font.SysFont('Monotype', 20, bold=True)

    #Erase previous empty square
    py.draw.rect(screen, color, py.Rect(x1 + 3, y1 + 3, 56, 56)) 
    
    if type(sol_ent) == np.ndarray and entries_ent[(x1, y1)] == 0:
        screen.blit(num_font.render(str(sol_ent[(y1//60, x1//60)]), True, BLUE),
                (25 + x1, 25 + y1)
        )
    else:
        if entries_ent[(x1, y1)] != 0:
            screen.blit(num_font.render(str(entries_ent[(x1, y1)]), True, BLACK),
                    (25 + x1, 25 + y1)
            )


# def set_font_color(invalid, assist, ):
#     if (x, y) in invalid.keys() and assist:
#         screen.blit(num_font.render(str(grid[(curr_y // 60, curr_x // 60)]), 
#         True, BLACK), (25 + curr_x, 25 + curr_y))
#     else:
#         screen.blit(num_font.render(str(grid[(curr_y // 60, curr_x // 60)]), 
#         True, BLACK), (25 + curr_x, 25 + curr_y))