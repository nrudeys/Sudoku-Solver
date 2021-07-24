from gen_dataset import *

#Using backtracking algo 
def solve_puzzle(grid):
    if solve_puzzle_helper(grid):   
        print_grid(grid)
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

print("Final call")
grid = fill_grid()
solve_puzzle(grid)
