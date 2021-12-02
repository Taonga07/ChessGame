import enum
import pytest
from os.path import join, dirname
import sys

sys.path.append(join(dirname(__file__), "ChessGame"))

from ChessGame import *
from sunfish_interface import Model, board_to_sunfish
import sunfish

def test1(game=Headless_ChessGame()):
    board_layout = game.dump()
    sunfish_layout = board_to_sunfish(board_layout)
    m = Model(sunfish_layout)
    m.print_pos()

    if sunfish_layout != sunfish.initial:
        for i, c in enumerate(sunfish.initial):
            d = sunfish_layout[i]
            if d != c:
                print(f"index {i} expected {c} but got {d}")
    assert sunfish_layout == sunfish.initial

    for white_move in ("Pa2:a4", "Pd2:d3"):
        (ncommands, errs) = game.commands(white_move)
        print(f"test1 white command={white_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

        move_pos = white_move.split(':')
        move_pos[0] = move_pos[0][1:]
        m.your_move(move_pos)

        #m = Model(board_to_sunfish(game.dump()), 0, (True,True), (True,True), 0, 0)
        m.sunfish_move()
        assert m.status == Model.MOVE_NONE
        
        black_move = m.moved_piece()
        (ncommands, errs) = game.commands(black_move)
        print(f"test1 black command={black_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

def test2(game=Headless_ChessGame()):
    for white_move in ("Pa2:a4", "Pd2:d3"):
        (ncommands, errs) = game.commands(white_move)
        print(f"test2 white command={white_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

        m = Model(board_to_sunfish(game.dump()))
        m.print_pos()
        m.sunfish_move()

        assert m.status == Model.MOVE_NONE

        black_move = m.moved_piece()
        (ncommands, errs) = game.commands(black_move)
        print(f"test2 black command={black_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

def test3(layout=sunfish.initial, max_index=100, testname="test3"):
    m = Model(layout)
    print(f"{testname} layout")
    m.print_pos()

    index=0
    while True:
        colour = Model.MOVE_BLACK if index%2 else Model.MOVE_WHITE

        m.sunfish_move(colour=colour, duration=0.1)
        print(f"\t{testname} move number {index} colour={Model.COLOUR[colour]} piece={m.moved_piece()}")

        m.print_pos(colour=colour)

        if m.status != Model.MOVE_NONE:
            break

        if index > max_index:
            break
        index = index+1

def test4():
    # few distinct pieces
    sunfish_layout = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' ....k...\n'  #  20 - 29
    ' n.......\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' .B......\n'  #  80 - 89
    ' ......K.\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
    )
    test3(layout=sunfish_layout, testname="test4")

def test5():
    # black mate
    sunfish_layout = (
    '         \n'  #   0 -  9
    '         \n'  #  10 - 19
    ' ....k...\n'  #  20 - 29
    ' ........\n'  #  30 - 39
    ' ........\n'  #  40 - 49
    ' ........\n'  #  50 - 59
    ' ........\n'  #  60 - 69
    ' ........\n'  #  70 - 79
    ' PPPPPPPP\n'  #  80 - 89
    ' RNBQKBNR\n'  #  90 - 99
    '         \n'  # 100 -109
    '         \n'  # 110 -119
    )
    test3(layout=sunfish_layout, testname="test5")

def test6(game=Headless_ChessGame(), testname="test6"):
    # interface ChessGame
    index=0
    while True:
        colour = Model.MOVE_BLACK if index%2 else Model.MOVE_WHITE

        m = Model(board_to_sunfish(game.dump()))  # reset each move
        if colour == Model.MOVE_BLACK:
            m.pos_list[-1].rotate()

        m.sunfish_move(colour=colour, duration=0.1)
        moved = m.moved_piece()
        print(f"\t{testname} move number {index} colour={Model.COLOUR[colour]} moved={moved}")
        m.print_pos(colour=colour)

        (ncommands, errs) = game.commands(moved)
        print(f"\t\t{testname} move number {index} {Model.COLOUR[colour]} command={moved}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

        if index > 100:
            break
        index = index+1

if __name__ == "__main__":
    # invoked by python and not pytest
    if True:
        #test1()
        #test2()
        #test4() # easier to sanity check
        #test3()
        #test5()
        test6()

