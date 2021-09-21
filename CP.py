import CD

class GameObject():
    def __init__(self, piece, colour, column, row, value):
        self.row = row
        self.value = value
        self.piece = piece
        self.colour = colour
        self.column = column
        self.possible_moves= []
        self.icon = CD.path+self.colour+'_'+self.piece+'.gif'

    def highlight_moves(self, window, board):
        for row_number, column_number in self.possible_moves:
            print('posible', self.possible_moves)
            squarex = window.grid_slaves(row = row_number, column = column_number)
            if len(squarex) > 1:
                print(f"warning, this square has more than one grid slave!!! {row_number}, {column_number}. count: {len(squarex)}")
            square = squarex[0] #returns list of widgets
            dest_square = board[row_number][column_number]
            if dest_square == None: #if there is nothing at position i
                square.config(bg='green') # highlight position i green
            else: # none has no attrubrite to clour this stops this error
                square.config(bg='red') # highlight position i red

    def remove_kings_check_moves(self, board):
        if self.piece == 'King':
            local_moves = []
            # create extra list of self.possible_moves not pinpoint too
            for move in self.possible_moves:
                for row_number in range(0, 8):
                    for column_number in range(0, 8):
                        #if fit is not my own piece
                        if board[row_number][column_number] != None and board[row_number][column_number] != board[self.row][self.column]:
                            #get the piece which is not selected possible moves
                            board[row_number][column_number].test_moves(board, [])
                            # go through that
                            for piece_move in board[row_number][column_number].possible_moves:
                                #check if a move in my possible moves is in that pieces
                                if piece_move != move:
                                    local_moves.append(move)
            self.possible_moves = local_moves

    def explore_moves(self, direction, board):
        working_value = self.row, self.column
        moves = []
        while True:
            working_value = ((working_value[0] + direction[0]), (working_value[1] + direction[1])) 
            if (working_value[0] >= 0)and(working_value[0] <= 7)and(working_value[1] >= 0)and(working_value[1] <= 7):
                dest_square = board[working_value[0]][working_value[1]]
                if dest_square == None:
                    moves.append(working_value)
                else:
                    if dest_square.colour != self.colour:
                        moves.append(working_value)
                    break
            else:
                break
        return moves

    def find_moves(self, board, path_to_king, run='a'):
        self.test_moves(board, path_to_king, run)
        self.remove_kings_check_moves(board)

    def test_moves(self, board, path_to_king, run='a'):
        self.possible_moves = []
        self.find_possible_moves(board)
        if len(path_to_king) > 0 and len(path_to_king) > 0: #if we are in check
            if self.piece == 'King': #king can move out of check
                self.possible_moves = [move for move in self.possible_moves if move not in path_to_king]
            else: #king can not block itelf from check
                self.possible_moves = list(set(self.possible_moves) & set(path_to_king))        #remove piece in possible moves that is not your colour
        possible_moves = []
        for move in self.possible_moves:
            moving_piece = board[move[0]][move[1]]
            if ( (moving_piece != None) and (moving_piece.colour != self.colour) ) or ( moving_piece == None):
                possible_moves.append(move)
        self.possible_moves = possible_moves

    def find_path_to_king(self, king_row, king_column):
        if self.piece != 'Knight': # attcking knight can only be taken
            if king_column - self.column != 0:
                column_dir = int((king_column - self.column) / (abs(king_column - self.column)))
                column_path = list(range(self.column, king_column, column_dir))
            if king_row - self.row != 0:
                row_dir = int((king_row - self.row) / (abs(king_row - self.row)) )
                row_path = list(range(self.row, king_row, row_dir))
            if king_column - self.column == 0:
                column_path = [king_column] * len(row_path)
            elif king_row - self.row == 0:
                row_path = [king_row] * len(column_path)
            return list(zip(row_path, column_path))
        return [(self.row, self.column)]

    def __repr__(self):
        # display object as constructor string
        return (f'{self.__class__.__name__}('f'{self.colour!r}, {self.column!r}, {self.row!r})')

class Pawn(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('Pawn', colour, column, row, 1)
    def first_move(self):
        if (self.row == 1 and self.colour == 'Black') or (self.row == 6 and self.colour == 'White'):
            return True
        return False
    def find_possible_moves(self, board):
        if self.colour == 'White':
            direction = -1
        else: 
            direction = 1
        if board[self.row + direction][self.column] == None: 
            self.possible_moves.append(((self.row + direction), self.column))
            if self.first_move():
                if board[self.row+ (direction*2)][self.column] == None:
                    self.possible_moves.append(((self.row + (direction*2)), self.column))
        if self.column > 1:
            dest_square = board[self.row + direction][self.column - 1]
            if dest_square != None and dest_square.colour != self.colour:
                # take left
                self.possible_moves.append(((self.row + direction), (self.column -1)))
        if self.column < 7:
            dest_square = board[self.row + direction][self.column + 1]
            if dest_square != None and dest_square.colour != self.colour:
                # take right
                self.possible_moves.append(((self.row + direction), (self.column + 1)))

class Rook(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('Rook', colour, column, row, 4)
    def find_possible_moves(self, board):
        self.possible_moves.extend(self.explore_moves((-1, 0), board))# up
        self.possible_moves.extend(self.explore_moves((0, +1), board))# right
        self.possible_moves.extend(self.explore_moves((0, -1), board))# left
        self.possible_moves.extend(self.explore_moves((+1, 0), board))# down

class Bishop(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('Bishop', colour, column, row, 3)
    def find_possible_moves(self, board):
        self.possible_moves.extend(self.explore_moves((-1, -1), board))# up left
        self.possible_moves.extend(self.explore_moves((-1, +1), board))# up right
        self.possible_moves.extend(self.explore_moves((+1, -1), board))# down left
        self.possible_moves.extend(self.explore_moves((+1, +1), board))# down right

class King(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('King', colour, column, row, 1)
        self.check_moves = []
    def find_possible_moves(self, board):
        if self.row > 0:
            self.possible_moves.append((self.row-1, self.column))
            if self.column > 0:
                self.possible_moves.append((self.row-1, self.column-1))
            if self.column < 7:
                self.possible_moves.append((self.row-1, self.column+1))
        if self.row < 7:
            self.possible_moves.append((self.row+1, self.column))
            if self.column > 0:
                self.possible_moves.append((self.row+1, self.column-1))
            if self.column < 7:
                self.possible_moves.append((self.row+1, self.column+1))
        if self.column < 7: 
            self.possible_moves.append((self.row, self.column+1))
        if self.column > 0:
            self.possible_moves.append((self.row, self.column-1))

class Queen(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('Queen', colour, column, row, 9)
    def find_possible_moves(self, board):
        self.possible_moves.extend(self.explore_moves((-1, -1), board))# up left
        self.possible_moves.extend(self.explore_moves((-1, +1), board))# up right
        self.possible_moves.extend(self.explore_moves((+1, -1), board))# down left
        self.possible_moves.extend(self.explore_moves((+1, +1), board))# down right
        self.possible_moves.extend(self.explore_moves((-1, 0), board))# up
        self.possible_moves.extend(self.explore_moves((0, +1), board))# right
        self.possible_moves.extend(self.explore_moves((0, -1), board))# left
        self.possible_moves.extend(self.explore_moves((+1, 0), board))# down

class Knight(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('Knight', colour, column, row, 5)
    def find_possible_moves(self, board): 
        if self.row < 6 and self.column > 0:
            self.possible_moves.append((self.row+2, self.column-1))
        if self.row < 6 and self.column < 7:
            self.possible_moves.append((self.row+2, self.column+1))
        if self.row > 1 and self.column > 0:
            self.possible_moves.append((self.row-2, self.column-1))
        if self.row > 1 and self.column < 7:
            self.possible_moves.append((self.row-2, self.column+1))
        if self.row > 0 and self.column < 6:
            self.possible_moves.append((self.row-1, self.column+2))
        if self.row < 7 and self.column < 6:
            self.possible_moves.append((self.row+1, self.column+2))
        if self.row > 0 and self.column > 1:
            self.possible_moves.append((self.row-1, self.column-2))
        if self.row < 7 and self.column > 1:
            self.possible_moves.append((self.row+1, self.column-2))

pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]