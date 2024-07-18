import pygame
import time
from solver import solve, valid, find_empty  

pygame.font.init()

# Define Grid Class
class Grid:
    rows = 9
    cols = 9

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.model = None
        self.cubes = [[Cube(0, i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.update_model()
        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, num):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(num)
            self.update_model()
            return True
        else:
            return False

    def solve(self):
        self.update_model()
        if solve(self.model):
            self.update_board()
            return True
        else:
            return False

    def update_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    self.cubes[i][j].set(self.model[i][j])
                    self.cubes[i][j].draw_change(self.win, False)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True


# Define Cube Class
class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # Only render the text if self.value is not zero
        if self.value != 0:
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (0, 68, 204), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        fnt = pygame.font.SysFont("comicsans", 40)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

    def set(self, val):
        self.value = val


# Main Function
def main():
    # Initialize Pygame Window
    win = pygame.display.set_mode((540, 540))
    pygame.display.set_caption("Sudoku Solver")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    firstPass = True

    # Main Game Loop
    while run:
        for event in pygame.event.get():
            # Select Top Square To Begin
            if firstPass == True:
              board.select(0, 0)
              firstPass = False

            # Quit the Game When Selected to Quit
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
                
                # Delete the Current Value of the Cube
                if event.key == pygame.K_BACKSPACE:
                  if board.selected:
                    i, j = board.selected
                    board.cubes[i][j].set(0)  # Clear the Value
                    key = None
                    
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
                            33        
                # Mouse Click Handling
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key = None
                
                # Solve the Board
                if event.key == pygame.K_RETURN:
                    # If the Board is Not Solvable
                    #if not board.solve():
                        #print("Board is Unsolvable")
                        #font = pygame.font.SysFont("comicsans", 60)
                        #text = font.render("Unsolvable!", 1, (255, 0, 0))
                        #win.blit(text, (540 // 2 - text.get_width() // 2, 540 // 2 - text.get_height() // 2))
                        #pygame.display.update()
                        #pygame.time.delay(2000)


        if board.selected and key is not None:
            board.place(key)

        redraw_window(win, board)
        pygame.display.update()

    pygame.quit()


# Redraw Pygame Window
def redraw_window(win, board):
    win.fill((255, 255, 255))
    board.draw()
    pygame.display.update()


# Run Main Function if Script is Executed Directly
if __name__ == "__main__":
    main()
