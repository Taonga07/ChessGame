
import CP

#
# A list of example scenarios that the developer can use for testing
# This file should have no tkinter code inside it - it should only deal with the board and pieces
#

def add_piece(board, piece):
    board[piece.row][piece.column] = piece

# This will probably be useful for a number of scenarios
def setup_kings_in_corners(board):
    add_piece(board, CP.King('White', 0, 0))
    add_piece(board, CP.King('Black', 7, 7))

# A sample test scenario
def setup_board_for_example_scenario_1(board):
    setup_kings_in_corners(board)
    add_piece(board, CP.Pawn('White', 2, 2))
    add_piece(board, CP.Pawn('Black', 3, 5))

def setup_board_for_example_scenario(board, scenario_num):
    if scenario_num == 1:
        setup_board_for_example_scenario_1(board)
    else:
        raise Exception(f"No example scenario: {scenario_num}")
