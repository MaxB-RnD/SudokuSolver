# GRID CLASS FOR THE SUDOKU SOLVER WHICH CHARACTERISES THE 9 X 9 GRID
from Cubes import *  
from Solver import *  

# DEFINE THE GRID CLASS
class Grid:
    # Initialise Variables for the Grid class
    rows = 9
    cols = 9


    # CONSTRUCTOR DEFINITION
    def __init__(self, rows, cols, width, height, win):
        self.rows = rows                                                                        # Number of rows in the grid
        self.cols = cols                                                                        # Number of columns in the grid
        self.width = width                                                                      # Width of the grid
        self.height = height                                                                    # Height of the grid
        self.model = None                                                                       # Model representing the current state of the grid
        self.cubes = [[Cube(0, i, j, width, height) for j in range(cols)] for i in range(rows)] # 2D list of Cube objects
        self.updateModel()                                                                     # Update the model to reflect the current grid state
        self.selected = None                                                                    # Currently selected cube
        self.win = win                                                                          # Pygame window where the grid is drawn


    # UPDATE THE MODEL TO MATCH THE CURRENT GRID STATE
    def updateModel(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]


    # PLACE A NUMBER IN THE SELECTED POSITION
    def place(self, num):
        # Get the Selected Row & Column
        row, col = self.selected  

        # If the Cube is Empty
        if self.cubes[row][col].value == 0:  
            self.cubes[row][col].set(num)    # Set the Cube's Value
            self.updateModel()              # Update the Model
            return True
        else:
            return False


    # SOLVE THE SUDOKU GRID
    def solve(self):
        # Update the Model to Match the Current Grid State
        self.updateModel()   

        # If the Solve Function Finds a Solution    
        if solve(self.model):     
            # Update the Board to Reflect the Solution
            self.updateBoard()   
            return True
        else:
            return False


    # UPDATE THE BOARD TO MATCH THE SOLVED MODEL
    def updateBoard(self):
        for i in range(self.rows):
            for j in range(self.cols):
                # If the Cube is Empty
                if self.cubes[i][j].value == 0:  
                    # Set the cube's Value & Mark it as Solved
                    self.cubes[i][j].set(self.model[i][j], is_solved=True)
                     # Draw the Change on the Screen  
                    self.cubes[i][j].drawChange(self.win)          


    # DRAW THE ENTIRE GRID
    def draw(self, reset):
        gap = self.width / 9
        for i in range(self.rows):
            for j in range(self.cols):
                # Draw Each Cube
                self.cubes[i][j].draw(self.win, reset)  

        # Draw Gridlines
        for i in range(self.rows + 1):
             # Make Every Third Line Thicker
            thick = 4 if i % 3 == 0 and i != 0 else 1 

            # Horizontal Lines
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick) 

            # Vertical Lines 
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)  


    # SELECT A CUBE BASED ON ROW AND COLUMN
    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                # Deselect All Cubes
                self.cubes[i][j].selected = False  

        # Select the Specified Cube
        self.cubes[row][col].selected = True   

         # Update the Selected Attribute    
        self.selected = (row, col)                


    # DETERMINE WHICH CUBE WAS CLICKED BASED ON POSITION
    def click(self, pos):
        # If Click is Within the Grid Area
        if pos[0] < self.width and pos[1] < self.height:  
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap

            # Return the Row & Column of the Clicked Cube
            return (int(y), int(x))  
        else:
            return None


    # CLEAR THE ENTIRE BOARD
    def clearBoard(self):
        for i in range(self.rows):
            for j in range(self.cols):
                # Set Each Cube's Value to 0
                self.cubes[i][j].set(0)  
        
        # Update the Model to Reflect the Cleared Board
        self.updateModel()              
