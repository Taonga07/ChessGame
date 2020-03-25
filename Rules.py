import Chess

class GameObject():
    def __init__(self, piece, icon, colour, column, row):
        self.icon = icon
        self.colour = colour
        self.piece = piece
        self.row = row
        self.column = column
        self.score = score
        
class Pawn(GameObject):
    def __init__(self, piece, icon, colour, column, row):
        super().__init__(piece, icon, colour, column, row)
        self.piece = 'Pawn'

    def check_move(self, new_row_number,new_column_number):
        return True
