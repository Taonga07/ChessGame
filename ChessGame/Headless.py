from Pieces import (  # pylint: disable=W0611, import-error
    Pawn,
    Rook,
    Bishop,
    Queen,
    King,
    Knight,
)  # pylint: enable=W0611, import-error
from os.path import expanduser, isdir, join, abspath, dirname
from shutil import copytree

from API import *

class Headless_ChessGame(ChessAPI):
    def __init__(self, file="New_Game.txt") -> None:
        super(ChessAPI, self).__init__()

        self.create_game_save_folder()  # give user template game_files
        self.from_pos = (0, 0)  # previously 'first_click'
        if file:
            self.board, self.turn = self.read_game_data(file)
        else:
            self.board = self.new_board()

    def create_game_save_folder(self):
        if not isdir(
            join(expanduser("~"), ".Chess_Games")
        ):  # check if homepath of user + folder exists
            # if folder dosen't create and copy templates across
            copytree(
                abspath(join("ChessGame", "Games")),
                join(expanduser("~"), ".Chess_Games"),
            )

    def read_game_data(
        self, Game_File, Game_Folder=abspath(join(dirname(__file__), "Games"))
    ):
        board = [[None] * 8 for row in range(8)]
        input_data = open(join(Game_Folder, Game_File), "r").readlines()
        for i, line in enumerate(input_data):
            if i == 0:
                turn = int(line.rstrip())
            else:
                Piece, Colour, Row, Column = line.rstrip().split(
                    " "
                )  # pylint: disable=W0612
                # pylint: enable=W0612
                piece = eval(Piece + "(str(Colour), int(Column), int(Row))")
                board[int(piece.row)][int(piece.column)] = piece
        return board, turn

    def save_game_data(self, Path_to_save_in):
        with open(Path_to_save_in, "w") as filehandle:
            filehandle.write(f"{str(self.turn)}\n")
            for row_number in range(0, 8):
                for column_number in range(0, 8):
                    if self.board[row_number][column_number] is not None:
                        _piece = self.board[row_number][column_number].piece
                        _colour = self.board[row_number][column_number].colour
                        _line = f"{_piece} {_colour} {row_number} {column_number}\n"
                        filehandle.write(_line)

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

    def move_selected_piece(self, square_clicked):
        clicked_row, clicked_cloumn = square_clicked
        piece_to_move = self.selected_piece_to_move
        if (
            clicked_row,
            clicked_cloumn,
        ) not in piece_to_move.possible_moves:
            return ChessErrs.ErrInvMove, ("Move Not Allowed", "Your piece cannot move there!")
        self.board[clicked_row][clicked_cloumn] = self.board[piece_to_move.row][
            piece_to_move.column
        ]
        self.board[piece_to_move.row][piece_to_move.column] = None
        piece_to_move.row = clicked_row
        piece_to_move.column = clicked_cloumn
        self.toggle_turn()
        return ChessErrs.ErrNone, ("Move Allowed", "You can move here")
