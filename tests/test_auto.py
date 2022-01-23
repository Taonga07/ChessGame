from ChessGame import Headless_ChessGame, ChessErrs, ChessExc, CheckMateExc, RandomMove, random_auto_move

'''
coverage run test_auto.py
coverage html && firefox htmlcov/index.html

coverage run  -m pytest test_auto.py

python -m cProfile  -o fart.cprof test_auto.py
pyprof2calltree -k -i fart.cprof
'''

'''
class RandomMove():
    PERM_SEMI_RANDOM_BIT = 0  # semi-random, avoid king moves and moving into kill zone
    PERM_TAKE_BIT = 1 # take()
    PERM_DODGE_BIT = 2 # dodge()
    PERM_LOOKAHEAD_BIT = 3 # lookahead()
'''

def test1(game=Headless_ChessGame(file=None)):
    setup1_white = "Qc1; Ke1; Pd2; Pe2"
    setup1_black = "ke8; pd7; qa3; pe3"

    command = f"{setup1_white}; {setup1_black}"
    (ncommands, errs) = game.commands(command)
    print(f"test1 dump: command={command}, ncommands={ncommands}, errs={errs}, {game.dump(unicode=True)}")

    if True:
        colour = game.get_turn_colour()
        perm = (1 << RandomMove.PERM_TAKE_BIT) # test take()
        rm = RandomMove(game, perm)
        move, taken = rm.get_move(perm)
        print(f"test1 {colour} {game.nturn} {hex(perm)} : {move} {taken}")
        assert move == ('c1', 'a3', 'Q') and taken == "q"

    if True:
        colour = game.get_turn_colour()
        perm = (1 << RandomMove.PERM_DODGE_BIT) # test dodge()
        rm = RandomMove(game, perm)
        move, taken = rm.get_move(perm)
        print(f"test1 {colour} {game.nturn} {hex(perm)} : {move} {taken}")
        assert move == ('c1', 'a3', 'Q') and taken == "q"
    
    if True:
        for perm in (0, (1 << RandomMove.PERM_SEMI_RANDOM_BIT)):
            colour = game.get_turn_colour()
            rm = RandomMove(game, perm)
            move, taken = rm.get_move(perm)
            print(f"test1 {colour} {game.nturn} {hex(perm)} : {move} {taken}")

def test2(game=Headless_ChessGame(file=None), perm=RandomMove.perm_notlook, testname='test2'):
    # Anastasia’s Mate
    setup_white = "Kg1; Re3; Ne7"
    setup_black = "kh7; pg7; be8"
    white_attack = 'Re3:h3'

    command = f"{setup_white}; {setup_black}; {white_attack}"
    (ncommands, errs) = game.commands(command)
    print(f"{testname} dump: command={command}, ncommands={ncommands}, errs={errs}, {game.dump(unicode=True)}")
    assert ncommands == 7 and len(errs) == 0, f"unexpected commands error in {command}"

    # sacrifice black bishop to escape check
    colour = game.get_turn_colour()
    rm = RandomMove(game, perm)
    # first test get_move
    move, taken = rm.get_move(perm)
    print(f"{testname} get_move {colour} {game.nturn} {hex(perm)} : {move} {taken}")
    assert move == ('e8', 'h5', 'b') and taken == "."

    # second test auto_move which uses get_move() to make the move
    _move = random_auto_move(game, perm) # black
    assert _move != None, f"unexpected no move"
    (abbrv, from_pos, to_pos, taken) = _move

    move = (from_pos, to_pos, abbrv)
    print(f"{testname} auto_move {colour} {game.nturn} {hex(perm)} : {move} {taken} {game.dump(unicode=True)}")
    assert move == ('e8', 'h5', 'b') and taken == "."

    # white
    _move = random_auto_move(game, perm) # white
    assert _move != None, f"unexpected no move"
    (abbrv, from_pos, to_pos, taken) = _move

    move = (from_pos, to_pos, abbrv)
    print(f"{testname} auto_move {game.nturn} {hex(perm)} : {move} {taken} {game.dump(unicode=True)}")
    assert move == ('h3', 'h5', 'R') and taken == "b"

    # black check mate 
    _move = random_auto_move(game, perm) # black
    assert _move == None, f"Expected CheckMate"

def test3(perm=-1, testname='test3'):
    test2(game=Headless_ChessGame(file=None), perm=perm, testname=testname)

def test4(game=Headless_ChessGame(file=None), perm=RandomMove.perm_notlook, testname='test4'):
    setup_white = "Kc1; Qa7"
    setup_black = "bc8; kd8"
    white_attack = 'Qa7:a8'

    command = f"{setup_white}; {setup_black}; {white_attack}"
    (ncommands, errs) = game.commands(command)
    print(f"{testname} dump: command={command}, ncommands={ncommands}, errs={errs}, {game.dump(unicode=True)}")
    assert ncommands == 5 and len(errs) == 0, f"unexpected commands error in {command}"

     # second test auto_move which uses get_move() to make the move
    move = random_auto_move(game, perm) # black
    assert move != None, f"unexpected no move"
    (abbrv, from_pos, to_pos, taken) = move
    print(f"{testname} auto_move {game.nturn} {hex(perm)} : {move} {taken} {game.dump(unicode=True)}")

    if perm == RandomMove.perm_notlook:
        # crude logic moves bishop as does not realise exposing king
        assert abbrv == 'b', f"{perm} Expected 'b' to have been moved, but got {abbrv}"
    else:
        # lookahead will move king as better
        assert abbrv == 'k', f"{perm} Expected 'k' to have been moved, but got {abbrv}"

def test5(perm=RandomMove.perm_all, testname='test5'):
    # use lookahead so move king and not bishop
    test4(game=Headless_ChessGame(file=None), perm=perm, testname=testname)

if __name__ == "__main__":
    # invoked by python and not pytest
    test1()
    test2()
    test3()
    test4()
    test5()
    pass