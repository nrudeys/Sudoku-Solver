import random

def fill_grid():
    #Creating empty dataset to represent grid (2D-matrix)
    grid = [[0 for row in range(9)] for col in range(9)]

    for row in range(9):
        r = 3*round(row//3)
        
        for col in range(r, r+3):
            num = random.randint(1,9)

            while square_has_num(grid, num, row, col):
                num = random.randint(1,9)
        
            grid[row][col] = num
    fill_nondiagonal(grid)
    print_grid(grid)
    return grid
 
def fill_nondiagonal(grid):
    if table_filled(grid):
        return True
    else:
        (row, col) = located_next_empty(grid)
        
        for num in range(1,10):
            if check_num_is_valid(grid, num, row, col):
                grid[row][col] = num
                if fill_nondiagonal(grid):
                    return True
                grid[row][col] = 0
        return False                

def located_next_empty(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0:
                return (row, col)
    

def table_filled(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col]==0:
                return False
    return True


#Helper function for checking if num is not already in row, col, or square
def check_num_is_valid(grid, num, grid_row, grid_col):
    if num in set(grid[grid_row]) or num_in_col(grid, num, grid_col):
        return False
    else:
        return True

#Check col
def num_in_col(grid, num, col):
    for row in range(9):
        if grid[row][col] == num:
            return True
    return False

#Helper function for checking if square portions already contain given num
def square_has_num(grid, num, grid_row, grid_col):
    #Get the 3x3 rows and cols for the input by using nearest multiple of 3
    #To get nearest mult of 3 used formula: base*round(num-1/base)
    row = 3*round((grid_row-1)/3)
    col = 3*round((grid_col-1)/3)

    for row_cell in range(row, row+3):
        for col_cell in range(col, col+3):
           if grid[row_cell][col_cell]==num:
                return True

    return False

def print_grid(grid):
    for row in range(9):
        for col in range(9):
            print(str(grid[row][col]) + " ", end='')
        print("")
    print("")

fill_grid()
