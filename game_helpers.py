import numpy as np
import pygame as py
import game_modes as modes
import gen_dataset as gen_data


def set_grid(easy, medium, hard, default):
    """Generate a grid according to modes

    Args:
        easy (bool): easy mode selected
        medium (bool): medium mode selected
        hard (bool): hard mode selected
        default (modes.Mode): randomly selected mode 
    """

    if easy:
        grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
    elif medium:
        grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
    elif hard:
        grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)
    else:
        if default == modes.Mode.EASY:
            grid = gen_data.gen_puzzle(0, 2, 4, 5, 42)
        elif default == modes.Mode.MEDIUM:
            grid = gen_data.gen_puzzle(3, 5, 5, 6, 53)
        else:
            grid = gen_data.gen_puzzle(6, 8, 6, 7, 64)

    return grid


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
        cell_indices.append(tuple(t * 60 for t in idx))

    return cell_indices


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
    """Gets 3x3 square of a cell using (x, y) position

    Args:
    curr_vals (numpy.ndarray): current vals of Sudoku puzzle
    x (int): x position of current cell 
    y (int): y position of current cell
    """

    sq_x_init = 3 * round(((x // 60) - 1) / 3)
    sq_y_init = 3 * round(((y // 60) - 1) / 3)

    return curr_vals[sq_y_init:sq_y_init + 3, sq_x_init:sq_x_init + 3]


def count_occurrences(curr_vals, num, x, y):
    """Count occurrences of given num in row, col, and square

    Args:
    curr_vals (numpy.ndarray): current vals of Sudoku puzzle
    num (int): number from 1 - 9
    x (int): x position of current cell 
    y (int): y position of current cell
    """

    square = get_square(curr_vals, x, y)

    col_count = np.count_nonzero(curr_vals[:, x // 60] == num)
    row_count = np.count_nonzero(curr_vals[y // 60, :] == num)
    sq_count = np.count_nonzero(square == num)

    return (col_count, row_count, sq_count)
