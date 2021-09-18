import numpy as np


def verify_validness(grid):
    """Verify if a completed Sudoku puzzle is valid

    This function checks the validness of a Sudoku puzzle by checking
    if each row, col, and sq has the sum of 45. (There are no 
    duplicate values due to the way the boards are generated/solved)

    >> 1 + 2 + ... + 9 = 45

    Args:
        grid (numpy.ndarray): 2D list which is representation of
        Sudoku puzzle
    """

    # Dividing grid into square portions
    all_squares = grid.reshape(3, 3, -1, 3).swapaxes(1, 2).reshape(-1, 3, 3)

    for i in range(9):
        if not (np.sum(grid[i]) == np.sum(grid[:, i])
                == np.sum(all_squares[i]) == 45):
            return False

    return True
