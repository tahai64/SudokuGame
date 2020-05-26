import pygame
from SudokuAlgo import solve, valid
import time
pygame.font.init()

# Imports solve and valid from SudokoAlgo. Valid function is used to see if user input is valid in the location that they placed the number. Solve algorithim is used to see if the user input is correct and will lead to a correctly finished sudoku puzzle  

class Grid:
    board = [
        [7,8,0,4,0,0,1,2,0],
        [6,0,0,0,7,5,0,0,9],
        [0,0,0,6,0,1,0,7,8],
        [0,0,7,0,4,0,2,6,0],
        [0,0,1,0,5,0,9,3,0],
        [9,0,4,0,6,0,0,0,5],
        [0,7,0,3,0,0,0,1,2],
        [1,2,0,0,0,7,4,0,0],
        [0,4,9,2,0,6,0,0,7]
    ]

    def __init__(self, rows, colms, width, height):
        self.rows = rows
        self.colms = colms
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(colms)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

# Sends model without sketch values to the SudokuAlgo to see if it will be able to be solved using the values that the user has inputted

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.colms)] for i in range(self.rows)]

# Confirms the value that you want to enter within a given cube on the board. Makes it permenant.

    def place(self, val):
        row, colm = self.selected
        if self.cubes[row][colm].value == 0:
            self.cubes[row][colm].set(val)
            self.update_model()

            if valid(self.model, val, (row,colm)) and solve(self.model):
                return True
            else:
                self.cubes[row][colm].set(0)
                self.cubes[row][colm].set_temp(0)
                self.update_model()
                return False

# Sets the temperary value in the cube on the board. User can place a temperary value that they think might fit in the cube before making it permanent when they are sure that it belongs.

    def sketching(self, val):
        row, colm = self.selected
        self.cubes[row][colm].set_temp(val)

    def draw(self, win):
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0,0,0), (0, i*gap), (self.width, i*gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

# Above is for drawing grid lines and below is for drawing cubes within those cubes
        for i in range(self.rows):
            for j in range(self.colms):
                self.cubes[i][j].draw(win)

# Selects which cube within the board you want to make a move in 

    def select(self, row, colm):
        for i in range(self.rows):
            for j in range(self.colms):
                self.cubes[i][j].selected = False

        self.cubes[row][colm].selected = True
        self.selected = (row, colm)

    def clear(self):
        row, colm = self.selected
        if self.cubes[row][colm].value == 0:
            self.cubes[row][colm].set_temp(0)

# Returns the position of the cube that the user has selected by clicking on

    def click(self, pos):
        """
        :param: pos
        :return: (row, colm)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y),int(x))
        else:
            return None

# Checks to see if the puzzle is finishing by checking to see if the board has been filled up and no empty spots remain 

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.colms):
                if self.cubes[i][j].value == 0:
                    return False
        return True


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, colm, width ,height):
        self.value = value
        self.temp = 0
        self.row = row
        self.colm = colm
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.colm * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128,128,128))
            win.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(win, (255,0,0), (x,y, gap ,gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

# Used to draw and display time elasped during game 

def redraw_window(win, board, time, strikes):
    win.fill((255,255,255))
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1, (0,0,0))
    win.blit(text, (540 - 160, 560))
    
# Drawing Strikes and the board/grid
    
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    board.draw(win)


def format_time(secs):
    sec = secs%60
    minute = secs//60
    hour = minute//60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540,600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

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
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("UnSuccessful")
                            strikes += 1
                        key = None

                        if board.is_finished():
                            print("Game over")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketching(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()