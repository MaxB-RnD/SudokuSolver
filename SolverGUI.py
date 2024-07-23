# GUI MAIN CODE FOR RUNNING THE UX SUDOKU SOLVER
from Grid import *
import pygame
import os
import sys
pygame.font.init()


# REDRAW PYGAME WINDOW
def redrawWindow(win, board, reset):
    win.fill((255, 255, 255))
    board.draw(reset)
    pygame.display.update()


# GET THE ABSOLUTE PATH TO A RESOURCE
def resource_path(relative_path):
    try:
        # PyInstaller Creates a Temp Folder & Stores Path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# DISPLAY THE INSTRUCTION SCREEN
def instructionScreen(win, instruction):
    # Load In Instruction Image
    screenPath = resource_path('./Screens/Start_Screen.png')
    instructionImage = pygame.image.load(screenPath)
    resizedImage = pygame.transform.smoothscale(instructionImage, (540, 540))

    # Render the Image
    while instruction:
        # Display the Instruction Screen
        for event in pygame.event.get():
            # Dismiss the Screen when Space is Pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    instruction = False
            
            # Quit the Game When X is Selected
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        # Clear the window
        win.fill((255, 255, 255))
        
        # Blit the image
        win.blit(resizedImage, (0, 0))

        # Update the Display
        pygame.display.update()


# CONTROLS FOR BACKSPACE FUNCTIONALITY
def backspace(board):
    if board.selected:
        i, j = board.selected
        # If cube is not empty, clear the value
        if board.cubes[i][j].value != 0:  
            board.cubes[i][j].set(0)
        # If cube is empty, move selection back
        else:  
            if j > 0:
                j -= 1
            else:
                j = board.cols - 1
                if i > 0:
                    i -= 1
                else:
                    i = board.rows - 1
            board.select(i, j)
    # Return Updated Key
    return None


# CONTROLS FOR TAB FUNCTIONALITY
def tab(board):
    if board.selected:
        i, j = board.selected
        if j < board.cols - 1:
            j += 1
        else:
            j = 0
            if i < board.rows - 1:
                i += 1
            else:
                i = 0
        board.select(i, j)
    # Return Updated Key
    return None


# CONTROLS FOR BOARD SOLVING (RETURN KEY) FUNCTIONALITY
def solveBoard(win, board, key, fail, reset):
    # Load In Unsolvable Image
    screenPath = resource_path('./Screens/Unsolvable.png')
    unsolvableImage = pygame.image.load(screenPath)
    resizedImage = pygame.transform.smoothscale(unsolvableImage, (540, 540))

    # If the Board is Solvable
    if  board.solve():
        # Update board with Solved Values
        board.updateBoard()  
        board.select(0, 0)
        return key, reset

    # If the Board is Unsolvable
    else:
        # Instruction Screen Loop
        while fail:
            # Display the Instruction Screen
            for event in pygame.event.get():
                # Dismiss the Screen when Space is Pressed OR when R is Pressed
                if event.type == pygame.KEYDOWN:
                    # Reset the board (clear all values)
                 if event.key == pygame.K_SPACE or event.key == pygame.K_r:
                    fail = False
                    reset = False
                    board.clearBoard()
                    board.select(0, 0)
                    key = None
                    return key, reset
                
                # Quit the Game When X is Selected
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            
            # Clear the window
            win.fill((255, 255, 255)) 
            
            # Blit the image
            win.blit(resizedImage, (0, 0))

            # Update the Display
            pygame.display.update()


# MAIN FUNCTION
def main():
    # Initialize Pygame Window
    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)

    # Initalise Control Variables
    key = None              # Current Key Press Value
    run = True              # Main Game Loop Running Condition
    instruction = True      # Display Instruction Screen
    firstPass = True        # Start of New Game Condition
    reset = False           # Enter has Been Pressed, Hide Square
    fail = True             # Board Cannot Be Solved

    # Display Instruction Screen
    instructionScreen(win, instruction)
    
    # Main Game Loop
    while run:
        for event in pygame.event.get():
            # Select Top Square To Begin
            if firstPass == True:
              board.select(0, 0)
              firstPass = False
            
            # Quit the Game When X is Selected
            if event.type == pygame.QUIT:
                run = False

            # Keyboard Input Handling
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9

                # Reset the board (clear all values)
                elif event.key == pygame.K_r:
                    reset = False
                    board.clearBoard()
                    board.select(0, 0)
                    key = None
                
               # Delete the Current Value of the Cube or Move Back a Square
                elif event.key == pygame.K_BACKSPACE:
                    key = backspace(board)
                
                # Tab the Square from Left to Right
                if event.key == pygame.K_TAB:
                    key = tab(board)

                # Solve the Board
                if event.key == pygame.K_RETURN:
                    # Reset the Square to Top Corner
                    reset = True

                    # Display Solved Board
                    key, reset = solveBoard(win, board, key, fail, reset)
                    fail = True

            # Mouse Click Handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        # Draw in a Value
        if board.selected and key is not None:
            board.place(key)

        # Update the Window
        redrawWindow(win, board, reset)
        pygame.display.update()

    # End the Program
    pygame.quit()


# CODE TO RUN MAIN FUNCTION
if __name__ == "__main__":
    main()
