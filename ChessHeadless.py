from Pieces import Pawn, Rook, Bishop, Queen, King, Knight

class ChessExc(Exception):
    pass

class CheckExc(ChessExc):
    def __init__(self, msg='Checkmate: end of game'):
        super(CheckExc, self).__init__(msg)

class CheckMateExc(ChessExc):
    def __init__(self, msg="Check: you're in check"):
        super(CheckMateExc, self).__init__(msg)

class InvMoveExc(ChessExc):
    def __init__(self, msg='Invalid move'):
        super(InvMoveExc, self).__init__(msg)

class ChessHeadless():
    def __init__(self, file='New_Game.txt'):
        self.board, self.turn = self.read_game_data(file)
        self.click, self.first_click = 1, (0, 0)
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_from_piece(self):
        return self.get_piece(*self.first_click)
    
    def movefrom(self, row, col):
        from_square = self.get_piece(row, col)

        if (from_square != None) and ( 
            ((self.turn == 0) and (from_square.colour == 'White')) or 
            ((self.turn == 1) and (from_square.colour == 'Black'))):
            if self.check_for_checkmate(from_square):
                raise CheckMateExc
            if self.check_against_check(from_square): # we are in check
                self.click = 1 - self.click
                raise CheckExc
            else: # limit moves if in check else normal moves
                self.first_click = (row, col)
        else: # if there is no piece or wrong colour piece where we clicked
            self.click = 1 - self.click
            raise InvMoveExc

        return from_square

    def moveto(self, row, col):
        from_square = self.get_from_piece()
        from_pos = (from_square.row, from_square.column)

        if (row, col) not in from_square.possible_moves: # check possible move for piece
            raise InvMoveExc

        self.board[row][col] = from_square
        self.board[from_pos[0]][from_pos[1]] = None

        to_square = self.get_piece(row, col)
        to_square.history.append((from_pos, (row, col)))
        to_square.row = row 
        to_square.column = col
        self.turn = 1 - self.turn

        return to_square
    
    def move(self, from_pos, to_pos):
        from_piece = self.movefrom(*from_pos)
        to_piece = self.moveto(*to_pos)
        return to_piece

    def read_game_data(self, file):
        turn = None
        board = [[None]*8 for row in range(8)]
        input_data = open(f'Games/{file}', 'r').readlines()
        for i, line in enumerate(input_data):
            if i == 0: turn = int(line.rstrip())
            else:
                Piece, Colour, Row, Column = line.rstrip().split(' ')
                piece = eval(Piece+'(str(Colour), int(Column), int(Row))')
                board[int(piece.row)][int(piece.column)] = piece 
        return board, turn
    
    def check_against_check(self, clicked_piece):
        # if you are in check get out of it
        paths_to_king, atackers_pos = [], []
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if self.board[row_number][column_number]!= None and self.board[row_number][column_number].colour == clicked_piece.colour:
                    self.board[row_number][column_number].find_moves(self.board, [])
                    for move in self.board[row_number][column_number].possible_moves:
                        square = self.board[move[0]][move[1]] # row, column
                        if (square != None) and (square.piece == 'King') and (square.colour == clicked_piece.colour): #our king is in check
                            atackers_pos.append((row_number, column_number))
                            paths_to_king += self.board[row_number][column_number].find_path_to_king(move[0], move[1])
                            # code above should add to the paths_to_king it values not the whole list
        if len(paths_to_king) > 0: # you are in check
            clicked_piece.find_moves(self.board, paths_to_king)
            if len(clicked_piece.possible_moves) == 0:
                return True # we can't move
        return False
    
    def check_for_checkmate(self, clicked_piece):
        pieces_that_cant_move, piece_on_board = 0, 0
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if self.board[row_number][column_number] != None:
                    if clicked_piece.colour == self.board[row_number][column_number].colour:
                        if self.check_against_check(self.board[row_number][column_number]):
                            pieces_that_cant_move += 1
                        piece_on_board += 1
        if piece_on_board == pieces_that_cant_move:
            return True
        return False
    
    def dump(self):
        # text summary of board
        str = ''
        for row_number in range(0, 8):
            linebuff = '' 
            for column_number in range(0, 8):
                piece = self.board[row_number][column_number]
                c = '.' if piece == None else piece.abbrv
                linebuff = f"{linebuff}{c} "
            str = f"{str}\n{linebuff}"
        return str

    def __repr__(self):
        # string representation
        return f"{self.__class__} : {vars(self)}"
