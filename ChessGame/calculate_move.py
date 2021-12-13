import random, copy, inspect, logging
from tkinter import Toplevel
from collections import defaultdict
from API import CheckMateExc

logger = logging
if True:
    # import logger in other modules to share same log config
    logger.basicConfig(filename='chess_game.log', filemode='w', \
        level = logging.DEBUG, format= "%(message)s")

def log(mess, indent=0):
    # prefix start with indent number of tabs, right justify caller name 
    caller = inspect.stack()[1][3]  # name of caller function
    logger.debug(("\t"*indent) + f"{caller:>16}: {mess}")

class RandomMove():
    PERM_TAKE_BIT = 0 # take()
    PERM_DODGE_BIT = 1 # dodge()

    class CheckMate(Exception):
        pass

    def __init__(self, game, perm=-1, nest_level=1):
        self.game = game
        self.permutations = perm # bit msk of functions to run before random_move()
        self.nest_level = nest_level # debug nesting level, useful when try_move()

        log('#'*16, indent=self.nest_level)
        log(f"RandomMove: {game.get_turn_colour()} perm={self.permutations}, level={self.nest_level}", indent=self.nest_level)

        # abstract name this colour variables white, but may actually be black move
        # this colours moves
        self.white_moves, self.white_takes, self.white_king, self.total_value = self.get_moves()
        self.white_checkmate = True if self.white_king == None else False
   
        game.toggle_turn() # swap turn
        self.black_moves, self.black_takes, self.black_king, self.total_value = self.get_moves()   # other colours moves
        self.black_checkmate = True if self.black_king == None else False
        game.toggle_turn() # swap back

        # (to, from) move that can take
        self.white_take_moves, self.white_take_target = self.take_moves_targets(self.white_takes)
        self.black_take_moves, self.black_take_target = self.take_moves_targets(self.black_takes)

        self.white_check = True if not self.white_checkmate and (self.white_king in self.black_take_target) else False
        self.black_check = True if not self.black_checkmate and (self.black_king in self.white_take_target) else False

        self.white_dests = set([ v for k in self.white_moves.keys() for v in self.white_moves[k][1] ])
        self.black_dests = set([ v for k in self.black_moves.keys() for v in self.black_moves[k][1] ])
        self.shared_dest = self.white_dests & self.black_dests # intersect
        # white move that can be followed by black take
        # TODO: Pawn diagonal take so not part of intersect
        self.white_moves_black_take = {(k, v): (self.white_moves[k][0][0], self.white_moves[k][0][1]) \
                    for k in self.white_moves.keys() for v in self.white_moves[k][1] if v in self.shared_dest}

    def take_moves_targets(self, takes):
        take_moves = {(_pos, _pm):(_a_v, _taken, _val) \
                    for (_pos, _pm, _a_v, _taken, _val) in takes}
        take_targets = defaultdict(list)
        for k in take_moves.keys():
            (_pos, _pm) = k 
            take_targets[_pm].append((_pos, *take_moves[k]))
        return take_moves, take_targets

    def get_moves(self):
        all_moves = {}  # this colours moves
        take_moves = [] # pieces this colour can take
        king_pos = None # king location
        total_value = 0 
        game = self.game

        for row_number in range(0, 8):
            for column_number in range(0, 8):
                # visit all pieces, my colour and other colour
                pos = (row_number, column_number) # from
                piece = game.get_piece(*pos)
                if piece != None and game.test_turn(piece.colour):
                    game.select_piece_to_move(pos) # update possible moves
                    a_v = (piece.abbrv, piece.value)
                    if a_v[0][0].lower() == 'k':
                        king_pos = pos
                    total_value =+ a_v[1]
                    if len(piece.possible_moves) == 0:
                        continue
                    all_moves[pos] = (a_v, tuple(piece.possible_moves))
                    for pm in piece.possible_moves:
                        # iterate to moves and record what can be taken
                        op = game.get_piece(*pm) # destination
                        if op != None:
                            take_moves.append((pos, pm, a_v, op.abbrv, op.value))

        take_moves.sort(key=lambda x: x[4], reverse=True) # sort on value
        log(f"{game.get_turn_colour()} " + 
            f"all_moves[{len(all_moves)}] take_moves[{len(take_moves)}]={take_moves} " +
                f"king_pos={king_pos}, total_value={total_value}", indent=self.nest_level)
        return all_moves, take_moves, king_pos, total_value

    def take(self, val=-1):
        # PERM_TAKE, best value take greater than val
        move = None
        taken = '.'
        val = -1
        for _take in self.white_takes:
            # first in list has (joint) highest value
            (pos, pm, a_v, taken, _val) = _take
            if _val < val:
                break
            _move = (pos, pm)
            if _move in self.white_moves_black_take:
                log(f"skipped _move={_move} in white_moves_black_take[{len(self.white_moves_black_take)}]={self.white_moves_black_take}", \
                    indent=self.nest_level )
            else:
                move = (pos, pm, a_v[0])
                val = _val
                break
        log(f"move={move}, taken={taken}, val={val}", indent=self.nest_level)
        return move, taken, val
    
    def dodge_list(self, val):
        # Check if I can be taken, have a value greater than val and 
        # there is a move that can be made
        froms = []
        for dp in self.black_takes:
            (pos, to, a_v, taken, defend_val) = dp # pos,to is the from,to of other colour
            if defend_val <= val: 
                # stop looking as attack better than defence
                break
            if to in self.white_moves:
                froms.append((to, defend_val))
        froms.sort(key=lambda x: x[1], reverse=True) # sort on value
        log(f"froms={froms}", indent=self.nest_level+1)
        return froms
    
    def dodge(self, val):
        # PERM_DODGE, move piece value greater than val that can be taken 
        froms = self.dodge_list(val) # sorted pieces greater than val in jeopardy
        move, taken, val = None, '.', -1
        if len(froms) == 0:
            return move, taken, val

        dodges = [] # escape moves that could be made
        takers = [] # escape moves that can take
        black_dests = self.black_dests
        white_take_moves = self.white_take_moves

        for (pos, _pval) in froms:
            for dest in self.white_moves[pos][1]:
                # loop through all possible (pos, dest) moves
                if dest in black_dests:
                    # takeable so keep looking
                    continue
                a_v = self.white_moves[pos][0]
                _move = (pos, dest, a_v[0])
                if (pos, dest) in white_take_moves:
                    # this move is a taker
                    (_a_v, _taken, _val) = white_take_moves[(pos, dest)]
                    takers.append((_move, _taken, _val)) # value of piece taken
                dodges.append((_move, a_v[1])) # value of piece moving

        takers.sort(key=lambda x: x[2], reverse=True) # sort on value
        if len(takers):
            (move, taken, val) = takers[0] # best value take move
            log(f"takers move={move}, taken={taken}, val={val}, takers[{len(takers)}]={takers}", indent=self.nest_level)
        if len(dodges):
            log(f"dodges[{len(dodges)}]={dodges}", indent=self.nest_level)
            _val = dodges[0][1] # dodges sorted on from value
            if _val >= val:
                # this piece value as good as any dodge take
                move, taken, val = dodges[0][0], '.', _val
                log(f"dodges move={move}, taken={taken}, val={val}", indent=self.nest_level+1)

        return move, taken, val

    def random_move(self):
        # any move
        move = None
        all_moves = []
        white_moves = self.white_moves
        if len(list(white_moves.keys())) > 0:
            all_moves = [(k,v, white_moves[k][0][0]) \
                            for k in list(white_moves.keys()) \
                                for v in white_moves[k][1]]
            move = random.choice(all_moves)
        log(f"move={move}", indent=self.nest_level)
        return move
    
    def get_move(self, perm=-1):
        from_pos, to_pos, taken = (None, None), (None, None), '.'
        move, taken, val = None, '.', -1
        if perm == -1:
            perm = self.permutations
        
        if perm & (1 << RandomMove.PERM_TAKE_BIT):
             res = self.take(val)
             if res[0] != None:
                (move, taken, val) = res
        
        if move == None:
            move = self.random_move()

        if perm & (1 << RandomMove.PERM_DODGE_BIT):
            res = self.dodge(val)
            if res[0] != None:
                (move, taken, val) = res
        
        log(f"move={move}, taken={taken}, val={val}", indent=self.nest_level)
        return move, taken, val

    def check(self):
        # Try all moves and return one that changes check state
        # TODO: rework to find move to put other into check
        move = None
        not_check = []
        
        if self.white_king in self.white_moves:
            for _move in [(pos, pm) for pos in self.white_moves \
                                        for pm in self.white_moves[pos][1]]:
                rm = self.try_move(_move)
                if rm.check != self.check:
                    # Found a move to get out of check
                    # Insert king move at start of list, else append
                    not_check.insert(0 if _move[0] == self.white_king else len(not_check), _move)
        
        if len(not_check):
            move = not_check[0]

        log( f"move={move}, not_check[{len(not_check)}]={not_check}", indent=self.nest_level)
        return move

    def try_move(self, move):
        dupl_game = copy.deepcopy(self.game)
        dupl_game.move(*move)
        rm = RandomMove(dupl_game, self.permutations, nest_level=2)
        return rm

def random_auto_move(game, perm=-1):
    # Return move to make, in: Headless_ChessGame(), out: from, to, taken or '.'
    from_pos, to_pos, taken = (None, None), (None, None), '.'
    colour = game.get_turn_colour()
    rm = RandomMove(game, perm)
    checkmate = rm.white_checkmate    # king previously taken
    if rm.white_check:
        # In check so look for move to get out of check
        move = rm.check()
        if move != None:
            if move in rm.white_take_moves:
                (_a_v, taken, _val) = rm.white_take_moves[move]
            log(f"escape check move={move}, taken={taken}", indent=rm.nest_level)
            return move[0], move[1], taken
        checkmate = True
    if checkmate:
        raise CheckMateExc

    move, taken, val = rm.get_move(perm)
    if move:
        from_pos, to_pos = move[0], move[1]
        moved = f"{move[2]}{from_pos}:{to_pos}"

        (ncommands, errs) = game.commands(moved)    # will toggle_turn
        log(f"command={moved}, from_pos={from_pos}, to_pos={to_pos}, taken={taken}, ncommands={ncommands}, errs={errs}, {game.dump(True)}")
        if len(errs) > 0:
            from_pos, to_pos, taken = (None, None), (None, None), '.'

    if taken.lower() == 'k':
        print(f"Checkmate {colour} takes {taken}")

    return from_pos, to_pos, taken   # moves and taken piece