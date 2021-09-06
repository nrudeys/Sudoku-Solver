import numpy as np

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


def set_ents_dicts(sol, used_spots):
    """Set to dictionarys to keep track of a Sudoku puzzle solution
       and entries

    Args:
    sol (numpy.ndarray): solution of Sudoku puzzle
    used_spots (list):  indices of cells with given clues
    """

    sol_entries = entries = {}

    for idx in get_cell_indices():
        if idx not in used_spots:
            sol_entries[idx] = sol[idx[0] // 60][idx[1] // 60]
            entries[idx] = 0
        else:
            sol_entries[idx] =  entries[idx] = True

    return sol_entries, entries


def get_curr_grid_vals(entries, used_spots, sol=None):
    """Gets current values in Sudoku puzzle

    Args:
    sol (numpy.ndarray): solution of Sudoku puzzle
    used_spots (list):  indices of cells with given clues
    """
    curr_grid_vals = np.asarray(list(entries.values())).reshape((9, 9))

    if sol is not None:
        for key in used_spots:
            idx = tuple(elem // 60 for elem in key)
            curr_grid_vals[idx] = sol[idx]

    return curr_grid_vals


