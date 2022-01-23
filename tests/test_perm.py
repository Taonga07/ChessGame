'''
Run a game with black and white using different permutations. Run many 
times to decide which is best strategy overall.
'''
from os.path import join, dirname
import sys, time
from ChessGame import *
WHITE_WIN = 1
BLACK_WIN = -1
DRAW = 0

#lookahead takes ages so reduce max_index if pytest
def test1(game=Headless_ChessGame(), testname="test1", max_index=5):
    index=0
    res = DRAW
    (abbrv, from_pos, to_pos, taken) = "", None, None, "."
    
    while True:
        colour = game.get_turn_colour()
        # white is all permuations including lookahead, black is all without lookahead 
        perm = RandomMove.perm_all if colour == 'white' else RandomMove.perm_notlook 
        start_time = time.perf_counter()
        _move = random_auto_move(game, perm)
        if _move == None: 
            print(f"{testname} {index} {colour} loses")
            res = WHITE_WIN if colour == 'black' else BLACK_WIN
        else:
            abbrv, from_pos, to_pos, taken = _move

        if res == DRAW:
            print(f"\t{testname} move number {index} {colour} duration={time.perf_counter()-start_time:0.3f}, " +
                f"{abbrv}{from_pos}:{to_pos}{'' if taken == '.' else ' takes ' + taken}") 

            if taken.lower() == 'k':
                print(f"{testname} checkmate move {index}  {colour} takes {taken}")
                res = BLACK_WIN if colour == 'black' else WHITE_WIN
        print(game.dump(unicode=True))

        if index > max_index or (res != DRAW):
            break
        index = index+1
    
    assert index > 3
    return (res, game.nturn)

if __name__ == "__main__":
    # invoked by python and not pytest
    res = []
    index = 0
    for index in range(1):
        res.append(test1(Headless_ChessGame(), max_index=100))
    print(f"res[{len(res)}] = {res}, sum = {sum([elem[0] for elem in res])}, " +
        f"average moves={sum([elem[1] for elem in res])/(index+1):0.1f}")

