
from os.path import join, dirname
import sys
from ChessGame import *

perm_lookahead = (1 << RandomMove.PERM_LOOKAHEAD_BIT)
perm_notlook = -1 & ~(1 << RandomMove.PERM_LOOKAHEAD_BIT)
perm_all = -1
WHITE_WIN = 1
BLACK_WIN = -1
DRAW = 0

def test7(game=Headless_ChessGame(), testname="test7"):
    index=0
    res = DRAW
    while True:
        colour = game.get_turn_colour()
        perm = perm_all if colour == 'white' else perm_notlook # white take, dodge; black is random
        try:
            abbrv, from_pos, to_pos, taken = random_auto_move(game, perm)
        except ChessExc as exc:
            print(f"{testname} {colour} {index} {exc}, {exc.err} ")
            res = WHITE_WIN if colour == 'black' else BLACK_WIN
            break

        False and print(f"\t{testname} move number {index} {colour}, " +
            f"{abbrv}{from_pos}:{to_pos}{'' if taken == '.' else ' takes ' + taken}") 

        if taken.lower() == 'k':
            print(f"{testname} checkmate move {index}  {colour} takes {taken}")
            res = BLACK_WIN if colour == 'black' else WHITE_WIN
            break

        if index > 100:
            res = DRAW
            break
        index = index+1
    
    return (res, index, game.nturn)

if __name__ == "__main__":
    # invoked by python and not pytest
    res = []
    for index in range(1):
        res.append(test7(Headless_ChessGame()))
    print(f"res[{len(res)}] = {res}, sum = {sum([elem[0] for elem in res])}, " +
        f"average moves={sum([elem[2] for elem in res])/(index+1)}")

