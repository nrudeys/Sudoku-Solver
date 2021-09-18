import numpy as np
import vertify_validness as verify


def solve_puzzle(grid):
    """Fill in remaining entries the provided Sudoku puzzle grid

    This function fills in the remaining entries through using a
    helper function

    Args:
        grid (numpy.ndarray): 2D list which is representation of
        Sudoku puzzle

    Raises:
        ValueError: solution is not found or invalid board is given
        (board with duplicates or with less than 17 clues)
    """

    if check_duplicates(grid):
        raise ValueError("Has Duplicates")
    elif np.count_nonzero(grid) < 17:
        raise ValueError("Not Enough Clues")
    elif solve_puzzle_helper(grid):
        return grid
    else:
        raise ValueError("No Solution")


def solve_puzzle_helper(grid):
    """Fill in remaining entries the provided Sudoku puzzle grid

    This function fills in the remaining entries using a 
    backtracking algorithm

    Args:
        grid (numpy.ndarray): 2D list which is representation of 
        Sudoku puzzle
    """
    # Base case, a solution has been found
    if not np.any(grid == 0):
        return True
    else:
        # Locating the next empty cell
        (row, col) = np.argwhere(grid == 0)[0]

        grid_row = grid[row, :]
        grid_col = grid[:, col]

        sq_x = 3 * round((row - 1) / 3)
        sq_y = 3 * round((col - 1) / 3)

        sq = grid[sq_x:sq_x + 3, sq_y:sq_y + 3]

        for num in np.arange(1, 10):
            if not check_num(grid, num, grid_col, grid_row, sq):
                grid[row][col] = num

                # Recursive call
                if solve_puzzle_helper(grid):
                    return True

                # No solution is found, reset cell to be empty
                grid[row][col] = 0

        return False


def check_num(grid, num, grid_col, grid_row, sq):
    """Checks for num is in column, row, or square of grid

    Args:
        grid (numpy.ndarray): 2D list which is representation of 
        Sudoku puzzle
        num (int): number that is being checked for
        grid_col (numpy.ndarray): 1D list representation of column
        grid_row (numpy.ndarray): 1D list representation of row
        sq (numpy.ndarray): 1D list representation of 3x3 square box
    """

    return num in grid_row or num in grid_col or num in sq


def check_duplicates(grid):
    """Checks for duplicate values in column, row, and squares of grid

    Args:
        grid (numpy.ndarray): 2D list which is representation of 
        Sudoku puzzle
    """

    # Dividing grid into square portions
    all_squares = grid.reshape(3, 3, -1, 3).swapaxes(1, 2).reshape(-1, 3, 3)

    for x in range(9):
        row = np.unique(grid[x], return_counts=True)
        col = np.unique(grid[:, x], return_counts=True)
        sq = np.unique(all_squares[x], return_counts=True)

        if row[0][0] == 0:
            # There are zero entries, ignore the count of zero values
            # (same cases in col and sq checks below)
            if np.any(row[1][1:] > 1):
                return True
        elif np.any(row[1] > 1):
            return True

        if col[0][0] == 0:
            if np.any(col[1][1:] > 1):
                return True
        elif np.any(col[1] > 1):
            return True

        if sq[0][0] == 0:
            if np.any(sq[1][1:] > 1):
                return True
        elif np.any(sq[1] > 1):
            return True

    return False
