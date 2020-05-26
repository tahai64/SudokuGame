#Standard starting grid for Sudoku puzzle

board = [

  [0,7,0,4,0,5,6,9,0],
  [9,2,4,7,6,0,8,0,0],
  [1,0,5,0,0,8,7,0,0],
  [0,3,8,0,5,7,0,0,0],
  [0,0,0,0,0,0,0,7,3],
  [0,4,7,0,9,0,1,2,0],
  [4,0,9,6,0,2,0,0,1],
  [7,0,0,8,3,0,4,0,9],
  [3,1,0,5,4,9,0,0,7]

]

# Making the Sudoku grid with this function 

def print_grid(bo):
    
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("---------------")
            
        for j in range(len(bo[0])): 
            if j % 3 == 0  and j != 0:
                print(" | ", end ="")
        
            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + "", end = "")


# Function used to find the empty spaces within the grid 

def locate_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
             if bo[i][j] == 0:
                 return(i, j)
    return None


# Checking to see if number is valid for its spot on the grid
# First part checks for row and second part checks for column 
# Final part checks for each box

def valid(bo, num, pos):
    for i in range (len(bo[0])):
        if bo[pos[0]] [i] == num and pos[1] != i:
            return False
    
    for i in range (len(bo)):
        if bo[i] [pos[1]] == num and pos[0] != i:
            return False
    
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    
    for i in range(box_y * 3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i , j) != pos:
                return False
    
    return True
    

# Backtracking algo used to solve the Puzzle

def solve(bo):
    locate = locate_empty(bo)
    if not locate:
        return True
    else:
        row, colm = locate

# Adds values from 1 to 10 into the empty space to see if it is 
# the correct number for that spot. If it is the right number
# for the spot then we keep the number there and move onto the 
# next empty space. If not then backtrack and reset number prior 
# because it is not a valid number (reset number try with another)
    
    for i in range(1,10):
        if valid (bo, i, (row, colm)):
            bo[row][colm] = i 
            
            if solve(bo):
                return True
                
            
            bo[row][colm] = 0
    
    return False


print_grid(board)

solve(board)

print("-------------------")
print("-------------------")
print("-------------------")
print("-------------------")
print("-------------------")

print_grid(board)
