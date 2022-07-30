from ChessGame.API import ChessAPI, ChessErrs, InvColourExc
from json import loads as json_loads
import ChessGame.Pieces as Pieces
from requests import get

URL = "https://raw.githubusercontent.com/Taonga07/ChessGame/fixes/resources/"

class Headless_ChessGame():
    def __init__(self, file=get(URL+"board.json").content) -> None:
        self.board, self.turn = self.read_game_data(file)

    def read_game_data(self, file):
        board = [[None] * 8 for row in range(8)]
        board_data = json_loads(file)
        turn = board_data["turn"]
        for piece in board_data["pieces"]:
            type, colour, position = piece
            row, column = position
            if type == Pieces.PIECE_PAWN:
                board[row][column] = Pieces.Pawn(colour, position)
            elif type == Pieces.PIECE_ROOK:
                board[row][column] = Pieces.Rook(colour, position)
            elif type == Pieces.PIECE_KNIGHT:
                board[row][column] = Pieces.Knight(colour, position)
            elif type == Pieces.PIECE_BISHOP:
                board[row][column] = Pieces.Bishop(colour, position)
            elif type == Pieces.PIECE_QUEEN:
                board[row][column] = Pieces.Queen(colour, position)
            elif type == Pieces.PIECE_KING:
                board[row][column] = Pieces.King(colour, position)
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