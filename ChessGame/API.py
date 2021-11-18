import re
from Pieces import Pawn, Rook, Knight, Bishop, Queen, King


class ChessErrs:
    """ChessGame error values"""

    ErrCheckMate = -1
    ErrCheck = -2
    ErrInvMove = -3
    ErrInvCommand = -4  # invalid command token
    ErrInvCommandMove = -5  # invalid move command


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


class ChessAPI(ChessTurn):
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

    def get_piece(self, row, col):
        """Return GameObject at (row, col)"""
        return self.board[row][col]

    def get_from_piece(self):
        """Return GameObject at previously selected from_pos"""
        return self.get_piece(*self.from_pos)

    def movefrom(self, row, col):
        """Select (row, col) to move from"""
        from_square = self.get_piece(row, col)

        if (from_square != None) and (self.test_turn(from_square.colour)):
            if self.check_for_checkmate(from_square):
                raise CheckMateExc
            if self.check_against_check(from_square):  # we are in check
                self.toggle_turn()
                raise CheckExc
            else:  # limit moves if in check else normal moves
                self.from_pos = (row, col)
        else:  # if there is no piece or wrong colour piece where we clicked
            self.toggle_turn()
            raise InvMoveExc

        return from_square

    def moveto(self, row, col):
        """Select (row, col) to move too"""
        from_square = self.get_from_piece()
        from_pos = (from_square.row, from_square.column)

        if (
            row,
            col,
        ) not in from_square.possible_moves:  # check possible move for piece
            raise InvMoveExc

        self.board[row][col] = from_square
        self.board[from_pos[0]][from_pos[1]] = None

        to_square = self.get_piece(row, col)
        to_square.history.append((from_pos, (row, col)))
        to_square.row = row
        to_square.column = col
        self.toggle_turn()
        return to_square

    def move(self, from_pos, to_pos):
        """Move piece at from_pos to to_pos"""
        from_piece = self.movefrom(*from_pos)
        to_piece = self.moveto(*to_pos)
        return to_piece

    def new_board(self):
        """Clear board of all pieces"""
        board = [[None] * 8 for row in range(8)]
        return board

    def notation_pos(self, token):
        """Return tuple (row, col) from parsed token, else None
        String fmt :: '(<row>, <col>)' | '[a-h][1-8]'
           first char row:[a-h], second char col:[1-8]
             eg. 'a8' == (0,0), 'a1' == (7,0), 'h1' == (7,7), 'h8' == (0,7)
        """
        pos = None
        row = -1
        col = -1

        if len(token) == 2:
            token = token.lower()
            col = ord(token[0]) - ord("a")  # col 'a' is table column 0
            row = 8 - int(token[1])  # row 1 is table row 7
        else:
            if re.match(r"\([0-7],[0-7]\)$", token):
                row = int(token[1])
                col = int(token[3])
        if row >= 0 and row < 8 and col >= 0 and col < 8:
            pos = (row, col)
        return pos

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
            pos_fmt = r"\([0-7],[0-7]\)|[A-ha-h][1-8]"
            m = re.match(f"({pieces_fmt})({pos_fmt})\:?({pos_fmt})?$", token)
            groups = m.groups() if m else None
            # print(f"DBG token {token} == {groups}")
            if groups == None or (groups[0] == None and groups[-1] == None):
                err_mess = f"invalid command token index [{indext}]:{token}"
                errs.append((indext, ChessErrs.ErrInvCommand, err_mess))
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
                        errs.append((indext, exc.err, err_mess))
                else:
                    err_mess = f"invalid command token index [{indext}]:{token} mismatch move {piece} ({from_pos}, {to_pos}"
                    errs.append(
                        (indext, ChessErrs.ErrInvCommandMove, err_mess))
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
                    errs.append(
                        (indext, ChessErrs.ErrInvCommandMove, err_mess))

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

    def dump(self):
        """text summary of board"""
        str = ""
        for row_number in range(0, 8):
            linebuff = ""
            for column_number in range(0, 8):
                piece = self.board[row_number][column_number]
                c = "." if piece == None else piece.abbrv
                linebuff = f"{linebuff}{c} "
            str = f"{str}\n{linebuff}"
        return str

    def __repr__(self):
        # string representation
        return f"{self.__class__} : {vars(self)}"
