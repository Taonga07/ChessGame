PIECE_KNIGHT, PIECE_ROOK, PIECE_PAWN = range(3,6)
PIECE_KING, PIECE_QUEEN, PIECE_BISHOP = range(3)
COLOUR_WHITE, COLOUR_BLACK = range(2)

class Piece:
    "contains defult attrabutes and functions that every piece has"
    def __init__(self, piece, colour, pos, value, icons, id):
        self.piece, self.colour, self.id = piece, colour, id
        self.img_pos = [self.colour, self.piece]
        self.icon = icons[self.colour]
        self.row, self.column = pos
        self.possible_moves = []
        self.value = value
    
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
        "returns a list of squares in the given direction until a piece is found"
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
    
    def set_possible_moves(self, board):
        self.possible_moves = []
        self.find_possible_moves(board)
        possible_moves = []
        for move in self.possible_moves:
            moving_piece = board[move[0]][move[1]]
            if (
                (moving_piece is not None) and (moving_piece.colour != self.colour)
            ) or (moving_piece is None):
                possible_moves.append(move)
        self.possible_moves = possible_moves

    def find_moves(self, board, path_to_king):
        self.set_possible_moves(board)
        if len(path_to_king) > 0:  # if we are in check
            if self.piece == "King":  # king can move out of check

                self.possible_moves = [
                    move for move in self.possible_moves if move not in path_to_king
                ]
            else:  # king can not block itelf from check
                # remove piece in possible moves that is not your colour
                self.possible_moves = list(set(self.possible_moves) & set(path_to_king))
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

    def pos(self):
        # (row, column) tuple
        return (self.row, self.column)

    def __repr__(self):
        # string representation
        #return f"{self.__class__} : {vars(self)}"
        pos = (self.row, self.column)
        return f"{self.colour}, {pos}, " + \
            f"{self.icon}, value={self.value},  possible_move[{len(self.possible_moves)}] = " + \
            f"{self.possible_moves}"

class Pawn(Piece):
    "subclass of Piece with pawn specific attributes"
    def __init__(self, colour, pos, id):
        super().__init__(PIECE_PAWN, colour, pos, 1, ["♙", "♟"], id)
        self.direction = 1 if self.colour == COLOUR_WHITE else -1
        self.first_move = self.check_first_move()

    def check_first_move(self):
        "check if pawn is on its starting row so is on its first move"
        if ((self.row == 1) and (self.colour == COLOUR_WHITE)) or (
            (self.row == 6) and (self.colour == COLOUR_BLACK)):
            return True
        return False

    def find_possible_moves(self, board, pieces_to_jump=0):
        "generate all the possible moves for the pawn"
        dest_row = self.row + self.direction
        dest_row_first = dest_row + self.direction  # first move can move two rows
        if not (dest_row >= 0 and (dest_row <= 7)):
            # pawn cannot go further
            # TODO: pawn promotion when it reaches other base line
            return

        if board[dest_row][self.column] is None:
            self.possible_moves.append(((dest_row), self.column))
            if self.first_move:
                if board[dest_row_first][self.column] is None:
                    self.possible_moves.append((dest_row_first, self.column))
                    self.first_move = False
        if self.column > 1:
            dest_square = board[dest_row][self.column - 1]
            if (dest_square is not None) and (dest_square.colour != self.colour):
                # take left
                self.possible_moves.append(
                    ((dest_row), (self.column - 1))
                )
        if self.column < 7:
            dest_square = board[dest_row][self.column + 1]
            if (dest_square is not None) and (dest_square.colour != self.colour):
                # take right
                self.possible_moves.append(
                    ((dest_row), (self.column + 1))
                )


class Rook(Piece):
    "subclass of Piece with a rooks attributes"
    def __init__(self, colour, pos, id):
        super().__init__(PIECE_ROOK, colour, pos, 4, ["♖", "♜"], id)

    def find_possible_moves(self, board, pieces_to_jump=0):
        "find all possible moves for rook"
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


class Bishop(Piece):
    "subclass of Piece with bishop specific attributes"
    def __init__(self, colour, pos, id):
        super().__init__(PIECE_BISHOP, colour, pos, 3, ["♗", "♝"], id)

    def find_possible_moves(self, board, pieces_to_jump=0):
        "Generate all possible moves for a bishop"
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


class King(Piece):
    "Subclass of Piece with king attributes"
    def __init__(self, colour, pos, id):
        super().__init__(PIECE_KING, colour, pos, 10, ["♔", "♚"], id)
        self.check_moves = []

    def find_possible_moves(self, board, pieces_to_jump=0):
        "Generate all possible moves for a king"
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


class Queen(Piece):
    "Sub class of game object with queen attributes"
    def __init__(self, colour, pos, id):
        super().__init__(PIECE_QUEEN, colour, pos, 9, ["♕", "♛"], id)

    def find_possible_moves(self, board, pieces_to_jump=0):
        "The queen's possible moves is a combination of the rook and bishop"
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


class Knight(Piece):
    "subclass of Piece with knight attributes"
    def __init__(self, colour, pos, id):
        super().__init__(PIECE_KNIGHT, colour, pos, 5, ["♘", "♞"], id)

    def find_possible_moves(self, board, pieces_to_jump=0):
        "finds all possible moves for the knight"
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