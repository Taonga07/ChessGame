import unittest

import Rules

#
# VSCode info: https://code.visualstudio.com/docs/python/testing
# 
# TestStringMethods sample tests are taken from: https://docs.python.org/3/library/unittest.html
#

class TestStringMethods(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    # Called automatically before each test
    def setUp(self):
        # Setup the empty board
        self.board = []
        for row in range(0, 8):
            self.board.append([None,None,None,None,None,None,None,None])

    # This avoids any confusion with row, column ordering - the 'piece' constructor accepts column, row but the board uses row, column
    # This routine avoids that by always using row, column
    def placePiece(self, row, column, piece):
        piece.row = row
        piece.column = column
        self.board[piece.row][piece.column] = piece
        return piece

    def test_pawn_1(self):
        # place a pawn on the empty board at ROW, COL
        pawn = self.placePiece( 6, 0, Rules.Pawn('Pawn', Rules.path+'White_Pawn.gif', 'white', None, None))

        # Run the test
        pawn.find_moves(self.board)
        # Check the results
        self.assertEqual(pawn.possible_moves, [ (5,0), (4,0) ])

        # Check when it's NOT our pawn's first move
        pawn.first_move = False
        # Run the test
        pawn.find_moves(self.board)
        # Check the results
        self.assertEqual(pawn.possible_moves, [ (5,0) ])

    def test_rook_1(self):
        # place a rook on the empty board at ROW, COL
        rook = self.placePiece( 0, 0, Rules.Rook('Rook', Rules.path+'White_Rook.gif', 'white', None, None))

        # Run the test
        rook.find_moves(self.board)
        
        # Check the results
        self.assertEqual(rook.possible_moves, [ (0,0), (0,1) ])


if __name__ == '__main__':
    unittest.main()