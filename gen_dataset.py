import random

def fill_grid():
    #Creating empty dataset to represent grid (2D-matrix)
    grid = [[0]*9]*9

    #Backtracking algorithm for generating a puzzle with a solution
    for row in range(9):
        for col in range(9):
            #Choosing and assigning valid number from 1-9 that could go in square
            num = random.randint(1,9)

            #If num is valid, we insert otherwise else leave it empty
            if check_num_is_valid(grid, num, row, col):
                grid[row][col] = num
    #Solved sudoku, copy values (no reference)
    res_grid = grid[:]

    #<Removing k entries>
    
    return grid


#Helper function for checking if num is not already in row, col, or square
def check_num_is_valid(grid, num, grid_row, grid_col):

    if num in grid[grid_row] or num in grid[grid_col] or square_has_num(grid, num, grid_row, grid_col):
        return False
    else:
        return True

def square_has_num(grid, num, grid_row, grid_col):
    #Get the 3x3 rows and cols for the input by using nearest multiple of 3
    #To get nearest mult of 3 used formula: base*round(num-1/base)
    row = 3*round((grid_row-1)/3)
    col = 3*round((grid_col-1)/3)

    for row_cell in range(row, row+3):
        for col_cell in range(col, col+3):
            if num in grid[row_cell][col_cell]:
                return False
    
    return True




    


