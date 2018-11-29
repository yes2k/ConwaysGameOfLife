import pygame
import math


pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


class Cell:
    """A Single Cell in a Board

    ==Attributes==
    @type x: int
        x-position of the cell
    @type y: int
        y-position of the cell
    @type size: int
        width and height of the cell
    @type state: bool
        state of the cell
    """

    def __init__(self, x, y, size, state):
        """Creates a Cell

        @type x: int
        @type y: int
        @type size: int
        @type state: bool
        @rtype None
        """
        self.square = pygame.Rect(x, y, size, size)
        self.state = state

    def get_state(self):
        """Returns state of the Cell

        @type self: Cell
        @rtype: Bool
        """
        return self.state

    def get_square(self):
        """
        @type self: Cell
        @rtype: Rect
        """
        return self.square


class Board:
    """A 2D array of Cells

    ===Attributes===
    @type rows: int
        Number of rows in the Board
    @type columns: int
        Number of columns in the Board
    @type size_of_squares:
        Size of each square in the Board
    """

    def __init__(self, rows, columns, size_of_squares):
        """Creates a Board

        @type rows: int
        @type columns: int
        @type size_of_squares: int
        @rtype: None
        """
        self.rows = rows
        self.columns = columns
        self.size_of_squares = size_of_squares
        self.boards = [[]]
        for i in range(self.columns):
            self.boards.append([])
            for j in range(self.rows):
                    self.boards[i].append(Cell(i*self.size_of_squares,
                                              j*self.size_of_squares,
                                              self.size_of_squares, False))

    def update(self):
        """The method to run every tick

        @type self: Board
        @rtype: None
        """
        for i in range(self.columns):
            for j in range(self.rows):
                pygame.draw.line(screen, (0, 0, 0),
                                (i * self.size_of_squares, 0),
                                (i * self.size_of_squares,
                                 self.get_rows()*self.get_size_of_square()))

                pygame.draw.line(screen, (0, 0, 0),
                                 (0, j * self.size_of_squares),
                                 (self.get_rows() * self.get_size_of_square(),
                                 j * self.size_of_squares))

                if self.boards[i][j].state is False:
                    pygame.draw.rect(screen, (225, 225, 225),
                                     self.boards[i][j].get_square())

                if self.boards[i][j].state is True:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     self.boards[i][j].get_square())

    def check_around_cell(self, x, y):
        """Returns the state of the adjacent cells

        @type x: int
        @type y: int
        @rtpye: array
        """
        states = [0, 0]
        for i in range(max(x-1, 0), min(x+2, self.columns)):
            for j in range(max(y-1, 0), min(y+2, self.rows)):
                if (i, j) == (x, y):
                    "do nothing"
                else:
                    if self.boards[i][j].state is True:
                        states[0] += 1
                    elif self.boards[i][j].state is False:
                        states[1] += 1
        return states

    def get_rows(self):
        """Returns number of rows in the board

        @type self: Board
        @return: int
        """
        return self.rows

    def get_columns(self):
        """Returns number of columns in the board

        @type self: Board
        @rtype: int
        """
        return self.columns

    def get_size_of_square(self):
        """Returns the size of the squares in the board

        @type self: Board
        @rtype: int
        """
        return self.size_of_squares

    def point_in_square(self, mouse_x, mouse_y):
        """Returns what cell contains the point (mouse_x, mouse_y)

        @type mouse_x: int
        @type mouse_y: int
        @rtype: tuple
        """
        for i in range(self.columns):
            for j in range(self.rows):
                if self.boards[i][j].square.collidepoint(mouse_x, mouse_y) == 1:
                    return (i, j)


class Main:
    """A 2D array of Cells

        ===Attributes===
        @type rows: int
            Number of rows in the Board
        @type columns: int
            Number of columns in the Board
        @type size_of_squares:
            Size of each square in the Board
    """

    def __init__(self, rows, columns, size_of_squares):
        """Initializes a Main class

        @type rows: int
        @type columns: int
        @type size_of_squares: int
        @rtype: None
        """
        self.board = Board(rows, columns, size_of_squares)
        self.im_board = [[False for x in range(columns)] for y in range(rows)]

    def clear_board(self):
        """Sets all the cells in the board to false

        @type self: Main
        @return: None
        """
        for i in range(self.board.get_columns()):
            for j in range(self.board.get_rows()):
                self.board.boards[i][j].state = False
                self.im_board[i][j] = False

    def update(self):
        """The method to run every tick

               @type self: Board
               @rtype: None
        """
        self.board.update()
        for i in range(self.board.get_columns()):
            for j in range(self.board.get_rows()):
                states = self.board.check_around_cell(i, j)
                if self.board.boards[i][j].state is True:
                    if states[0] < 2:
                        self.im_board[i][j] = False

                    if states[0] == 2 or states[0] == 3:
                        self.im_board[i][j] = True

                    if states[0] > 3:
                        self.im_board[i][j] = False

                if self.board.boards[i][j].state is False:
                    if states[0] == 3:
                        self.im_board[i][j] = True

        for i in range(self.board.get_columns()):
            for j in range(self.board.get_rows()):
                self.board.boards[i][j].state = self.im_board[i][j]

    def initial_update(self):
        """Call when game not running

        @type self: Main
        @rtype: None
        """
        self.board.update()


if __name__ == '__main__':
    clock = pygame.time.Clock()
    start = False
    num_row = 40
    num_col = 40
    size_of_squares = 10
    m = Main(num_row, num_col, size_of_squares)
    done = False
    initial = True

    while not done:
        screen.fill((225, 225, 225))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if math.sqrt(pos[0]**2 + pos[1]**2) <= math.sqrt(2*(350**2)):
                    coord = m.board.point_in_square(pos[0], pos[1])
                    m.board.boards[coord[0]][coord[1]].state = \
                        not m.board.boards[coord[0]][coord[1]].state

        if initial is True:
            m.initial_update()
            pygame.draw.ellipse(screen, (225, 0, 0),
                                pygame.Rect(600, 50, 10, 10))

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_s]:
            start = True
            initial = False
        if pressed[pygame.K_x]:
            start = False
            initial = True
        if pressed[pygame.K_c]:
            m.clear_board()

        if start is True:
            m.update()
            pygame.draw.ellipse(screen, (0, 255, 0),
                                pygame.Rect(600, 50, 10, 10))

        pygame.display.flip()
        clock.tick(60)
        pygame.time.delay(1)
