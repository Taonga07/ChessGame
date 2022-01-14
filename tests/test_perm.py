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

#lookahead not working yet so skip test
def skip_test1(game=Headless_ChessGame(), testname="test1", max_index=100):
    index=0
    res = DRAW
    (abbrv, from_pos, to_pos, taken) = "", None, None, "."
    
    while True:
        colour = game.get_turn_colour()
        # white is all permuations including lookahead, black is all without lookahead 
        perm = RandomMove.perm_all if colour == 'white' else RandomMove.perm_notlook 
        start_time = time.perf_counter()
        try:
            abbrv, from_pos, to_pos, taken = random_auto_move(game, perm)
        except ChessExc as exc:
            print(f"{testname} {colour} {index} {exc}, {exc.err} ")
            res = WHITE_WIN if colour == 'black' else BLACK_WIN

        if res == DRAW:
            print(f"\t{testname} move number {index} {colour} duration={time.perf_counter()-start_time:0.2f}, " +
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
    for index in range(1):
        res.append(skip_test1(Headless_ChessGame()))
    print(f"res[{len(res)}] = {res}, sum = {sum([elem[0] for elem in res])}, " +
        f"average moves={sum([elem[1] for elem in res])/(index+1):0.1f}")

