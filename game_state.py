'''
Xinyi Cheng
CS5001
Fall 2021
Final project
'''
from constants import NUM_SQUARES, BLACK, BLACK_KING, RED, RED_KING


class GameState:
    '''
        Class -- GameState
            Represents game state.
        Attributes:
            matrix -- A list of lists contained the instances of pieces
        Method:
            is_cell_in_border -- Check if a cell's row and column are in
             borders,then the cell is in border.
            is_enemy -- Check if the other color is differnet from this color.
            is_same -- Check if the other color is the same as this color.
            all_valid_pieces -- Find all the pieces of this color that could
             make moves(including capturing moves and non_capturing moves).
            all_capturing_moves -- Find all the pieces of given color that
             could make capturing.
            valid_moves -- Calculate all valid positions that the given
             selected pieces could be moved to.
            get_capturing_moves -- Calculate all valid positions that the
             selected pieces could be moved to by capturing moves.
            get_non_capturing_moves -- Calculate all valid positions that the
             selected pieces could be moved to by non-capturing moves.
            move_piece -- Exchange the positions of two numbers in a matrix.
            become_king -- Change the number in the matrix when a piece becomes
             king.
            check_lose -- Check if one of the two player loses.
    '''
    def __init__(self):
        '''
            Constructor -- creates a new instance of PlayingCard
            Parameters:
                self -- the current GameState object
        '''
        self.selected_piece = []
        # 1 for black, 2 for red, 3 for black king, 4 for red king
        self.matrix = [
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 2, 0, 2, 0, 2, 0, 2],
            [2, 0, 2, 0, 2, 0, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1]
        ]
        # 1 for black, 2 for red, 3 for black king, 4 for red king
        # non-capturing moves possible directions, a map
        self.non_cap_dirs = {1: [[-1, -1], [-1, 1]],
                             2: [[1, -1], [1, 1]],
                             3: [[-1, -1], [-1, 1], [1, -1], [1, 1]],
                             4: [[-1, -1], [-1, 1], [1, -1], [1, 1]]
                             }
        # 1 for black, 2 for red, 3 for black king, 4 for red king
        # capturing moves possible directions, a map
        self.cap_dirs = {1: [[-2, -2], [-2, 2]],
                         2: [[2, -2], [2, 2]],
                         3: [[-2, -2], [-2, 2], [2, -2], [2, 2]],
                         4: [[-2, -2], [-2, 2], [2, -2], [2, 2]]
                         }

    def is_cell_in_border(self, row: int, col: int):
        '''
            Method -- is_cell_in_border
                Check if a cell's row and column are in borders,then the cell
                 is in border
            Parameters:
                self -- The current GameState object
                row -- The row of the cell, an integer
                col -- The column of the cell, an integer
            Returns:
                True if the cell is in border, and False otherwise.
        '''
        return row >= 0 and row < NUM_SQUARES and \
            col >= 0 and col < NUM_SQUARES

    def is_enemy(self, this_color, other_color):
        '''
            Method -- is_enemy
                Check if the other color is differnet from this color
            Parameters:
                self -- The current GameState object
                this_color -- the current color, an integer
                other_color -- the color should be checked, an integer
            Returns:
                True if the colors are different and the other color is not
                 vacant, and False otherwise
        '''
        return other_color != 0 and other_color % 2 != this_color % 2

    def is_same(self, this_color, other_color):
        '''
            Method -- is_same
                Check if the other color is the same as this color
            Parameters:
                self -- The current GameState object
                this_color -- the current color, an integer
                other_color -- the color should be checked, an integer
            Returns:
                True if the colors are same and the other color is not vacant,
                 and False otherwise
        '''
        return other_color != 0 and this_color % 2 == other_color % 2

    def all_valid_pieces(self, color):
        '''
            Method -- all_valid_pieces
                Find all the pieces of this color that could make moves
                (including capturing moves and non_capturing moves)
            Parameters:
                self -- The current GameState object
                color -- The color that the pieces should be, an integer
            Returns:
                A list of tuples, all the pieces of this color in the board
                 that could make moves. Tuples in the form (row, col).
        '''
        lst = []
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                if self.is_same(color, self.matrix[row][col]) and\
                  len(self.valid_moves([row, col])) > 0:
                    lst.append((row, col))
        return lst

    def all_capturing_moves(self, color):
        '''
            Method -- all_capturing_moves
                Find all the pieces of given color that could make capturing
                 moves.
            Parameters:
                self -- The current GameState object
                color -- The given color, an integer
            Returns:
                A list of tuples, all the pieces of given color that could make
                 capturing moves. Tuples in the form (row, col).
        '''
        lst = []
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                if self.is_same(color, self.matrix[row][col]):
                    capturing_moves = self.get_capturing_moves([row, col])
                    if len(capturing_moves) > 0:
                        lst.append((row, col))
        return lst

    def valid_moves(self, selected_piece: list):
        '''
            Method -- valid_moves
                Calculate all valid positions that the given selected pieces
                 could be moved to
            Parameters:
                self -- The current GameState object
                selected_piece -- A list of the position that the selected
                 pieces. In the form [row, col]
            Returns:
                A list of tuples. If the selected piece have capturing moves,
                 then only return the positions that the piece could make
                  capturing moves to. If the selected piece doesn't have any
                   valid capturing moves, then returns eturn the positions that
                    could make non-capturing moves to. Tuples in the form
                     (row, col).
        '''
        capturing_moves = self.get_capturing_moves(selected_piece)
        non_capturing_moves = self.get_non_capturing_moves(selected_piece)
        if len(capturing_moves) > 0:
            return capturing_moves
        else:
            return non_capturing_moves

    # return a list of tuple
    def get_capturing_moves(self, selected_piece: list):
        '''
            Method -- get_capturing_moves
                Calculate all valid positions that the selected pieces could be
                 moved to by capturing moves
            Parameters:
                self -- The current GameState object
                selected_piece -- A list of the position that the selected
                 pieces. In the form [row, col]
            Returns:
                A list of tuples. The list is all valid positions that the
                 selected pieces could be moved to by capturing moves. Tuples
                  in the form (row, col).
        '''
        capturing_moves = []
        selected_row, selected_col = selected_piece
        color = self.matrix[selected_row][selected_col]
        for i in range(len(self.non_cap_dirs[color])):
            x, y = self.non_cap_dirs[color][i]
            neighbor = [selected_row + x, selected_col + y]
            if self.is_cell_in_border(neighbor[0], neighbor[1]):
                neighbor_color = self.matrix[neighbor[0]][neighbor[1]]
                # if the neighbor is in border and is the enemy,
                # then check if next_neighbor is in border and empty
                if self.is_enemy(color, neighbor_color):
                    x, y = self.cap_dirs[color][i]
                    next_neighbor = (selected_row + x, selected_col + y)
                    if self.is_cell_in_border(next_neighbor[0],
                                              next_neighbor[1]) and \
                            self.matrix[next_neighbor[0]][next_neighbor[1]] \
                            == 0:
                        capturing_moves.append(next_neighbor)
        return capturing_moves

    # return a list of tuple
    def get_non_capturing_moves(self, selected_piece: list):
        '''
            Method -- get_non_capturing_moves
                Calculate all valid positions that the selected pieces could be
                 moved to by non-capturing moves
            Parameters:
                self -- The current GameState object
                selected_piece -- A list of the position that the selected
                 pieces. In the form [row, col]. row and col are integers.
            Returns:
                A list of tuples. The list is all valid positions that the
                 selected pieces could be moved to by non-capturing moves.
                  Tuples in the form (row, col). row and col are integers.
        '''
        non_capturing_moves = []
        selected_row, selected_col = selected_piece
        color = self.matrix[selected_row][selected_col]
        for x, y in self.non_cap_dirs[color]:
            neighbor = (selected_row + x, selected_col + y)
            if self.is_cell_in_border(neighbor[0], neighbor[1]) and \
                    self.matrix[neighbor[0]][neighbor[1]] == 0:
                non_capturing_moves.append(neighbor)
        return non_capturing_moves

    def move_piece(self, old, new):
        '''
            Method -- move_piece
                Exchange the positions of two numbers in a matrix. And if it
                 is capturing move, it will erase the captured piece.
            Parameters:
                self -- The current GameState object
                old -- the position of the selected piece, a list of two
                 integers, in the form[row, column]
                new -- the position of the selected piece that is moved to, a
                 list of two integers, in the form[row, column]
            Returns:
                Nothing. Exchange the positions of two numbers in a matrix.
                 And if it is capturing move, it will erase the captured piece.
        '''
        self.matrix[old[0]][old[1]],\
            self.matrix[new[0]][new[1]] = \
            self.matrix[new[0]][new[1]], \
            self.matrix[old[0]][old[1]]
        self.erase_captured_piece(old, new)

    def become_king(self):
        '''
            Method -- become_king
                Change the number in the matrix when a piece becomes king
            Parameters:
                self -- The current GameState object
            Returns:
                Nothing. But changes the number in the matrix
        '''
        for col in range(NUM_SQUARES):
            if self.matrix[0][col] == BLACK:
                self.matrix[0][col] = BLACK_KING
            elif self.matrix[7][col] == RED:
                self.matrix[7][col] = RED_KING

    def check_lose(self, color):
        '''
            Method -- check_lose
                Check if one of the two player loses
            Parameters:
                self -- The current GameState object
                color -- The color that may lose
            Returns:
                True if the given color loses (it has no position to move to or
                 there is no pieces of this color on the board), and False
                  otherwise.
        '''
        # The number of pieces in the given color
        num_pieces = 0
        # The number of pieces in the given color that could be moved
        pieces_could_move = 0
        for row in range(NUM_SQUARES):
            for col in range(NUM_SQUARES):
                if self.is_same(color, self.matrix[row][col]):
                    num_pieces += 1
                    if len(self.valid_moves([row, col])) > 0:
                        pieces_could_move += 1
        return num_pieces == 0 or pieces_could_move == 0

    def erase_captured_piece(self, selected_piece, moved_to):
        '''
            Function -- erase_captured_piece
                If it is a capturing move, erase the captured pieces.
            Parameters:
                selected_piece -- the position of the selected piece, a list
                 of two integers, in the form[row, column]
                moved_to -- the position of the selected piece that is moved
                 to, a list of two integers, in the form[row, column]
            Returns:
                Nothing. If it is a capturing move, erase the captured pieces.
        '''
        a = (selected_piece[0] + moved_to[0]) / 2
        b = (selected_piece[1] + moved_to[1]) / 2
        if a % 1 == 0 and b % 1 == 0:
            self.matrix[int(a)][int(b)] = 0
