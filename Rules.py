import os


class GameObject():
    def __init__(self, piece, icon, colour, column, row, score):
        self.icon = icon
        self.colour = colour
        self.piece = piece
        self.row = row
        self.column = column
        self.score = score
        
class Pawn(GameObject):
    def __init__(self, piece, icon, colour, column, row, score):
        super().__init__(piece, icon, colour, column, row, score)
        self.piece = 'Pawn'

    def check_move(self, new_row_number,new_column_number):
        return True

# our varibles/lits

path = os.getcwd() + '/Chess_Resources/'