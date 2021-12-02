from os.path import dirname, abspath, join
import sys


class GameObject:
    uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
    def __init__(self, piece, colour, column, row, value):
        self.row, self.value, self.piece, self.InCheck = row, value, piece, False
        self.colour, self.column, self.possible_moves = colour, column, []
        base_path = getattr(sys, "_MEIPASS", dirname(abspath(__file__)))
        self.icon = join(
            base_path, "Chess_Resources", self.colour + "_" + self.piece + ".gif"
        )
        # first char, e.g. 'P' for Pawn
        self.abbrv = "N" if self.piece == "Knight" else self.piece[0]
        if self.colour == "Black":
            self.abbrv = (
                self.abbrv.lower()
            )  # e.g. 'p' for Pawn, or 'n' for black knight
        self.history = []


    def find_possible_moves(self, board, pieces_to_jump=0):
        pass

    def highlight_moves(self, window, board):
        for row_number, column_number in self.possible_moves:
            squarex = window.grid_slaves(row=row_number, column=column_number)
            if len(squarex) > 1:
                print(
                    f"warning, this square has more than one grid slave!!! {row_number}, {column_number}. count: {len(squarex)}"
                )
            square = squarex[0]  # returns list of widgets
            dest_square = board[row_number][column_number]
            if dest_square is None:  # if there is nothing at position i
                square.config(bg="green")  # highlight position i green
            else:  # none has no attrubrite to clour this stops this error
                square.config(bg="red")  # highlight position i red

    def remove_check_moves(self, board):
        local_moves = []
        for row in range(8):
            for column in range(8):
                if self.piece == "king":
                    for move in self.possible_moves:
                        # if it is not my own piece
                        if (board[row][column] is not None) and (
                            board[row][column] != board[self.row][self.column]
                        ):
                            # generate moves from piece we are checking to edge
                            # of board as if we had moved
                            if (self.row, self.column) in board[row][
                                column
                            ].path_past_self(board):
                                local_moves.append(move)
                # else:  # if king not piece clicked clicked we check if the king is on our row
                # if (
                #     (board[row][column] is not None)
                #     and (board[row][column].piece == "King")
                #     and (board[row][column].colour == self.colour)
                # ):
                #     if (row, column) in board[row][column].path_past_self(board, (self.row, self.column)):
                #         self.possible_moves = []
                #         return
        # remove moves
        for move in local_moves:
            self.possible_moves.remove(move)

    def explore_moves(self, direction, board, pieces_to_jump=0):
        working_value = self.row, self.column
        moves = []
        while True:
            working_value = (
                (working_value[0] + direction[0]),
                (working_value[1] + direction[1]),
            )
            if (
                (working_value[0] >= 0)
                and (working_value[0] <= 7)
                and (working_value[1] >= 0)
                and (working_value[1] <= 7)
            ):
                dest_square = board[working_value[0]][working_value[1]]
                if dest_square is None:
                    moves.append(working_value)
                else:
                    if dest_square.colour != self.colour:
                        if pieces_to_jump == 0:
                            moves.append(working_value)
                            break
                        pieces_to_jump -= 1
                    else:
                        break
            else:
                break
        return moves

    def find_moves(self, board, path_to_king):
        self.possible_moves = []
        self.find_possible_moves(board)
        if len(path_to_king) > 0:  # if we are in check
            if self.piece == "King":  # king can move out of check

                self.possible_moves = [
                    move for move in self.possible_moves if move not in path_to_king
                ]
            else:  # king can not block itelf from check
                # remove piece in possible moves that is not your colour
                self.possible_moves = list(set(self.possible_moves) & set(path_to_king))
        possible_moves = []
        for move in self.possible_moves:
            moving_piece = board[move[0]][move[1]]
            if (
                (moving_piece is not None) and (moving_piece.colour != self.colour)
            ) or (moving_piece is None):
                possible_moves.append(move)
        self.possible_moves = possible_moves
        self.remove_check_moves(board)

    def find_path_to_king(self, king_row, king_column):
        if self.piece != "Knight":  # attcking knight can only be taken
            if king_column - self.column != 0:
                column_dir = int(
                    (king_column - self.column) / (abs(king_column - self.column))
                )
                column_path = list(range(self.column, king_column, column_dir))
            if king_row - self.row != 0:
                row_dir = int((king_row - self.row) / (abs(king_row - self.row)))
                row_path = list(range(self.row, king_row, row_dir))
            if king_column - self.column == 0:
                column_path = [king_column] * len(row_path)
            elif king_row - self.row == 0:
                row_path = [king_row] * len(column_path)
            return list(zip(row_path, column_path))
        return [(self.row, self.column)]

    def path_past_self(self, board):  # pylint: disable=R1710
        if (self.piece != "Knight") and (self.piece != "Pawn"):
            return self.find_possible_moves(board, pieces_to_jump=1)
        elif self.piece == "Pawn":
            if self.column < 7:
                return [
                    ((self.row + self.direction), (self.column + 1))
                ]  # pylint: disable=E1101
            if self.column > 1:
                return [
                    ((self.row + self.direction), (self.column - 1))
                ]  # pylint: disable=E1101
            # pylint: enable=E1101
        else:
            return self.find_possible_moves(board)

    def __repr__(self):
        # string representation
        # return f"({self.__class__}){self} : {vars(self)}"
        return f"{self.__class__} : {vars(self)}"


class Pawn(GameObject):
    def __init__(self, colour, column, row):
        super().__init__("Pawn", colour, column, row, 1)
        if self.colour == "White":
            self.direction = -1
        else:
            self.direction = 1

    def first_move(self):
        if ((self.row == 1) and (self.colour == "Black")) or (
            (self.row == 6) and (self.colour == "White")
        ):
            return True
        return False

    def find_possible_moves(self, board, pieces_to_jump=0):
        if board[self.row + self.direction][self.column] is None:
            self.possible_moves.append(((self.row + self.direction), self.column))
            if self.first_move():
                if board[self.row + (self.direction * 2)][self.column] is None:
                    self.possible_moves.append(
                        ((self.row + (self.direction * 2)), self.column)
                    )
        if self.column > 1:
            dest_square = board[self.row + self.direction][self.column - 1]
            if (dest_square is not None) and (dest_square.colour != self.colour):
                # take left
                self.possible_moves.append(
                    ((self.row + self.direction), (self.column - 1))
                )
        if self.column < 7:
            dest_square = board[self.row + self.direction][self.column + 1]
            if (dest_square is not None) and (dest_square.colour != self.colour):
                # take right
                self.possible_moves.append(
                    ((self.row + self.direction), (self.column + 1))
                )


class Rook(GameObject):
    def __init__(self, colour, column, row):
        super().__init__("Rook", colour, column, row, 4)

    def find_possible_moves(self, board, pieces_to_jump=0):
        self.possible_moves.extend(
            self.explore_moves((-1, 0), board, pieces_to_jump)
        )  # up
        self.possible_moves.extend(
            self.explore_moves((0, +1), board, pieces_to_jump)
        )  # right
        self.possible_moves.extend(
            self.explore_moves((0, -1), board, pieces_to_jump)
        )  # left
        self.possible_moves.extend(
            self.explore_moves((+1, 0), board, pieces_to_jump)
        )  # down


class Bishop(GameObject):
    def __init__(self, colour, column, row):
        super().__init__("Bishop", colour, column, row, 3)

    def find_possible_moves(self, board, pieces_to_jump=0):
        self.possible_moves.extend(
            self.explore_moves((-1, -1), board, pieces_to_jump)
        )  # up left
        self.possible_moves.extend(
            self.explore_moves((-1, +1), board, pieces_to_jump)
        )  # up right
        self.possible_moves.extend(
            self.explore_moves((+1, -1), board, pieces_to_jump)
        )  # down left
        self.possible_moves.extend(
            self.explore_moves((+1, +1), board, pieces_to_jump)
        )  # down right


class King(GameObject):
    def __init__(self, colour, column, row):
        super().__init__("King", colour, column, row, 1)
        self.check_moves = []

    def find_possible_moves(self, board, pieces_to_jump=0):
        if self.row > 0:
            self.possible_moves.append((self.row - 1, self.column))
            if self.column > 0:
                self.possible_moves.append((self.row - 1, self.column - 1))
            if self.column < 7:
                self.possible_moves.append((self.row - 1, self.column + 1))
        if self.row < 7:
            self.possible_moves.append((self.row + 1, self.column))
            if self.column > 0:
                self.possible_moves.append((self.row + 1, self.column - 1))
            if self.column < 7:
                self.possible_moves.append((self.row + 1, self.column + 1))
        if self.column < 7:
            self.possible_moves.append((self.row, self.column + 1))
        if self.column > 0:
            self.possible_moves.append((self.row, self.column - 1))


class Queen(GameObject):
    def __init__(self, colour, column, row):
        super().__init__("Queen", colour, column, row, 9)

    def find_possible_moves(self, board, pieces_to_jump=0):
        self.possible_moves.extend(
            self.explore_moves((-1, -1), board, pieces_to_jump)
        )  # up left
        self.possible_moves.extend(
            self.explore_moves((-1, +1), board, pieces_to_jump)
        )  # up right
        self.possible_moves.extend(
            self.explore_moves((+1, -1), board, pieces_to_jump)
        )  # down left
        self.possible_moves.extend(
            self.explore_moves((+1, +1), board, pieces_to_jump)
        )  # down right
        self.possible_moves.extend(
            self.explore_moves((-1, 0), board, pieces_to_jump)
        )  # up
        self.possible_moves.extend(
            self.explore_moves((0, +1), board, pieces_to_jump)
        )  # right
        self.possible_moves.extend(
            self.explore_moves((0, -1), board, pieces_to_jump)
        )  # left
        self.possible_moves.extend(
            self.explore_moves((+1, 0), board, pieces_to_jump)
        )  # down


class Knight(GameObject):
    def __init__(self, colour, column, row):
        super().__init__("Knight", colour, column, row, 5)

    def find_possible_moves(self, board, pieces_to_jump=0):
        if (self.row < 6) and (self.column > 0):
            self.possible_moves.append((self.row + 2, self.column - 1))
        if (self.row < 6) and (self.column < 7):
            self.possible_moves.append((self.row + 2, self.column + 1))
        if (self.row > 1) and (self.column > 0):
            self.possible_moves.append((self.row - 2, self.column - 1))
        if (self.row > 1) and (self.column < 7):
            self.possible_moves.append((self.row - 2, self.column + 1))
        if (self.row > 0) and (self.column < 6):
            self.possible_moves.append((self.row - 1, self.column + 2))
        if (self.row < 7) and (self.column < 6):
            self.possible_moves.append((self.row + 1, self.column + 2))
        if (self.row > 0) and (self.column > 1):
            self.possible_moves.append((self.row - 1, self.column - 2))
        if (self.row < 7) and (self.column > 1):
            self.possible_moves.append((self.row + 1, self.column - 2))


pieces = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
