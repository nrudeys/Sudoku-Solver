import random
import numpy as np

#Global variables 
grid_indices = [i for i in range(9)]
possible_nums = [i for i in range(1,10)]

#Generating sudoku puzzle w/ complete solution, first filling diagonal square then non-diagonal
def fill_grid():

    #Creating empty dataset to represent grid (2D-matrix)
    grid = [[0 for row in range(9)] for col in range(9)]

    fill_diagonal(grid)

    #Fill the rest of the grid        
    completed_puzzle = fill_nondiagonal(grid)

    #Print values
    #print("Complete")
    #print_grid(grid)

    remove_entries(grid)
    #print("Removed")
    #print_grid(grid)
    return grid
 
#Helper function to fill rest of grid, using backtracking algo
def fill_nondiagonal(grid):

    #Base case, checking if we reached a solution
    if table_filled(grid):
        return True
    else:

        #Locating the next empty cell 
        (row, col) = located_next_empty(grid)
        
        #Going through possible nums and checking if it is valid, we insert num into cell
        #and do a recursive call for the next empty cell. If we reach a point where all the 
        #all possible combos are tried and no solution is reached, we backtrack and try to
        #update the cell with the next possible number. The point of this is to try each possible
        #combination to reach a solution
        for num in possible_nums:
            if check_num_is_valid(grid, num, row, col) and not square_has_num(grid, num, row, col):
                grid[row][col] = num

                #We found a solution
                if fill_nondiagonal(grid):
                    return True
                
                #No solution is reach, reset cell to be empty
                grid[row][col] = 0
        #All combos were tried with a given num and no solution was reached
        return False                

#Removing k entries from completed puzzle
def remove_entries(grid):
    #Since we need at least 17 clues, we can remove up to 64 entries
    #Going to remove around 40 to 64 to avoid cases with too little or many removed

    count = 0

    for row in grid_indices:
        #Selecting k randomly for each row
        k = random.randint(5,8)
        
        while count + k > 64:
            #Avoiding 8 since we don't want a case in which its all 8 makes a loop
            k = random.randint(4,6)           
        count+=k
        delete = set(random.sample(range(1,len(grid[row])+1), k))
        grid[row] = [num if num not in delete else 0 for num in grid[row]]
    print(81-count)
    return grid

#Looking for the next empty cell by checking each cell one by one 
def located_next_empty(grid):
    for row in grid_indices:
        for col in grid_indices:
            if grid[row][col]==0:
                return (row, col)
    

#Checking if all entries in the grid have a value from 1 to 9 (No zeros)
def table_filled(grid):
    for row in grid_indices:
        for col in grid_indices:
            if grid[row][col]==0:
                return False
    return True


#Helper function for checking if num is not already in row, col, or square
def check_num_is_valid(grid, num, grid_row, grid_col):
    if num in set(grid[grid_row]) or num_in_col(grid, num, grid_col):
        return False
    else:
        return True

#Check col has given num
def num_in_col(grid, num, col):
    for row in grid_indices:
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

#Visual respresentation of sudoku puzzle
def print_grid(grid):
    for row in grid_indices:
        for col in grid_indices:
            print(str(grid[row][col]) + " ", end='')
        print("")
    print("")

def fill_diagonal(grid):
    #Going through each cell in grid (filling diagonal)
    for row in grid_indices:

        #Get upper left cell for square according to row #
        r = 3*round(row//3)
        
        #Going to check the 3 columns in current square
        for col in range(r, r+3):

            #Generating random number from 1 to 9
            num = random.randint(1,9)

            #Since we are only doing diagonal squares, we only need to check
            #if current square does not contain chosen num, we only update the cell
            #with num once we confirm it's valid
            while square_has_num(grid, num, row, col):
                num = random.randint(1,9)
        
            grid[row][col] = num