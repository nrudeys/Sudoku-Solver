import numpy as np
import random
import solve_dataset as sd
import vertify_validness as verify


def gen_puzzle(init_min, init_max, min_loop, max_loop, max_val):
    """Generates an incomplete Sudoku puzzle

    This function takes the arguments and passes it to the 
    remove_entriesfunction, the given values indicate how many entries
    to remove initially (values depend on selected "mode") and within a
    loop

    Args:
        init_min (int): initial min value for removing values
        init_max (int): initial max value for removing values
        min_loop (int): min value for removing values 
        max_loop (int): max value for removing values
        max_val (int): max value of entries to be removed from grid
    """

    grid = np.zeros((9, 9), dtype=int)

    # Fill diagonal
    for i in range(3):
        grid[3*i:(3*i) + 3, 3*i:(3*i) + 3] = (
            np.random.choice(np.arange(1, 10), replace=False, size=(3, 3))
        )

    # Fill in rest of the grid
    completed_puzzle = sd.solve_puzzle_helper(grid)

    remove_k_entries(grid, init_min, init_max, min_loop, max_loop, max_val)

    return grid


def remove_k_entries(grid, init_min, init_max, min_loop, max_loop, max_val):
    """Removes entries from a completed Sudoku puzzle grid

    This function remove K entries from the grid by using the int args
    passed in. These values indicate the difficultly mode selected by
    a user.

    >>EASY MODE: 32 to 42 entries are removed
    >>MED MODE: 43 to 53 entries are removed
    >>HARD MODE: 54 to 64 entries are removed

    Args:
        grid (numpy.ndarray): 2D list to represent the Sudoku puzzle
        init_min (int): initial min value for removing values
        init_max (int): initial max value for removing values
        min_loop (int): min value for removing values 
        max_loop (int): max value for removing values
        max_val (int): max value of entries to be removed from grid
    """

    count = 0
    k = random.randint(init_min, init_max)

    for row in [i for i in range(9)]:
        while count + k > max_val:
            k = random.randint(min_loop, max_loop)

        count += k

        # Removing K entries
        delete = set(random.sample(range(1, len(grid[row]) + 1), k))
        grid[row] = [0 if x in delete else x for x in grid[row]]

        # Selecting k randomly for each row
        k = random.randint(min_loop, max_loop)
    return grid
