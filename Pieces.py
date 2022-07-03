class GameObject():
    def __init__(self, piece, colour, column, row, value):
        self.row, self.value, self.piece, self.InCheck = row, value, piece, False
        self.colour, self.column, self.possible_moves = colour, column, []
        self.icon = 'Chess_Resources/'+self.colour+'_'+self.piece+'.gif'
        self.abbrv = self.piece[0]  # first char, e.g. 'P' for Pawn
        if self.colour == 'Black':
            self.abbrv = self.abbrv.lower()  # e.g. 'p' for Pawn 
        self.history = []

    def highlight_moves(self, window, board):
        for row_number, column_number in self.possible_moves:
            squarex = window.grid_slaves(row = row_number, column = column_number)
            if len(squarex) > 1:
                print(f"warning, this square has more than one grid slave!!! {row_number}, {column_number}. count: {len(squarex)}")
            square = squarex[0] #returns list of widgets
            dest_square = board[row_number][column_number]
            if dest_square == None: #if there is nothing at position i
                square.config(bg='green') # highlight position i green
            else: # none has no attrubrite to clour this stops this error
                square.config(bg='red') # highlight position i red

    def remove_check_moves(self, board):
        local_moves = []
        for row in range(8):
            for column in range(8):
                if self.piece == 'king':
                    for move in self.possible_moves:
                        #if fit is not my own piece
                        if board[move[0]][move[1]] != None and board[move[0]][move[1]] != board[self.row][self.column]:
                            # generate moves from piece we are checking to edge of board in direction of current possible move
                            if (self.row, self.column) in board[row][column].path_past_self(board, (move[0], move[1])):
                                local_moves.append(move)
                else: # if we are a king we check if the king is on our row
                    if board[row][column] != None and board[row][column].piece == 'King' and board[row][column].colour == self.colour:
                        if (row, column) in board[board[row][column].row][board[row][column].column].path_past_self(board, (self.row, self.column)):
                            self.possible_moves = []
                            return
        # remove moves
        for move in local_moves:
            self.possible_moves.remove(move)

    def explore_moves(self, direction, board, pieces_to_jump=0):
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
                            if pieces_to_jump == 0:
                                moves.append(working_value)
                                break
                            pieces_to_jump -= 1
                        else: break
                else:
                    break
            return moves

    def find_moves(self, board, path_to_king):
        self.possible_moves = []
        self.find_possible_moves(board)
        if len(path_to_king) > 0: #if we are in check
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
        self.remove_check_moves(board)

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
    
    def path_past_self(self, board, square_to_move_to):
        square_row, square_column = square_to_move_to
        if self.piece != 'Knight' and  self.piece != 'Pawn':
            #neend more checking
            direction = (abs(square_row-self.row), abs(square_column-self.column))
            return self.explore_moves(direction, board, pieces_to_jump=1)
        elif self.piece == 'Pawn':
            if self.column < 7: return [((self.row + self.direction), (self.column + 1))]
            if self.column > 1: return [((self.row + self.direction), (self.column - 1))]
        else: return self.find_possible_moves(board)
    
    def __repr__(self):
        # string representation
        #return f"({self.__class__}){self} : {vars(self)}"
        return f"{self.__class__} : {vars(self)}"


class Pawn(GameObject):
    def __init__(self, colour, column, row):
        super().__init__('Pawn', colour, column, row, 1)
        if self.colour == 'White': self.direction = -1
        else: self.direction = 1
    def first_move(self):
        if (self.row == 1 and self.colour == 'Black') or (self.row == 6 and self.colour == 'White'):
            return True
        return False
    def find_possible_moves(self, board):
        if board[self.row + self.direction][self.column] == None: 
            self.possible_moves.append(((self.row + self.direction), self.column))
            if self.first_move():
                if board[self.row+ (self.direction*2)][self.column] == None:
                    self.possible_moves.append(((self.row + (self.direction*2)), self.column))
        if self.column > 1:
            dest_square = board[self.row + self.direction][self.column - 1]
            if dest_square != None and dest_square.colour != self.colour:
                # take left
                self.possible_moves.append(((self.row + self.direction), (self.column -1)))
        if self.column < 7:
            dest_square = board[self.row + self.direction][self.column + 1]
            if dest_square != None and dest_square.colour != self.colour:
                # take right
                self.possible_moves.append(((self.row + self.direction), (self.column + 1)))

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