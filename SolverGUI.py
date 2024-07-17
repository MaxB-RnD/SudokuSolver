# GUI FOR SUDOKU SOLVER FUNCTION
import pygame
import time

# Import solver functions
from solver import solve, valid, find_empty  
pygame.font.init()



# CREATE A GRID OBJECT/BOARD SPACE
class Grid:
    # INITIALISE THE SUDOKU GRID
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None

        # Initialise Grid with Empty Values
        self.cubes = [[Cube(0, i, j, width, height) for j in range(cols)] for i in range(rows)]  

        # Initialise the Model Based on Initial Cube Values
        self.update_model() 

        # Currently Selected Cube (row, col)
        self.selected = None 

        # Pygame Window Surface
        self.win = win  

    
    # UPDATE THE INTERNAL MODEL/BOARD TO REFLECT CURRENT VALUES
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    # PLACE A VALUE IN THE SELECTED CUBE
    def place(self, num):
        # Place Value in Cube
        row, col = self.selected

        # Check if Value is Empty
        if self.cubes[row][col].value == 0:
            # Set Square to Value
            self.cubes[row][col].set(num)
            self.update_model()
            return True
            
        # If Value is Not Empty Don't Allow Chnage
        else:
            return False

    
    # SOLVE THE CURRENT BOARD
    def solve(self):
        # Update the Internal Board
        self.update_model()

        # If the Board Solves Update the Board
        if solve(self.model):
            self.update_board()
            return True
        else:
            return False

    
    # UPDATE THE BOARD TO REFLECT THE SOLVED STATE
    def update_board(self):
        # Transfer the Solve State Board to the GUI
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    self.cubes[i][j].set(self.model[i][j])
                    self.cubes[i][j].draw_change(self.win, False)

    
    # DRAW THE GRID AND CUBES
    def draw(self):
        # Define Grid Size
        gap = self.width / 9

        # Set Line Thickness
        for i in range(self.rows + 1):
            # Box Edge Line
            if i % 3 == 0 and i != 0:
                thick = 4
            # Normal Line
            else:
                thick = 1
                
            # Draw the Line on the Board
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw the Value in the Cube
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    
    # SELECT A CUBE
    def select(self, row, col):
        # Loop Through the Entire Board
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
                
        # Select the Current Square to Take an Input Value
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    
    # GET POSITION OF CLICKED CUBE
    def click(self, pos):
        # Bounds Check the Click
        if pos[0] < self.width and pos[1] < self.height:
            # Return the Co-ordinates
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            # Return Nothing if Out of Bounds
            return None

    
    # CLEAR THE TEMPORARY VALUE IN A CUBE
    def clear(self):
        # Select the Row and Col
        row, col = self.selected

        # Check Cube is Not empty Return Value
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    
    # SKETCH A VALUE IN A CUBE
    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    
    # CHECK IF THE BOARD IS COMPLETED
    def is_finished(self):
        # Loop Through Board
        for i in range(self.rows):
            for j in range(self.cols):
                # Look for Empty Squares
                if self.cubes[i][j].value == 0:
                    return False

        # No Empty Squares Board is Complete
        return True



# DEFINE THE CUBE CLASS 
class Cube:
    rows = 9
    cols = 9
    
    # INITALISE A SINGLE CUBE IN THE SUDOKU GRID
    def __init__(self, value, row, col, width, height):
        # Initialise the Variables
        self.value = value
        self.temp = 0  # Temporary Value (for sketching)
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False  # Whether this Cube is Currently Selected

    
    # DRAW THE CUBE ON THE PYGAME INTERFACE
    def draw(self, win):
        # Choose and Set Font and Spacing
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # When Valid Display Font
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))

        # If Not Render as Black
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        # Draw the Cube Borders
        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    
    # DRAW CHANGES TO THE CUBE WHEN TRANSITIONING TO SOLVED
    def draw_change(self, win, g=True):
        # Set Fonts and Spacing
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # Draw the Window & Render the Text
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

    
    # SET THE VALUE OF THE CUBE
    def set(self, val):
        self.value = val

    
    # SET THE TEMPORARY VALUE OF THE CUBE
    def set_temp(self, val):
        self.temp = val


# REDRAW THE PYGAME WINDOW
def redraw_window(win, board):
    win.fill((255,255,255))
    board.draw()



# MAIN FUNCTION TO RUN THE SUDOKU SOLVER GUI
def main():
    # Initalise the Game Board
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True

    # Game Run Loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
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
                if event.key == pygame.K_RETURN:
                    # Board is Ready to Be Solved
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                        key = None

                        if board.is_finished():
                            print("Game over")
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not board.solve():
                        print("Board is unsolvable")
                        font = pygame.font.SysFont("comicsans", 60)
                        text = font.render("Unsolvable!", 1, (255, 0, 0))
                        win.blit(text, (540 // 2 - text.get_width() // 2, 600 // 2 - text.get_height() // 2))
                        pygame.display.update()
                        pygame.time.delay(2000)  # Display message for 2 seconds

        if board.selected and key is not None:
            board.sketch(key)

        redraw_window(win, board)
        pygame.display.update()

    pygame.quit()



# CALL THE MAIN FUNCTION
if __name__ == "__main__":
    main()
