"""
Auto python tests using 'pytest' (`pip3 install pytest`)
https://docs.pytest.org/en/6.2.x/goodpractices.html

Tests are in subdir ChessGame/tests so ChessGame/.. directory needs to be on
the PYTHONPATH to access the module i.e. PYTHONPATH=$PWD pytest tests/test_test1.py
Instead, run from top dir via `python -m pytest`

pytest descends subdirs and runs tests that are in file names that 
start "test_" and functions that start with "test":
- To run all tests from topdir:   python3 -m pytest
- To list all avalable tests:     python3 -m pytest --collect-only
- To run a specific test file:    python3 -m pytest -k test_test1
- To run specific test:           python3 -m pytest -k test6_dodgy

Generate report of test coverage (`pip3 install coverage`):
$ PYTHONPATH=$PWD coverage run  -m pytest -k test_test1.py
$ coverage report # basic report
$ coverage html && firefox htmlcov/index.html # html to zoom into source lines
Note: a test objective is to visit all source lines, so use coverage report
to identify tests to add.
"""
# fmt: off
import pytest
from os.path import join, dirname
import sys

sys.path.append(join(dirname(__file__), "ChessGame"))
from ChessGame import *
# fmt: on

"""
Sanity test board layout. Depends on implementation details which is
fragile in a test as any change in code may break it. 
Done first as later tests may depend on assumptions of layout
"""


def test1_layout(game=Headless_ChessGame()):
    # Check default initial board layout
    board = game.board
    assert len(board) == 8 and len(board[0]) == 8
    assert game.turn == 0  # White

    for r in board[2:5]:
        assert r == [None] * 8

    for sq in board[1] + board[6]:
        assert isinstance(sq, Pawn)

    for r in (0, 7):
        colour = "Black" if r == 0 else "White"

        for sq in list(board[r][c] for c in (0, 7)):
            assert isinstance(sq, Rook)
            assert sq.colour == colour

        for sq in list(board[r][c] for c in (1, 6)):
            assert isinstance(sq, Knight)

        for sq in list(board[r][c] for c in (2, 5)):
            assert isinstance(sq, Bishop)

        assert isinstance(board[r][3], Queen)
        assert isinstance(board[r][4], King)

        print(f"test1 dump: {game.dump(unicode=True)}")
        return game


def test2_moveto(game=Headless_ChessGame()):
    # First movefrom/moveto white pawn
    from_pos = (6, 3)  # row: 6, col: 3 which is initial White Pawn
    from_square = game.get_piece(*from_pos)
    print(f"from_square[{from_pos}]: {from_square}")

    assert from_square.row == from_pos[0] and from_square.column == from_pos[1]
    assert from_square.piece == "Pawn" and from_square.colour == "White"

    game.click = 0
    try:
        from_piece = game.movefrom(*from_pos)
    except ChessExc as exc:
        assert False, f"valid movefrom {from_pos} raised an exception {exc}"
    assert from_piece == from_square

    # initial white Pawns can move 1 or 2 squares vertical up
    moves = from_piece.possible_moves

    assert (
        len(moves) == 2
        and moves[0] == (from_pos[0] - 1, from_pos[1])
        and moves[1] == (from_pos[0] - 2, from_pos[1])
    )

    to_pos = moves[0]  # first possible move
    to_piece = game.get_piece(*to_pos)
    print(f"to piece at {to_pos}: {to_piece}")
    assert to_piece == None

    try:
        to_square = game.moveto(*to_pos)
    except ChessExc as exc:
        assert False, f"valid moveto {to_pos} raised an exception {exc}"

    print(f"to_square[{to_pos}]: {to_square}")
    assert game.get_piece(*from_pos) == None  # check from cleared

    print(f"test2 dump: {game.dump(unicode=True)}")

    ########################
    # test3_move(): 2nd move black pawn
    from_pos = (1, 4)  # black pawn
    to_pos = (3, 4)
    from_piece = game.get_piece(*from_pos)

    try:
        to_piece = game.move(from_pos, to_pos)
    except ChessExc as exc:
        assert False, f"valid move({from_pos}, {to_pos}) raised an exception {exc}"

    print(f"to_pos[{to_pos}]: {to_piece}")
    assert to_piece == from_piece
    assert len(to_piece.history) == 1 and to_piece.history[0] == (from_pos, to_pos)

    print(f"test3 dump: {game.dump(unicode=True)}")
    return game


def test4_invfrom(game=Headless_ChessGame()):
    # first move move white
    raised_exc = None

    # Invalid from
    for from_pos_exc in (
        ((0, 0), InvColourExc),
        ((3, 7), InvMoveExc),
    ):  # (black rook, none)
        from_pos = from_pos_exc[0]
        exp = from_pos_exc[1]
        try:
            from_piece = game.movefrom(*from_pos)
        except ChessExc as exc:
            raised_exc = exc
            print(f"test4 Expected invalid movefrom {from_pos} : {exc}, {exc.err} ")
        assert isinstance(raised_exc, exp)

    # Invalid to
    from_pos = (6, 3)  # valid white pawn
    try:
        from_piece = game.movefrom(*from_pos)
    except:
        assert False, "valid move but error thrown"

    # (three up vert, one back vert, black rook, none)
    for to_pos in ((3, 3), (7, 3), (0, 0), (3, 7)):
        try:
            to_piece = game.moveto(*to_pos)
        except ChessExc as exc:
            raised_exc = exc
            if isinstance(raised_exc, InvMoveExc):
                print(f"test4 Expected invalid moveto {to_pos} : {exc}")
        assert isinstance(raised_exc, InvMoveExc)

    return game


def test5_commands():
    # init game and pieces
    game = Headless_ChessGame(None)  # no input file

    (ncommands, errs) = game.commands("nonsense; Xa1; Pa9; p(8,8); !; Ki1")
    print(f"test5 nonsense {ncommands}: {errs}")
    assert ncommands == 6 and len(errs) == ncommands

    # init start, white king in check, dump
    (ncommands, errs) = game.commands("Ke1; Qc3; ra1; d")
    print(f"test5 init {ncommands}: {errs}")
    assert ncommands == 4 and errs == []

    # errors: invalid move as white move, no Q at h1, piece already (7,0), invalid to
    (ncommands, errs) = game.commands("ra1:a2; Qh1:h2; P(7,0); Ke1:e3")
    print(f"test5 inv {ncommands}: {errs}")
    assert ncommands == 4 and len(errs) == 4

    return game


def test6_check():

    game = Headless_ChessGame(None)  # no pieces

    # white king in check
    (ncommands, errs) = game.commands("ke8; Ke2; Ba3; Qc3; ra2")
    print(f"test6 init {ncommands}: {errs}, {game.dump(unicode=True)}")
    # game.save_file('test6.txt')
    assert errs == []

    ######################

    # invalid move as white in check
    (ncommands, errs) = game.commands("Qc3:b3")
    print(f"test6 Queen {ncommands}: {errs}")
    assert ncommands == 1 and len(errs) == 1 and errs[0][1] == ChessErrs.ErrInvMove

    """
    I was surprised that 'check' state is not reported.
    Instead 'Invalid move' is reported and possible_moves lists only those that 
    that stop check
    """
    piece = game.get_piece(5, 2)  # Qc3
    expected_moves = [(6, 1), (6, 2), (6, 3)]
    assert (
        piece.abbrv == "Q"
        and len(piece.possible_moves) == len(expected_moves)
        and set(piece.possible_moves) == set(expected_moves)
    )

    #######################

    # invalid move as white in check
    (ncommands, errs) = game.commands("Ba3:b4")
    print(f"test6 Bishop {ncommands}: {errs}")
    assert ncommands == 1 and len(errs) == 1 and errs[0][1] == ChessErrs.ErrInvMove

    # invalid move as white in check
    (ncommands, errs) = game.commands("Ke2:d2")
    print(f"test6 King {ncommands}: {errs}")
    assert ncommands == 1 and len(errs) == 1 and errs[0][1] == ChessErrs.ErrInvMove

    return game


@pytest.mark.xfail
def test7_mate(game=Headless_ChessGame()):
    command = "Pe2:e4; pf7:f5; Pe4:f5; pg7:g5; Qd1:h5"
    (ncommands, errs) = game.commands(command)
    print(
        f"test7 dump: command={command}, ncommands={ncommands}, errs={errs}, {game.dump(unicode=True)}"
    )
    #game.save_file("test7.txt")

    ntok = len(command.split(";"))
    assert (
        ncommands == ntok
        and len(errs) == 1
        and errs[0][0] == ntok - 1
        and errs[0][1] == ChessErrs.ErrCheckMate
    ), f"Expected CheckMate"


def test8_check2(game=Headless_ChessGame()):
    command = "Pe2:e4; pd7:d5; Bf1:b5; ph7:h5"
    (ncommands, errs) = game.commands(command)
    print(
        f"test8 dump: command={command}, ncommands={ncommands}, errs={errs}, {game.dump(unicode=True)}"
    )
    #game.save_file("test8.txt")

    ntok = len(command.split(";"))
    assert (
        ncommands == ntok
        and len(errs) == 1
        and errs[0][0] == ntok - 1
        and errs[0][1] == ChessErrs.ErrCheck
    )


if __name__ == "__main__":
    # invoked by python and not pytest
    if True:
        test1_layout()
        game = test2_moveto()
        # test3_move(game)   # pytest does not preserve return values
        test4_invfrom()
        test5_commands()
        test6_check()
        test7_mate()
    test8_check2()
    pass
