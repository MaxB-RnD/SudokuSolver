# BACKTRACKING ALGORITHM FOR THE SUDOKU SOLVER

# FINDS AN EMPTY POSITION ON THE SUDOKU BOARD
def findEmpty(board):
    # Iterate Through the Board to Find an Empty Cell
    for i in range(len(board)):
        for j in range(len(board[0])):
            # Return the Position of the Empty Cell
            if board[i][j] == 0:
                return (i, j)  # row, col

    # Return None if No Empty Cells are Found
    return False


# CHECKS IF PLACING A NUMBER IN A SPECIFIC POSITION MAKES A VALID BOARD
def isValid(board, number, position):
    # Check the Row for Duplicates
    for i in range(len(board[0])):
        if board[position[0]][i] == number and position[1] != i:
            return False

    # Check the Column for Duplicates
    for i in range(len(board)):
        if board[i][position[1]] == number and position[0] != i:
            return False

    # Check the 3x3 Box for Duplicates
    box_x = position[1] // 3
    box_y = position[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == number and (i, j) != position:
                return False

    # If No Duplicates are Found, Return True
    return True


# FUNCTION THAT SOLVES THE GIVEN SUDOKU BOARD USING BACKTRACKING
def solveSudoku(board):
    # Find the Next Empty Cell
    find = findEmpty(board)
    
    # If There Are No Empty Cells, the Board is Solved
    if not find:
        return True
    else:
        row, col = find

    # Try Placing Numbers 1-9 in the Empty Cell
    for i in range(1, 10):
        # Check if Placing Number in (row, col) is Valid
        if isValid(board, i, (row, col)):
            # Place Number in the Cell
            board[row][col] = i

            # Recursively Try to Solve the Rest of the Board
            if solveSudoku(board):
                return True

            # If placing number doesn't lead to a solution, reset the cell
            board[row][col] = 0

    # If No Number from 1-9 Leads to a Solution, Return False
    return False