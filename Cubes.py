# CUBE CLASS FOR THE SUDOKU SOLVER WHICH MAKE UP THE 9 X 9 GRID
import pygame

# DEFINE THE CUBE CLASS
class Cube:
    # Initialise Variables for the Cube class
    rows = 9
    cols = 9


    # CONSTRUCTOR DEFINITION
    def __init__(self, value, row, col, width, height):
        self.value = value           # Initial Value of the Cube
        self.row = row               # Row Position of the Cube
        self.col = col               # Column Position of the Cube
        self.width = width           # Width of the Cube
        self.height = height         # Height of the Cube
        self.selected = False        # Whether the Cube is Currently Selected
        self.is_solved = False       # Whether the Cube is Part of the Solved Board


    # DRAW THE CUBE ON THE PYGAME INTERFACE
    def draw(self, win, reset):
        # Set the Font
        fnt = pygame.font.SysFont("comicsans", 40)  

        # Calculate the Gap Between Cubes
        gap = self.width / 9   

        # X & Y position of the Cube                     
        x = self.col * gap                         
        y = self.row * gap                         

        # Draw Background
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap))

        # Only Render the Text if self.value is Not Zero
        if self.value != 0:
            # Set Colour Based on Solved State
            colour = (128, 128, 128) if self.is_solved else (0, 0, 0)  

            # Render the Text
            text = fnt.render(str(self.value), 1, colour)              
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        # Draw Border if the Cube is Selected
        if self.selected:
            if reset:
                pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 3)
            else:
                pygame.draw.rect(win, (0, 68, 193), (x, y, gap, gap), 3)


    # DRAW CHANGES TO THE CUBE WHEN TRANSITIONING TO SOLVED
    def drawChange(self, win):
        # Set the Font
        fnt = pygame.font.SysFont("comicsans", 40)  

        # Calculate the Gap Between Cubes
        gap = self.width / 9    

        # X & Yposition of the cube                    
        x = self.col * gap                          
        y = self.row * gap                     

        # Draw the Cube with Updated Value
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap))
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))


    # SET THE VALUE OF THE CUBE
    def set(self, val, is_solved=False):
        # Set the Cube's Value
        self.value = val     

        # Update the Solved State      
        self.is_solved = is_solved 