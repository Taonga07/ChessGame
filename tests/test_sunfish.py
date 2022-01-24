import enum
import pytest
from os.path import join, dirname
import sys

# import cProfile
# python -m cProfile -s cumtime test_sufish.py
#
# python -m cProfile -o fart.cprof test_sunfish.py
# pip3 install  pyprof2calltree
# pyprof2calltree -k -i fart.cprof

#sys.path.append(join(dirname(__file__), "ChessGame"))

from ChessGame import *

def test1(game=Headless_ChessGame()):
    board_layout = game.dump()
    sunfish_layout = board_to_sunfish(board_layout)
    m = SunFishModel(sunfish_layout)
    m.print_pos()

    if sunfish_layout != SunFishModel.initial:
        for i, c in enumerate(SunFishModel.initial):
            d = sunfish_layout[i]
            if d != c:
                print(f"index {i} expected {c} but got {d}")
    assert sunfish_layout == SunFishModel.initial

    for white_move in ("Pa2:a4", "Pd2:d3"):
        (ncommands, errs) = game.commands(white_move)
        print(f"test1 white command={white_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

        move_pos = white_move.split(':')
        move_pos[0] = move_pos[0][1:]
        m.your_move(move_pos)

        m.sunfish_move()
        assert m.status == SunFishModel.MOVE_NONE
        
        black_move = m.moved_piece()
        (ncommands, errs) = game.commands(black_move)
        print(f"test1 black command={black_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

def test2(game=Headless_ChessGame()):
    for white_move in ("Pa2:a4", "Pd2:d3"):
        (ncommands, errs) = game.commands(white_move)
        print(f"test2 white command={white_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

        m = SunFishModel(board_to_sunfish(game.dump()))
        m.print_pos()
        m.sunfish_move()

        assert m.status == SunFishModel.MOVE_NONE

        black_move = m.moved_piece()
        (ncommands, errs) = game.commands(black_move)
        print(f"test2 black command={black_move}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

def test3(layout=SunFishModel.initial, testname="test3", max_index=100):
    m = SunFishModel(layout)
    print(f"{testname} layout")
    m.print_pos()

    index=0
    while True:
        colour = SunFishModel.MOVE_BLACK if index%2 else SunFishModel.MOVE_WHITE

        m.sunfish_move(colour=colour, duration=0.1)
        print(f"\t{testname} move number {index} colour={SunFishModel.COLOUR[colour]} piece={m.moved_piece()}")

        m.print_pos(colour=colour)

        if m.status != SunFishModel.MOVE_NONE:
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

@pytest.mark.xfail
def test6_dodgy(game=Headless_ChessGame(), testname="test6", max_index=5):
    # interface ChessGame
    # TODO: Sunfish generate move black bf8:c8 which ChessGame reports as invalid
    # Output:
    # test6 move number 5 Black command=bf8:c5, ncommands=1, errs=[(0, -3, 'command token index [0]:bf8:c5 move((0, 5), (3, 2)) raised an exception Invalid move')],
    index=0
    while True:
        colour = SunFishModel.MOVE_BLACK if index%2 else SunFishModel.MOVE_WHITE

        m = SunFishModel(board_to_sunfish(game.dump()))  # reset each move
        if colour == SunFishModel.MOVE_BLACK:
            m.pos_list[-1].rotate()

        m.sunfish_move(colour=colour, duration=0.1)
        moved = m.moved_piece()
        print(f"\t{testname} move number {index} colour={SunFishModel.COLOUR[colour]} moved={moved}")
        m.print_pos(colour=colour)

        (ncommands, errs) = game.commands(moved)
        print(f"\t\t{testname} move number {index} {SunFishModel.COLOUR[colour]} command={moved}, ncommands={ncommands}, errs={errs}, {game.dump()}")
        assert ncommands == 1 and len(errs) == 0

        if index > max_index:
            break
        index = index+1

if __name__ == "__main__":
    # invoked by python and not pytest
    if True:
        test1()
        test2()
        test4() # easier to sanity check
        test3()
        test5()
        test6_dodgy()


