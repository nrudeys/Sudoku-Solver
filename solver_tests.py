import numpy as np
import solve_dataset as sd


def dup_col_test():
    # Duplicate in first and second col
    grid = np.asarray([
        [5, 6, 8, 1, 2, 3, 4, 7, 9],
        [5, 2, 1, 0, 0, 9, 3, 8, 0],
        [0, 0, 3, 0, 6, 8, 2, 5, 0],
        [0, 0, 6, 2, 0, 1, 0, 4, 7],
        [1, 4, 0, 0, 0, 6, 5, 0, 0],
        [8, 7, 0, 0, 0, 5, 0, 0, 2],
        [0, 0, 4, 8, 3, 0, 7, 6, 0],
        [0, 3, 0, 6, 1, 7, 0, 0, 0],
        [0, 8, 7, 9, 5, 0, 0, 2, 0]
    ])

    try:
        sd.solve_puzzle(grid)
    except ValueError as err:
        return True

    return False


def dup_row_test():
    grid = np.asarray([
        [5, 6, 8, 5, 2, 3, 4, 7, 9],
        [0, 2, 1, 0, 0, 9, 3, 8, 0],
        [0, 0, 3, 0, 6, 8, 2, 5, 0],
        [0, 0, 6, 2, 0, 1, 0, 4, 7],
        [1, 4, 0, 0, 0, 6, 5, 0, 0],
        [8, 7, 0, 0, 0, 5, 0, 0, 2],
        [0, 0, 4, 8, 3, 0, 7, 6, 0],
        [0, 3, 0, 6, 1, 7, 0, 0, 0],
        [0, 8, 7, 9, 5, 0, 0, 2, 0]
    ])

    try:
        sd.solve_puzzle(grid)
    except ValueError as err:
        return True

    return False


def dup_sq_test():
    grid = np.asarray([
        [5, 6, 8, 1, 2, 3, 4, 7, 9],
        [0, 5, 1, 0, 0, 9, 3, 8, 0],
        [0, 0, 3, 0, 6, 8, 2, 5, 0],
        [0, 0, 6, 2, 0, 1, 0, 4, 7],
        [1, 4, 0, 0, 0, 6, 5, 0, 0],
        [8, 7, 0, 0, 0, 5, 0, 0, 2],
        [0, 0, 4, 8, 3, 0, 7, 6, 0],
        [0, 3, 0, 6, 1, 7, 0, 0, 0],
        [0, 8, 7, 9, 5, 0, 0, 2, 0]
    ])

    try:
        sd.solve_puzzle(grid)
    except ValueError as err:
        return True

    return False


def not_enough_given_clues_test():
    # Needs at least 17 clues (only provided 9)
    grid = np.asarray([
        [5, 6, 8, 1, 2, 3, 4, 7, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])

    try:
        sd.solve_puzzle(grid)
    except ValueError as err:
        return True

    return False


def unsolveable_puzzle_test():
    # No solution
    grid = np.asarray([
        [1, 2, 3, 0, 9, 0, 0, 0, 0],
        [4, 5, 6, 0, 8, 0, 0, 0, 0],
        [0, 8, 9, 0, 7, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 0, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0]
    ])

    try:
        sd.solve_puzzle(grid)
    except ValueError as err:
        return True
    return False


def main():
    assert dup_row_test() == True, "Should throw error - duplicate is in ROW"
    assert dup_col_test() == True, "Should throw error - duplicate is in COL"
    assert dup_sq_test() == True, "Should throw error - duplicate is in SQ"
    assert unsolveable_puzzle_test() == True, "Should have no solution"
    assert not_enough_given_clues_test() == True, "Should have throw error, \
        insufficient amount of clues"


if __name__ == "__main__":
    main()
