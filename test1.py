'''
Auto python tests. 
To run all tests:       pytest test1.py
To list avalable tests: pytest test1.py --collect-only  
To run specific test:   pytest test1.py -k test2_moveto
'''

import pytest
import ChessHeadless
import Pieces

'''
Sanity test board layout. Depends on implementation details which is
fragile in a test as any change in code may break it. 
Done first as later tests may depend on assumptions of layout
'''
def test1_layout(game=ChessHeadless.ChessHeadless()):
    # Check default initial board layout
    board = game.board
    assert len(board) == 8 and len(board[0]) == 8
    assert game.turn == 0  # White

    for r in board[2:5]:
        assert r == [None]*8

    for sq in board[1] + board[6]:
        assert isinstance(sq, Pieces.Pawn) 
    
    for r in (0, 7):
        colour = 'Black' if r == 0 else 'White'

        for sq in [board[r][c] for c in (0, 7)]:
            assert isinstance(sq, Pieces.Rook)
            assert sq.colour == colour
    
        for sq in list(board[r][c] for c in (1, 6)):
            assert isinstance(sq, Pieces.Knight)

        for sq in list(board[r][c] for c in (2, 5)):
            assert isinstance(sq, Pieces.Bishop)
    
        assert isinstance(board[r][3], Pieces.Queen)
        assert isinstance(board[r][4], Pieces.King)

        print(f"test1 dump: {game.dump()}")
        return game

def test2_moveto(game=ChessHeadless.ChessHeadless()):
    #First movefrom/moveto white pawn
    from_pos = (6, 3)   # row: 6, col: 3 which is initial White Pawn
    from_square = game.get_piece(*from_pos)
    print(f"from_square[{from_pos}]: {from_square}")

    assert from_square.row == from_pos[0] and from_square.column == from_pos[1]
    assert from_square.piece == 'Pawn' and from_square.colour == 'White'

    game.click = 0
    try:
        from_piece = game.movefrom(*from_pos)
    except ChessHeadless.ChessExc as exc:
        assert False, f"valid movefrom {from_pos} raised an exception {exc}"
    assert from_piece == from_square 

    # initial white Pawns can move 1 or 2 squares vertical up
    moves = from_piece.possible_moves

    assert len(moves) == 2 and \
        moves[0] == (from_pos[0]-1, from_pos[1]) and \
        moves[1] == (from_pos[0]-2, from_pos[1])

    to_pos = moves[0] # first possible move
    to_piece = game.get_piece(*to_pos)
    print(f"to piece at {to_pos}: {to_piece}")
    assert to_piece == None

    try:
        to_square = game.moveto(*to_pos)
    except ChessHeadless.ChessExc as exc:
        assert False, f"valid moveto {to_pos} raised an exception {exc}"

    print(f"to_square[{to_pos}]: {to_square}")
    assert game.get_piece(*from_pos) == None    ## check from cleared

    print(f"test2 dump: {game.dump()}")

    ########################
    # test3_move(): 2nd move black pawn
    from_pos = (1, 4)   # black pawn
    to_pos = (3, 4)
    from_piece = game.get_piece(*from_pos)

    try:
        to_piece = game.move(from_pos, to_pos)
    except ChessHeadless.ChessExc as exc:
        assert False, f"valid move({from_pos}, {to_pos}) raised an exception {exc}"

    print(f"to_pos[{to_pos}]: {to_piece}")
    assert to_piece == from_piece
    assert len(to_piece.history) == 1 and \
        to_piece.history[0] == (from_pos, to_pos)
    
    print(f"test3 dump: {game.dump()}")
    return game

def test4_invfrom(game=ChessHeadless.ChessHeadless()):
    # first move move white
    raised_exc = None

    # Invalid from 
    for from_pos in ((0, 0), (3,7)):    # (black rook, none)
        try:
            from_piece = game.movefrom(*from_pos)
        except ChessHeadless.ChessExc as exc:
            raised_exc = exc
            if isinstance(raised_exc, ChessHeadless.InvMoveExc):
                print(f'test4 Expected invalid movefrom {from_pos} : {exc}')
        assert isinstance(raised_exc, ChessHeadless.InvMoveExc)

    # Invalid to
    from_pos = (6, 3)   # valid white pawn
    try:
        from_piece = game.movefrom(*from_pos)
    except:
        assert False, 'valid move but error thrown'

    # (three up vert, one back vert, black rook, none)
    for to_pos in ((3, 3), (7, 3), (0, 0), (3,7)):    
        try:
            to_piece = game.moveto(*to_pos)
        except ChessHeadless.ChessExc as exc:
            raised_exc = exc
            if isinstance(raised_exc, ChessHeadless.InvMoveExc):
                print(f'test4 Expected invalid moveto {to_pos} : {exc}')
        assert isinstance(raised_exc, ChessHeadless.InvMoveExc)

    return game

def test5_commands():
    # init game and pieces
    game = ChessHeadless.ChessHeadless(None) # no input file

    (ncommands, errs) = game.commands('nonsense; Xa1; Pa9; p(8,8); !; Ki1')
    print(f"test5 nonsense {ncommands}: {errs}")
    assert ncommands == 6 and len(errs) == ncommands

    (ncommands, errs) = game.commands('Ke1; Qc3; ra1; d') # init start, white king in check, dump
    print(f"test5 init {ncommands}: {errs}")
    assert ncommands == 4 and errs == []

    # errors: invalid move as white move, no Q at h1, piece already (7,0), invalid to
    (ncommands, errs) = game.commands('ra1:a2; Qh1:h2; P(7,0); Ke1:e3')
    print(f"test5 inv {ncommands}: {errs}")
    assert ncommands == 4 and len(errs) == 4

    return game

@pytest.mark.xfail
def test6_check():
    game = ChessHeadless.ChessHeadless(None) # no pieces

    (ncommands, errs) = game.commands('Ke1; Qc3; ra1') # init start, white king in check, dump
    print(f"test6 init {ncommands}: {errs}")
    assert ncommands == 3 and errs == []

    (ncommands, errs) = game.commands('Qc3:b2') # invalid move as white in check
    print(f"test5 check {ncommands}: {errs}")
    assert ncommands == 2 and len(errs) == 1

    (ncommands, errs) = game.commands('Ke1:d2; ra1:a2') # white out of check
    assert ncommands == 2 and errs == []

    print(f"test6 dump: {game.dump()}")
    return game

if __name__== "__main__":
    # invoked by python and not pytest
    test1_layout() 
    game = test2_moveto()
    #test3_move(game)   # pytest does not preserve return values
    test4_invfrom()
    test5_commands()
    test6_check()
    pass



    
