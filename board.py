'''
Xinyi Cheng
CS5001
Fall 2021
Final project
'''
from constants import NUM_SQUARES, CORNER, SQUARE, SQUARE_COLORS, BLACK, RED,\
 EDGES_OF_SQUARE, BLACK_KING, RED_KING, RIGHT_ANGLE, THREE, FOUR, \
 PIECES_COLORS, HIGHLIGHT
from game_state import GameState
import turtle
import random


class Board:
    '''
        Class -- Board
            The UI.
        Attributes:
            gamestate -- A GameState object, used to keep track of
             the status of the squares and the current "turn".
            highbound -- The positive edge of the board.
            lowbound -- The negative edge of the board.
            pen -- The Turtle responsible for drawing.
            screen -- The screen.
        Methods:
            (none intended to be accessed outside the class)
    '''
    turn = BLACK
    winner = False

    def __init__(self):
        '''
            Constructor -- Creates a new instance of Board
            Parameters:
                self -- The current Board object.
        '''
        self.pen = turtle.Turtle()
        self.screen = turtle.Screen()
        self.screen.onclick(self.click_handler)
        self.gamestate = GameState()

        self.draw_board()
        self.draw_pieces(self.gamestate.matrix)
        turtle.done()

    def draw_circle(self, size):
        '''
            Function -- draw_circle
                Draw a circle with a given radius.
            Parameters:
                self.pen -- an instance of Turtle.
                size -- the radius of the circle.
            Returns:
                Nothing. Draws a colorful circle in the graphics window.
        '''
        self.pen.pendown()
        self.pen.begin_fill()
        self.pen.circle(size)
        self.pen.end_fill()
        self.pen.penup()

    def draw_square(self, size):
        '''
            Function -- draw_square
                Draw a square of a given size.
            Parameters:
                self.pen -- an instance of Turtle.
                size -- the length of each side of the square.
            Returns:
                Nothing. Draws a square in the graphics window.
        '''
        self.pen.pendown()
        self.pen.begin_fill()  # begin filling the square
        for i in range(EDGES_OF_SQUARE):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.end_fill()  # end filling the square
        self.pen.penup()

    def draw_square_nofilling(self, size):
        '''
            Function -- draw_square
                Draw a square of a given size without filling.
            Parameters:
                self.pen -- an instance of Turtle.
                size -- the length of each side of the square.
            Returns:
                Nothing. Draws a square in the graphics window.
        '''
        self.pen.pendown()
        for i in range(EDGES_OF_SQUARE):
            self.pen.forward(size)
            self.pen.left(RIGHT_ANGLE)
        self.pen.penup()

    # squares = [[row1, col1], [row2,col2]]
    def draw_highlight(self, highlight_color, squares):
        '''
            Function -- draw_highlight
                Draw squares of a given size without filling.
            Parameters:
                self.pen -- an instance of Turtle.
                highlight_color -- the color that used to draw the square,
                 a string.
                squares -- a list of list, the position that the squares in.
                 The smaller list is in the form [row, col]. row and col are
                  integers.
            Returns:
                Nothing. Draws squares in the graphics window.
        '''
        self.pen.color(highlight_color)
        turtle.tracer(0, 0)
        for row, col in squares:
            x = self.col_to_x(col)
            y = self.row_to_y(row)
            self.pen.setposition(x, y)
            self.draw_square_nofilling(SQUARE)

    def draw_board(self):
        '''
            Function -- draw_board
                Draw a board of a given size.
            Parameter:
                self -- the current object.
            Return:
                Nothing. Draw a board in the graphics window.
        '''
        board_size = NUM_SQUARES * SQUARE
        # Create the UI window. This should be the width of the board plus a
        # little margin
        window_size = board_size + SQUARE
        # The extra + SQUARE is the margin
        turtle.setup(window_size, window_size)

        # Set the drawing canvas size. The should be actual board size
        turtle.screensize(board_size, board_size)
        turtle.bgcolor(SQUARE_COLORS[1])  # The window's background color white
        turtle.tracer(0, 0)  # makes the drawing appear immediately

        # pen = turtle.Turtle()  # This variable does the drawing.
        self.pen.penup()  # This allows the pen to be moved.
        self.pen.hideturtle()  # This gets rid of the triangle cursor.

        # The first parameter is the outline color, the second is the filler
        self.pen.color(PIECES_COLORS[0], SQUARE_COLORS[1])

        # Step 1 - the board outline
        corner = - board_size / 2
        self.pen.setposition(corner, corner)
        self.draw_square(board_size)

        # Step 2 & 3 - the checkerboard squares.
        self.pen.color(PIECES_COLORS[0], SQUARE_COLORS[0])
        # ????????????self.pencolor="black", fillcolor = "light grey"
        for col in range(NUM_SQUARES):
            for row in range(NUM_SQUARES):
                self.pen.setposition(corner + SQUARE * col,
                                     corner + SQUARE * row)
                if col % 2 != row % 2:
                    self.draw_square(SQUARE)

    def draw_pieces(self, matrix):
        '''
            Function -- draw_pieces
                Draw pieces as the matrix.
            Parameters:
                self.pen -- an instance of Turtle.
                matrix -- the presence of the pieces.
            Returns:
                Nothing. Draws pieces in the graphics window.
        '''
        turtle.tracer(0, 0)
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                # red pieces and red's king
                if matrix[row][col] == RED or matrix[row][col] == RED_KING:
                    self.pen.color(PIECES_COLORS[1], PIECES_COLORS[1])
                    self.pen.setposition(CORNER + SQUARE * 0.5 + SQUARE * col,
                                         SQUARE * THREE - SQUARE * row)
                # black pieces and black's king
                elif matrix[row][col] == BLACK or \
                        matrix[row][col] == BLACK_KING:
                    self.pen.color(PIECES_COLORS[0], PIECES_COLORS[0])
                    self.pen.setposition(CORNER + SQUARE * 0.5 + SQUARE * col,
                                         SQUARE * THREE - SQUARE * row)
                # Prevent the occasion that moving the leftmost and uppermost
                # red piece causes the wrong drawing.
                else:
                    continue
                self.draw_circle(SQUARE / 2 - 1)

    def y_to_row(self, a):
        '''
            Method -- y_to_row
                Helper function that transfer y cooradinate in the window to
                 row in the matrix.
            Parameters:
                self -- the current Board object.
                a -- the y cooradiate, a float.
            Returns:
                the corresponding row of y cooradinate, an integer.
        '''
        x = a // SQUARE
        return THREE - x

    def x_to_col(self, a):
        '''
            Method -- x_to_col
                Helper function that transfer x cooradinate in the window to
                 column in the matrix.
            Parameters:
                self -- the current Board object.
                a -- the x cooradiate, a float.
            Returns:
                the corresponding column of x cooradinate, an integer.
        '''
        x = a // SQUARE
        return x + FOUR

    def row_to_y(self, a):
        '''
            Method -- row_to_y
                Helper function that transfer row in the matrix to
                 y cooradinate in the window to get the drawing starting point.
            Parameters:
                self -- the current Board object.
                a -- the row in the matrix, an integer.
            Returns:
                the corresponding y cooradinates of row, an float.
        '''
        return (THREE - a) * SQUARE

    def col_to_x(self, a):
        '''
            Method -- row_to_y
                Helper function that transfer row in the matrix to
                 y cooradinate in the window to get the drawing starting point.
            Parameters:
                self -- the current Board object.
                a -- the row in the matrix, an integer.
            Returns:
                the corresponding y cooradinates of row, an float.
        '''
        return (a - FOUR) * SQUARE

    def turns(self, last):
        '''
            Method -- turns
                Helper function that take turns between two colors.
            Parameters:
                self -- the current Board object.
                last -- the last turn, an integer.
            Returns:
                The turns that different from the last turn, an integer.
        '''
        if last == BLACK:
            return RED
        elif last == RED:
            return BLACK

    def click_handler(self, x, y):
        '''
            Function -- click_handler
                Called when a click occurs.
            Parameters:
                x -- X coordinate of the click.
                 Automatically provided by Turtle.
                y -- Y coordinate of the click.
                 Automatically provided by Turtle.
            Returns:
                Does not and should not return. Click handlers are a special
                 type of function automatically called by Turtle. You will not
                  have access to anything returned by this function.
        '''
        if x > CORNER and x < (NUM_SQUARES * SQUARE + CORNER) and \
           y > CORNER and y < (NUM_SQUARES * SQUARE + CORNER):
            print(x, y)
            print('The click was in board')
        else:
            print(x, y)
            print('The click was not in board')
        if not self.winner:
            # the corresponding row of the x cooradinates in this click
            n = int(self.x_to_col(x))
            # the corresponding column of the y cooradinates in this click
            m = int(self.y_to_row(y))
            # print("selected piece", self.gamestate.selected_piece)
            # When the player should choose a black piece to move.
            if len(self.gamestate.selected_piece) == 0 and self.turn == BLACK:
                # ??????????????????????????????????????????row???col
                valid_blacks = self.gamestate.all_valid_pieces(self.turn)
                if (m, n) in valid_blacks:  # ?????????click?????????row???col???????????????????????????
                    self.gamestate.selected_piece = [m, n]
                    # m,n ?????????click?????????row???col
                    capturing_moves = self.gamestate.get_capturing_moves(
                        self.gamestate.selected_piece)
                    non_capturing_moves = self.gamestate.\
                        get_non_capturing_moves(self.gamestate.selected_piece)
                    # draw highlights
                    self.draw_highlight(HIGHLIGHT[0],
                                        [self.gamestate.selected_piece])
                    self.draw_highlight(HIGHLIGHT[1],
                                        capturing_moves + non_capturing_moves)
                else:
                    print("Please click valid black pieces")
            # When the player has chosen a black piece to move
            # ?????????????????????
            elif len(self.gamestate.selected_piece) != 0 and \
                    self.turn == BLACK:
                # ?????????????????????capturing move???????????????len!=0?????????capturing move
                has_capturing = self.gamestate.all_capturing_moves(self.turn)
                # ?????????????????????????????????selected_pieces????????????????????????
                black_could_to = self.gamestate.\
                    valid_moves(self.gamestate.selected_piece)
                # ??????capturing move??????????????????non_capturing move
                if len(has_capturing) == 0:
                    # ???
                    if len(black_could_to) != 0 and (m, n) in black_could_to:
                        self.gamestate.\
                            move_piece(self.gamestate.selected_piece, (m, n))
                        self.turn = self.turns(self.turn)
                    self.gamestate.selected_piece = []
                    self.gamestate.become_king()  # ?????????????????????king,????????????3???4
                # ???capturing move??????????????????capturing moves???
                else:
                    # ?????????click?????????(row,col)???selected_pieces??????????????????????????????selected_pieces??????????????????capturing????????????
                    if (m, n) in black_could_to and\
                            tuple(self.gamestate.selected_piece) \
                            in has_capturing:
                        self.gamestate.\
                            move_piece(self.gamestate.selected_piece, (m, n))
                        self.gamestate.become_king()  # ?????????????????????king,????????????3???4
                        # multi_capturing
                        self.gamestate.selected_piece = [m, n]
                        dic = self.gamestate.\
                            get_capturing_moves(self.gamestate.selected_piece)
                        if len(dic) == 0:
                            self.turn = self.turns(self.turn)
                            self.gamestate.selected_piece = []
                            self.gamestate.become_king()  # ?????????????????????king,????????????3???4
                        else:
                            print("It's a multi-capturing move, \
please click the previous piece.")
                    # selected_pieces?????????????????????capturing????????????
                    elif tuple(self.gamestate.selected_piece) \
                            not in has_capturing:
                        self.gamestate.selected_piece = []
                        print("Please click the black piece that can make\
 capturing move.")
                    # ?????????click?????????(row,col)??????selected_pieces????????????????????????
                    elif (m, n) not in black_could_to and \
                            len(black_could_to) > 0:
                        self.gamestate.selected_piece = []
                        print("Please click the valid cell that the black\
 piece could move to:", black_could_to)
                    else:
                        self.gamestate.selected_piece = []
                        self.gamestate.become_king()  # ?????????????????????king,????????????3???4
                        print("Please click the black piece that can make\
 capturing move.")
                self.draw_board()
                self.draw_pieces(self.gamestate.matrix)
                if self.gamestate.check_lose(RED):
                    print("Black wins!")
                    self.winner = True
            # ??????????????????????????????????????????
            elif self.turn == RED:
                # ????????????????????????????????????????????????row???col
                valid_reds = self.gamestate.all_valid_pieces(self.turn)
                # ???????????????capturing?????????
                has_capturing = self.gamestate.all_capturing_moves(self.turn)
                if len(has_capturing) > 0:
                    # ???????????????????????????????????????, get a tuple (row, col)
                    chosen_red = has_capturing[random.
                                               randint(0, len(has_capturing)
                                                       - 1)]
                    # ?????????????????????????????????selected_pieces????????????????????????
                    chosen_could_to = self.gamestate.valid_moves(chosen_red)
                    chosen_to = chosen_could_to[random.
                                                randint(0, len(chosen_could_to)
                                                        - 1)]
                    # ??????capturing move??????????????????non_capturing move
                    self.gamestate.move_piece(chosen_red, chosen_to)
                    self.gamestate.become_king()  # ?????????????????????king,????????????3???4
                    # multi_capturing
                    chosen_red = chosen_to
                    dic = self.gamestate.get_capturing_moves(chosen_red)
                    while len(dic) != 0:
                        next_move = dic[random.randint(0, len(dic) - 1)]
                        self.gamestate.move_piece(chosen_red, next_move)
                        chosen_red = next_move
                        dic = self.gamestate.get_capturing_moves(chosen_red)
                else:
                    chosen_red = valid_reds[random.
                                            randint(0, len(valid_reds) - 1)]
                    # ?????????????????????????????????selected_pieces????????????????????????
                    chosen_could_to = self.gamestate.valid_moves(chosen_red)
                    chosen_to = chosen_could_to[random.
                                                randint(0, len(chosen_could_to)
                                                        - 1)]
                    # ??????capturing move??????????????????non_capturing move
                    self.gamestate.move_piece(chosen_red, chosen_to)
                self.turn = self.turns(self.turn)
                self.draw_board()
                self.draw_pieces(self.gamestate.matrix)
                if self.gamestate.check_lose(BLACK):
                    print("Red wins!")
                    self.winner = True
        else:
            print("The game is over!")
