import re
from ChessGame.Pieces import Pawn, Rook, Knight, Bishop, Queen, King

class ChessErrs:
    """ChessGame error values"""

    ErrNone = 0  # no error
    ErrCheckMate = -1
    ErrCheck = -2
    ErrInvMove = -3
    ErrInvColour = -4
    ErrInvCommand = -5  # invalid command token
    ErrInvCommandMove = -6  # invalid move command

class ChessExc(Exception):
    """ChessGame base exception"""

    def __init__(self, msg=None, err=0):
        super(ChessExc, self).__init__(msg)
        self.err = err


class CheckMateExc(ChessExc):
    """ChessGame "check mate" exception"""

    def __init__(self, msg="Checkmate: end of game", err=ChessErrs.ErrCheckMate):
        super(CheckMateExc, self).__init__(msg, err)


class CheckExc(ChessExc):
    """ChessGame "check" exception"""

    def __init__(self, msg="Check: you're in check", err=ChessErrs.ErrCheck):
        super(CheckExc, self).__init__(msg, err)


class InvMoveExc(ChessExc):
    """ChessGame "invalid move" exception"""

    def __init__(self, msg="Invalid move", err=ChessErrs.ErrInvMove):
        super(InvMoveExc, self).__init__(msg, err)


class InvColourExc(ChessExc):
    """ChessGame "invalid colour" exception"""

    def __init__(self, msg="Invalid colour", err=ChessErrs.ErrInvColour):
        super(InvColourExc, self).__init__(msg, err)


class ChessTurn:
    """ChessGame turn i.e. 'white' or 'black'"""

    turn_dict = {"white": 0, "black": 1}

    def __init__(self, colour="white") -> None:
        colour = colour.lower()
        assert colour in self.turn_dict
        self.turn = self.turn_dict[colour]

    def toggle_turn(self):
        """Change turn to other"""
        if self.turn == self.turn_dict["black"]:
            self.turn = self.turn_dict["white"]
        else:
            self.turn = self.turn_dict["black"]

    def test_turn(self, colour):
        """Return True if turn is colour"""
        return self.turn_dict[colour.lower()] == self.turn
    
    def get_turn_colour(self):
        colour = ''
        for k in self.turn_dict:
            if self.turn_dict[k] == self.turn:
                colour=k
                break
        return colour

class Position():

    pos_fmt = r"\([0-7]\s*,\s*[0-7]\)"
    notation_fmt = r"[A-Ha-h][1-8]"
    pos_or_not_fmt = f"{pos_fmt}|{notation_fmt}"

    # (row, col) position tuple or notation
    def __init__(self, pos_or_not=None):
        self.set_pos(pos_or_not)
    
    def set_pos(self, pos_or_not):
        (self.position, self.notation) = \
                    Position.pos_or_notation(pos_or_not)
    
    def get_pos(self):
        # return tuple (pos, notation)
        return (self.position, self.notation)

    def pos(self):
        return self.position
    
    def notation(self):
        return self.notation
    
    def __repr__(self):
        return f"{self.position}:{self.notation}"

    @staticmethod
    def pos_or_notation(pos_or_not):
        # Return (pos, notation), input can be pos or notation
        res = (None, None)
        pos = Position.notation_pos(pos_or_not)
        if pos:
            res = (pos, pos_or_not)
        else:
            _not = Position.pos_notation(pos_or_not)
            if _not:
                res = (pos_or_not, _not)
        return res

    @staticmethod
    def pos_notation(pos):
        # pos to notation, return None if invalid
        res = None
        if pos and len(pos) == 2:
            (row, col) = pos
            if row >= 0 and row < 8 and col >= 0 and col < 8:
                res = f"{chr(ord('a') + col)}{8 - row}" 
        return res

    @staticmethod
    def notation_pos(notation):
        # notation  [a-h][1-8] to tuple (row, col), return if invalid
        pos = None
        if isinstance(notation, str) and len(notation) == 2:
            token = notation.lower()
            col = ord(token[0]) - ord("a")  # col 'a' is table column 0
            row = 8 - int(token[1])  # row 1 is table row 7
            if row >= 0 and row < 8 and col >= 0 and col < 8:
                pos = (row, col)
        return pos

    @staticmethod
    def position_token(token):
        """Return tuple (row, col) from parsed token, else None
        String fmt :: '(<row>, <col>)' | '[a-h][1-8]'
           first char row:[a-h], second char col:[1-8]
             eg. 'a8' == (0,0), 'a1' == (7,0), 'h1' == (7,7), 'h8' == (0,7)
        """
        pos = None
        row = -1
        col = -1

        if not token or (not isinstance(token, str)):
            if len(token) == 2:
                pos = token # assume list or tuple eg. (0, 0)
            return pos

        if len(token) == 2:
            (row, col) = Position.notation_pos(token)
        else:
            if re.match(Position.pos_fmt, token):
                row = int(token[1])
                col = int(token[3])
        if row >= 0 and row < 8 and col >= 0 and col < 8:
            pos = (row, col)
        return pos 

class ChessAPI(ChessTurn, Position):
    """ChessGame functions that can be invoked from cmdline e.g:
    from ChessGame import *
    game=Headless_ChessGame():
    command = 'Pe2:e4; pd7:d5; Bf1:b5; ph7:h5'
    (ncommands, errs) = game.commands(command)
    assert ncommands == 4 and len(errs) == 0
    game.dump()
    game.save_file('test.txt')
    """

    def __init__(self):
        super(ChessTurn, self).__init__()

    def raise_exc(self, err):
        exc = None
        if err == ChessErrs.ErrCheckMate:
            exc = CheckMateExc
        elif err == ChessErrs.ErrCheck:
            exc = CheckExc
        elif err == ChessErrs.ErrInvMove:
            exc = InvMoveExc
        elif err == ChessErrs.ErrInvColour:
            exc = InvColourExc
        if exc:
            raise exc

    def get_piece(self, row, col):
        """Return GameObject at (row, col)"""
        return self.board[row][col]
    
    def get_piece_notation(self, pos_or_not):
        """Return GameObject at algebraic notation e.g. e4"""
        res = None
        pos = Position(pos_or_not).pos()
        if pos:
            res = self.get_piece(*pos)
        return res

    def get_from_piece(self):
        """Return GameObject at previously selected from_pos"""
        return self.selected_piece_to_move  # self.get_piece(*self.from_pos)

    def get_from_pos(self):
        from_piece = self.get_from_piece()
        return (from_piece.row, from_piece.column)

    def movefrom(self, row, col):
        """Select (row, col) to move from"""
        Allowed_to_select = self.select_piece_to_move((row, col))
        if Allowed_to_select[0]:
            err = Allowed_to_select[0]
            self.raise_exc(err)

        return self.get_piece(row, col)

    def moveto(self, row, col):
        """Select (row, col) to move too"""
        from_pos = self.get_from_pos()
        Allowed_to_select = self.move_selected_piece((row, col))
        if Allowed_to_select[0]:
            err = Allowed_to_select[0]
            self.raise_exc(err)

        to_square = self.get_piece(row, col)
        to_square.history.append((from_pos, (row, col)))
        return to_square

    def move(self, from_pos, to_pos):
        """Move piece at from_pos to to_pos"""
        from_piece = self.movefrom(*from_pos)
        to_piece = self.moveto(*to_pos)
        return to_piece

    @staticmethod
    def new_board():
        """Clear board of all pieces"""
        board = [[None] * 8 for row in range(8)]
        return board
    
    def notation_piece(self, token):
        """Return tuple (<class>, colour) if token starts with a piece abbrv, else None.
        one char abbrv of piece (R N B Q K P) or 'D' for board.dump,
        upper case is white, lower black e.g. N is white knight, n is black
        """
        piece = None
        pieces = {
            "R": Rook,
            "N": Knight,
            "B": Bishop,
            "Q": Queen,
            "K": King,
            "P": Pawn,
            "D": "dump",
        }
        if len(token) == 1:
            p = token[0]
            colour = "White" if p.isupper() else "Black"
            p = p.upper()
            if p in pieces:
                if p == "D":
                    piece = ()  # empty
                    print(f"Notation dump: {self.dump()}")
                else:
                    piece = (pieces[p], colour)
        return piece

    def commands(self, command):
        """Run command string fmt:: [<piece_creations>] <piece_moves>
        Returns tuple (ncommands, errs) where:
          ncommands :: number of commands in string
          errs :: empty list [] if no errors, else error list [err_index, err_val, err_mess]
            err_index :: command index
            err_val :: error value
            err_mess :: error message
        """
        """
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
        """
        errs = []
        tokens = command.split(";")
        ncommands = len(tokens)
        for (indext, token) in enumerate(tokens):
            token = re.sub(r"\s+", "", token)  # remove whitespace
            m = re.match(r"[Dd]$", token)
            if m:
                print(f"Notation dump: {self.dump()}")
                continue

            pieces = "RNBQKP"
            pieces_fmt = f"[{pieces}{pieces.lower()}]"
            pos_fmt = Position.pos_or_not_fmt
            m = re.match(f"({pieces_fmt})({pos_fmt}):?({pos_fmt})?$", token)
            groups = m.groups() if m else None
            # print(f"DBG token {token} == {groups}")
            if groups == None or (groups[0] == None and groups[-1] == None):
                err_mess = f"invalid command token index [{indext}]:{token}"
                errs.append((indext, ChessErrs.ErrInvCommand, err_mess))
                continue

            np = self.notation_piece(groups[0])
            if np == None:
                continue
            from_pos = Position.position_token(groups[1])
            piece = self.get_piece(*from_pos)
            to_pos = None
            if groups[2]:
                to_pos = Position.position_token(groups[2])

            if to_pos:
                if piece and piece.abbrv == groups[0]:
                    # move e.g. Ke1:d2; expects match piece at from_pos:
                    try:
                        self.move(from_pos, to_pos)
                    except ChessExc as exc:
                        err_mess = f"command token index [{indext}]:{token} move({from_pos}, {to_pos}) raised an exception {exc}"
                        errs.append((indext, exc.err, err_mess))
                else:
                    err_mess = f"invalid command token index [{indext}]:{token} mismatch move {piece} ({from_pos}, {to_pos}"
                    errs.append((indext, ChessErrs.ErrInvCommandMove, err_mess))
            else:
                np = None
                if piece == None:
                    # New piece only if square empty
                    np = self.notation_piece(token[0])
                if np:
                    # create new piece
                    self.board[from_pos[0]][from_pos[1]] = np[0](
                        np[1], from_pos[1], from_pos[0]
                    )
                else:
                    err_mess = f"invalid command token index [{indext}]:{token}, existing piece {piece.piece} {from_pos}"
                    errs.append((indext, ChessErrs.ErrInvCommandMove, err_mess))

        return (ncommands, errs)

    def save_file(self, filename):
        """Save to filename"""
        with open(filename, "w") as filehandle:
            filehandle.write(f"{str(self.turn)}\n")
            for row_number in range(0, 8):
                for column_number in range(0, 8):
                    if self.board[row_number][column_number] != None:
                        _piece = self.board[row_number][column_number].piece
                        _colour = self.board[row_number][column_number].colour
                        _line = f"{_piece} {_colour} {row_number} {column_number}\n"
                        filehandle.write(_line)

    def dump(self, unicode=False):
        """text summary of board"""
        str = ""
        for row_number in range(0, 8):
            linebuff = f" {8-row_number}" if unicode else ""
            for column_number in range(0, 8):
                piece = self.board[row_number][column_number]
                c = "." if piece == None else piece.abbrv
                if unicode:
                    c = f" {Pawn.uni_pieces[c]}"
                linebuff = f"{linebuff}{c}"
            str = f"{str}\n{linebuff}"
        if unicode:
            str = f"{str}\n   a b c d e f g h \n"
        return str

    def __repr__(self):
        # string representation
        return f"{self.__class__} : {vars(self)}"
