from chess_pieces import PIECE_BISHOP, PIECE_KING, PIECE_KNIGHT, PIECE_PAWN, PIECE_QUEEN, PIECE_ROOK
from chess_pieces import Piece, Pawn, Rook, Knight, Bishop, Queen, King, COLOUR_WHITE, COLOUR_BLACK
from json import loads as json_loads
from chess_api import ChessAPI
from requests import get
from math import floor

URL = "https://raw.githubusercontent.com/Taonga07/ChessGame/master/resources/"

class HeadlessChess(ChessAPI):
    def __init__(self, file=get(URL+"board.json").content) -> None:
        super().__init__()
        self.board, self.turn = self.read_game_data(file)

    def read_game_data(self, file):
        board = [[None] * 8 for row in range(8)]
        board_data = json_loads(file)
        turn = board_data["turn"]
        for id, piece in enumerate(board_data["pieces"]):
            piece_colour, piece_type, piece_pos = piece
            row, column = piece_pos
            if piece_type == PIECE_PAWN:
                board[row][column] = Pawn(piece_colour, piece_pos, id)
            elif piece_type == PIECE_ROOK:
                board[row][column] = Rook(piece_colour, piece_pos, id)
            elif piece_type == PIECE_KNIGHT:
                board[row][column] = Knight(piece_colour, piece_pos, id)
            elif piece_type == PIECE_BISHOP:
                board[row][column] = Bishop(piece_colour, piece_pos, id)
            elif piece_type == PIECE_QUEEN:
                board[row][column] = Queen(piece_colour, piece_pos, id)
            elif piece_type == PIECE_KING:
                board[row][column] = King(piece_colour, piece_pos, id)
            else:
                raise Exception("Invalid Piece Type")
        return board, turn

    def check_for_checkmate(self, clicked_piece):
        pieces_that_cant_move, piece_on_board = 0, 0
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if self.board[row_number][column_number] is not None:
                    if (
                        clicked_piece.colour
                        == self.board[row_number][column_number].colour
                    ):
                        if self.check_against_check(
                            self.board[row_number][column_number]
                        ):
                            pieces_that_cant_move += 1
                        piece_on_board += 1
        if piece_on_board == pieces_that_cant_move:
            return True
        return False

    def check_against_check(self, clicked_piece):
        # if you are in check get out of it
        paths_to_king, atackers_pos = [], []
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if (self.board[row_number][column_number] is not None) and (
                    self.board[row_number][column_number].colour != clicked_piece.colour
                ):
                    self.board[row_number][column_number].find_moves(self.board, [])
                    for move in self.board[row_number][column_number].possible_moves:
                        square = self.board[move[0]][move[1]]  # row, column
                        if (
                            (square is not None)
                            and (square.piece == "King")
                            and (square.colour == clicked_piece.colour)
                        ):  # our king is in check
                            atackers_pos.append((row_number, column_number))
                            paths_to_king += self.board[row_number][
                                column_number
                            ].find_path_to_king(move[0], move[1])
                            # code above should add to the paths_to_king it
                            # values not the whole list
        clicked_piece.find_moves(self.board, paths_to_king)
        if len(paths_to_king) > 0:  # you are in check
            if len(clicked_piece.possible_moves) == 0:
                return True  # we can't move
        return False

    def select_piece_to_move(self, square_clicked):
        piece_clicked = self.board[square_clicked[0]][square_clicked[1]]
        if self.check_piece_colour_against_turn(piece_clicked):
            if self.check_for_checkmate(piece_clicked):
                return ChessErrs.ErrCheckMate, ("Checkmate", "End of Game")
            if self.check_against_check(piece_clicked):
                return ChessErrs.ErrCheck, ("Check", "You can not move this piece")
            else:
                self.selected_piece_to_move = piece_clicked
                return ChessErrs.ErrNone, ("Move Allowed", "You can move this piece")
        else:
            return ChessErrs.ErrInvMove, (
                "Move Not Allowed",
                "You Have not selected one of your pieces",
            )

    def check_piece_colour_against_turn(self, piece_clicked):
        if piece_clicked is not None:  # We have clicked a piece
            if self.test_turn(piece_clicked.colour):
                return True
            else:
                raise InvColourExc
        return False
    
    def move_board(self, piece, dest):
        # move GameObject piece to dest (row, col)
        (dest_row, dest_col) = dest
        self.board[dest_row][dest_col] = piece

        self.board[piece.row][piece.column] = None
        (piece.row, piece.column) = (dest_row, dest_col)
        self.nturn += 1

    def move_selected_piece(self, square_clicked):
        clicked_row, clicked_cloumn = square_clicked
        piece_to_move = self.selected_piece_to_move
        if (
            clicked_row,
            clicked_cloumn,
        ) not in piece_to_move.possible_moves:
            return ChessErrs.ErrInvMove, (
                "Move Not Allowed",
                "Your piece cannot move there!",
            )
        self.move_board(piece_to_move, square_clicked)
        self.toggle_turn()
        return ChessErrs.ErrNone, ("Move Allowed", "You can move here")

    def get_pieces(self) -> dict:
        "Returns a dictionary of all the pieces on the board"
        pieces = {}
        for square in [y for x in self.board for y in x]:
            if square is not None:
                pieces[square.id] = {
                    "piece": square.piece,
                    "colour": square.colour,
                    "pos": [square.column, square.row]
                }
        return pieces
    
    def get_piece(self, piece_id) -> Piece:
        "Returns a piece from the board"
        for row, column in self.board:
            square = self.board[row][column]
            if square is not None:
                if square.id == piece_id:
                    return square
        return None
    
    def highlight_moves(self, piece_id) -> dict:
        "returns dictionary of possible moves for a piece"
        highlighted_squares = {(0,125,0):[], (125,0,0):[], (0,0,125):id}
        piece = self.get_piece(piece_id)
        piece.find_possible_moves(self.board)
        for move in piece.possible_moves:
            dest_square = self.board[move[0]][move[1]]
            if dest_square is None: # if empty square
                highlighted_squares["green"].append(self.index_2d(move))
            else: # if square is occupied
                highlighted_squares["red"].append(self.index_2d(move))
        return highlighted_squares

    def index_2d(self, index) -> int:
        "convert index of an array to the index for a martix"
        return (index[0] * 8) + index[1]

    def index_1d(self, index) -> tuple:
        "convert index of a matrix to the index of an array"
        return (index%8, floor(index / 8))