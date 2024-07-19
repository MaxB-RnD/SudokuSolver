# GUI MAIN CODE FOR RUNNING THE UX SUDOKU SOLVER
from Grid import *
pygame.font.init()

    
# Redraw Pygame Window
def redrawWindow(win, board, reset):
    win.fill((255, 255, 255))
    board.draw(reset)
    pygame.display.update()

    
# Main Function
def main():
    # Initialize Pygame Window
    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)
    key = None              # Current Key Press Value
    run = True              # Main Game Loop Running Condition
    instruction = True      # Display Instruction Screen
    firstPass = True        # Start of New Game Condition
    reset = False           # Enter has Been Pressed, Hide Square

    # Instruction Screen Loop
    while instruction:
        # Display the Instruction Screen
        for event in pygame.event.get():
            # Load In Instruction Image
            instructionImage = pygame.image.load('./Screens/Start2.jpg')
            resizedImage = pygame.transform.scale(instructionImage, (540, 540))

            # Dismiss the Screen when Space is Pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    instruction = False
            
        # Clear the window
        win.fill((255, 255, 255))  # Fill with white or any background color
        
        # Blit the image
        win.blit(resizedImage, (0, 0))  # Adjust the position as neede

        # Update the Display
        pygame.display.update()


    # Main Game Loop
    while run:
        for event in pygame.event.get():
            # Select Top Square To Begin
            if firstPass == True:
              board.select(0, 0)
              firstPass = False
              
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
                        key = None

                
                # Solve the Board
                if event.key == pygame.K_RETURN:
                    reset = True
                    # If the Board is Not Solvable
                    if not board.solve():
                        print("Board is Unsolvable")
                        font = pygame.font.SysFont("comicsans", 60)
                        text = font.render("Unsolvable!", 1, (255, 0, 0))
                        win.blit(text, (540 // 2 - text.get_width() // 2, 540 // 2 - text.get_height() // 2))
                        pygame.display.update()
                        pygame.time.delay(2000)
                    else:
                        board.updateBoard()  # Update board with solved values
                        board.select(0,0)

                # Tab the Square from Left to Right
                if event.key == pygame.K_TAB:
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
                    key = None
            
            # Mouse Click Handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key is not None:
            board.place(key)

        redrawWindow(win, board, reset)
        pygame.display.update()

    pygame.quit()

# Run Main Function if Script is Executed Directly
if __name__ == "__main__":
    main()
