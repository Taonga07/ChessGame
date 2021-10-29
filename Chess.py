from tkinter import messagebox, PhotoImage, Tk, Label, N, S, W, E
from Pieces import Pawn, Rook, Bishop, Queen, King, Knight
from os.path import join, expanduser
import sys


class ChessGame:
    def __init__(self, window, square_colours=("White", "Grey"), file="New_Game.txt"):
        self.window, self.click, self.first_click = window, 1, (0, 0)
        self.board, self.turn = self.read_game_data(file)
        self.square_colours = square_colours
        self.layout_board()

    def read_game_data(self, file):
        board = [[None] * 8 for row in range(8)]
        input_data = open(join(expanduser("~"), ".Chess_Games", file), "r").readlines()
        for i, line in enumerate(input_data):
            if i == 0:
                turn = int(line.rstrip())
            else:
                Piece, Colour, Row, Column = line.rstrip().split(" ")
                piece = eval(Piece + "(str(Colour), int(Column), int(Row))")
                board[int(piece.row)][int(piece.column)] = piece
        return board, turn

    def layout_board(self):
        bttnclr_turn = 0
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                square_colour = self.square_colours[bttnclr_turn]
                if self.board[row_number][column_number] is None:
                    text, img = "                 \n\n\n", None
                else:
                    img, text = (
                        PhotoImage(file=self.board[row_number][column_number].icon),
                        None,
                    )
                square = Label(self.window, text=text, bg=square_colour, image=img)
                grid_slaves = self.window.grid_slaves(row_number, column_number)
                if len(grid_slaves) > 0:
                    for g in grid_slaves:
                        g.destroy()
                square.image = img
                square.grid(row=row_number, column=column_number, sticky=N + S + W + E)
                square.bind("<Button-1>", self.on_click)
                bttnclr_turn = 1 - bttnclr_turn
            bttnclr_turn = 1 - bttnclr_turn

    def check_against_check(self, clicked_piece):
        # if you are in check get out of it
        paths_to_king, atackers_pos = [], []
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if (
                    (self.board[row_number][column_number] is not None)
                    and (self.board[row_number][column_number].colour
                    != clicked_piece.colour)
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

    def on_click(self, event):
        self.click = 1 - self.click
        square_info = event.widget.grid_info()
        current_square = (int(square_info["row"]), int(square_info["column"]))
        square_clicked = self.board[current_square[0]][current_square[1]]
        if self.click == 0:  # on fist click we are select a piece
            if (square_clicked is not None) and (
                ((self.turn == 0) and (square_clicked.colour == "White"))
                or ((self.turn == 1) and (square_clicked.colour == "Black"))
            ):
                if self.check_for_checkmate(square_clicked):
                    messagebox.showinfo("Checkmate", "Checkmate end of game")
                    while True:
                        pass
                if self.check_against_check(square_clicked):  # we are in check
                    messagebox.showinfo("Check", "you're in check")
                    self.click = 1 - self.click
                else:  # limit moves if in check else normal moves
                    event.widget.config(bg="blue")  # highlight clicked square
                    square_clicked.highlight_moves(self.window, self.board)
                    self.first_click = (current_square[0], current_square[1])
            else:  # if there is no piece or wrong colour piece where we clicked
                messagebox.showinfo(
                    "Move Not Allowed", "No/Your piece there, try again"
                )
                self.click = 1 - self.click
        else:  # this is our second click, we are selecting the square to move to
            old_piece = self.board[self.first_click[0]][self.first_click[1]]
            if (
                current_square[0],
                current_square[1],
            ) not in old_piece.possible_moves:  # check possible move for piece
                messagebox.showinfo("Move Not Allowed", "Your piece cannot move there!")
                self.layout_board()  # reset board
                return
            self.board[current_square[0]][current_square[1]] = self.board[
                self.first_click[0]
            ][self.first_click[1]]
            self.board[current_square[0]][current_square[1]].row = current_square[0]
            self.board[current_square[0]][current_square[1]].column = current_square[1]
            self.board[self.first_click[0]][self.first_click[1]] = None
            self.layout_board()  # reset board
            self.turn = 1 - self.turn
