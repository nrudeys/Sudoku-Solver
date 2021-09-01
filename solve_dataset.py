from gen_dataset import *
from board_setup import *
import numpy as np

#Using backtracking algo 
def solve_puzzle(grid):
    if check_duplicates(np.array(grid), np.array(grid).reshape(3, 3, -1, 3).swapaxes(1,2).reshape(-1, 3,3)):
        raise ValueError("Invalid board -- contains duplicates")
    elif np.count_nonzero(grid) < 17:
        raise ValueError("Invalid board -- not enough provided clues")
    elif solve_puzzle_helper(grid):   
        return grid
    else:
        raise ValueError("No solution")

def solve_puzzle_helper(grid):
 #Base case, checking if we reached a solution
    if table_filled(grid):
        return True
    else:
        #Locating the next empty cell 
        (row, col) = located_next_empty(grid)

        for num in possible_nums:
            if check_num_is_valid(grid, num, row, col) and not square_has_num(grid, num, row, col):
                grid[row][col] = num

                #We found a solution
                if solve_puzzle_helper(grid):
                    return True
                
                #No solution is reach, reset cell to be empty
                grid[row][col] = 0
        #All combos were tried with a given num and no solution was reached
        return False       

def check_duplicates(grid, squares):
    for x in range(9):
        row = np.unique(grid[x], return_counts = True)
        col = np.unique(grid[:,x], return_counts = True)
        sq = np.unique(squares[x], return_counts = True)

        if row[0][0] == 0:
            if (np.any(row[1][1:] > 1)):
                return True
        elif (np.any(row[1] > 1)):
            return True

        if col[0][0] == 0:
            if (np.any(col[1][1:] > 1)):
                return True
        elif (np.any(col[1] > 1)):
            return True
        
        if sq[0][0] == 0:
            if (np.any(sq[1][1:] > 1)):
                return True
        elif (np.any(sq[1] > 1)):
            return True

    return False

#grid.reshape(3, 3, -1, 3).swapaxes(1,2).reshape(-1, 3,3))