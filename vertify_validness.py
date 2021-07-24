from solve_dataset import *

#Generating a solution
grid = solve_puzzle(fill_grid())

#We can verify the correctness of a sudoku puzzle by checking if each row, col, and square have the sum of 45
#(already checking for uniqueness earlier on)
def verify_validness(grid):

    for row in grid_indices:
      
        #Verify row equals 45
        if sum(grid[row]) != 45:
            return False
      
        for col in grid_indices:
      
            #Verify col equals 45 
            if not verify_col(grid, col):
                return False
            
            #Verify square equals 45  
            if not verify_square(grid, row, col):
                return False
    return True

#Helper function checking the entries of column
def verify_col(grid, col):
    sum = 0
    for row in grid_indices:
        #Went over already don't need to go through rest of loop
        if sum > 45:
            return False
        sum+=grid[row][col]
    #Check for if sum is under 45
    if sum != 45:
        return False
    return True

#Helper function checking the entries of square
def verify_square(grid, grid_row, grid_col):
    #Get the 3x3 rows and cols for the input by using nearest multiple of 3
    #To get nearest mult of 3 used formula: base*round(num-1/base)
    row = 3*round((grid_row-1)/3)
    col = 3*round((grid_col-1)/3)

    sum = 0
    for row_cell in range(row, row+3):
        for col_cell in range(col, col+3):

           #We don't need to keep going through loop as we know the entries of the square are incorrect
           #as we are over the expected value
           if sum > 45:
               return False

           sum+=grid[row_cell][col_cell]
    
    #Square solution is incorrect, sum is under what is expected
    if sum != 45:
        return False

    return True

print(verify_validness(grid))