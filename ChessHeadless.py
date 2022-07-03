import re
from Pieces import Pawn, Rook, Bishop, Queen, King, Knight

class ChessExc(Exception):
    pass

class CheckExc(ChessExc):
    def __init__(self, msg='Checkmate: end of game'):
        super().__init__(msg)

class CheckMateExc(ChessExc):
    def __init__(self, msg="Check: you're in check"):
        super().__init__(msg)

class InvMoveExc(ChessExc):
    def __init__(self, msg='Invalid move'):
        super().__init__(msg)

class ChessHeadless():
    def __init__(self, file='New_Game.txt'):
        self.board, self.turn = self.read_game_data(file) # file maybe None
        self.click, self.first_click = 1, (0, 0)
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_from_piece(self):
        return self.get_piece(*self.first_click)
    
    def movefrom(self, row, col):
        from_square = self.get_piece(row, col)

        if (from_square is not None) and ( 
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
    
    def new_board(self):
        board = [[None]*8 for row in range(8)]
        return board
    
    def notation_pos(self, token):
        # Return tuple (row, col) from parsed token, else None
        # String fmt :: '(<row>, <col>)' | '[a-h][1-8]'
        #   first char row:[a-h], second char col:[1-8]
        #      eg. 'a8' == (0,0), 'a1' == (7,0), 'h1' == (7,7), 'h8' == (0,7)
        pos = None
        row = -1; col = -1

        if len(token) == 2:
            token.lower()
            col = ord(token[0]) - ord('a') # col 'a' is table column 0
            row = 8 - int(token[1])          # row 1 is table row 7
        else:
            if re.match(r'\([0-7],[0-7]\)$', token):
                row = int(token[1])
                col = int(token[3])
        if row >= 0 and row < 8 and col >= 0 and col < 8:
            pos = (row, col)
        return pos
    
    def notation_piece(self, token):
        # Return tuple (<class>, colour) if token starts with a piece abbrv, else None.
        # one char abbrv of piece (R N B Q K P) or 'D' for board.dump, 
        # upper case is white, lower black e.g. N is white knight, n is black
        # 
        piece = None
        pieces = {
            'R' : Rook, 
            'N' : Knight, 
            'B' : Bishop, 
            'Q' : Queen,
            'K' : King, 
            'P' : Pawn,
            'D' : 'dump'
        }
        if len(token) == 1:
            p = token[0]
            colour = 'White' if p.isupper() else 'Black'
            p = p.upper()
            if p in pieces:
                if p == 'D':
                    piece = ()  # empty
                    print(f"Notation dump: {self.dump()}")
                else:
                    piece = (pieces[p], colour)
        return piece
    
    def commands(self, command):
        '''
        Run command string fmt:: [<piece_creations>] <piece_moves>
        e.g. 'Ke1; Qc3; ra1; d; Ke1:d2; ra1:a2' ## white king in check, dump, K moved, rook attacks K
        where:
            <piece_creations> :: <piece_creation> [; <piece_creations>]

            <piece_creation> :: <piece_or_dump><pos> : to create a piece at pos
            <piece_or_dump> :: <piece> | 'D' : where 'd' is string dump action
            <piece> :: <piece_white> | <piece_black>
            <piece_white> :: 'R' | 'N' | 'B' | 'Q' | 'K' | 'P' : upper case is white
            <piece_black> :: 'r' | 'n' | 'b' | 'q' | 'k' | 'p' : lower case is black
            <pos> :: <label> | <row_col> : two position formats
            <label> :: <col_label> <row_label> : e.g. a1 == (7,0), h8 == (0, 7)
            <row_col> :: '(<row>, <col>)' : board position tuple e.g. (0, 0) for r (black rook)
            <col_label> :: '[a-h]' : 'a' == column 0, 'h' == column 7
            <row_label> :: '[1-8]' : 1 == row 7, 8 == row 0

            <piece_moves> :: <piece_move> [; <piece_moves>]
            <piece_move> :: <piece> <from_pos>:<to_pos>
            <from_pos> :: <pos> : move from position
            <to_pos> :: <pos> : move to position
        '''
        errs = []
        tokens = command.split(';')
        ncommands = len(tokens)
        for (indext, token) in enumerate(tokens):
            token = re.sub(r'\s+', '', token) # remove whitespace
            m = re.match(r'[Dd]$', token)
            if m:
                print(f"Notation dump: {self.dump()}")
                continue

            pieces = 'RNBQKP'
            pieces_fmt = f'[{pieces}{pieces.lower()}]'
            pos_fmt = r'\([0-7],[0-7]\)|[A-ha-h][1-8]'
            m = re.match(f'({pieces_fmt})({pos_fmt})\:?({pos_fmt})?$', token)
            groups = m.groups() if m else None
            #print(f"DBG token {token} == {groups}")
            if groups is None or (groups[0] is None and groups[-1] is None):
                err_mess = f"invalid command token index [{indext}]:{token}"
                errs.append((indext, err_mess))
                continue

            np = self.notation_piece(groups[0])
            if np == None:
                continue
            from_pos = self.notation_pos(groups[1])
            piece = self.get_piece(*from_pos)
            to_pos = None
            if groups[2]:
                to_pos = self.notation_pos(groups[2])

            if to_pos:
                if piece and piece.abbrv == groups[0]:
                    # move e.g. Ke1:d2; expects match piece at from_pos:
                    try:
                        self.move(from_pos, to_pos)
                    except ChessExc as exc:
                        err_mess = f"command token index [{indext}]:{token} move({from_pos}, {to_pos}) raised an exception {exc}"
                        errs.append((indext, err_mess))
                else:
                    err_mess = f"invalid command token index [{indext}]:{token} mismatch move {piece} ({from_pos}, {to_pos}"
                    errs.append((indext, err_mess))
            else:
                np = None
                if piece == None:
                    # New piece only if square empty
                    np = self.notation_piece(token[0])
                if np:
                    # create new piece
                    self.board[from_pos[0]][from_pos[1]] = \
                        np[0](np[1], from_pos[1], from_pos[0])
                else:
                    err_mess = f"invalid command token index [{indext}]:{token}, existing piece {piece.piece} {from_pos}"
                    errs.append((indext, err_mess))

        return (ncommands, errs)

    def read_game_data(self, file):
        turn = 0
        board = self.new_board()
        if file:
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
