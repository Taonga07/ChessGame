import random, copy, inspect, logging
from ChessGame.API import ChessExc, CheckMateExc, ChessAPI, Position
import threading, time, os

'''
Useful links:
1. https://www.chessprogramming.org/Main_Page
2. https://lichess.org/editor
3. [Coding Adventure: Chess AI](https://youtu.be/U4ogK0MIzqk) **highly recommended**
4. https://en.wikipedia.org/wiki/Chess_strategy
'''
LOG_OFF=0
LOG_LOW=1
LOG_MED=2
LOG_HIGH=3
LOG_FLAG = LOG_OFF # set 0 to disable logging
log_env = os.getenv('ChessGame_LOG')
if log_env:
    LOG_FLAG = LOG_LOW 
    try:
        LOG_FLAG = int(log_env)
    except:
        pass

logger = logging
if LOG_FLAG:
    # import logger in other modules to share same log config
    logger.basicConfig(filename='chess_game.log', filemode='w', \
        level = logging.DEBUG, format= "%(message)s")

def indent_spaces(indent=0):
    return f"{' ':<4}"*indent

def log(mess, indent=0):
    # Output to logging, prefix start with indent number of tabs, right justify caller name.
    # `LOG_FLAG and log(expr)` idiom used to avoid overhead of evaluation expr when no logging
    if LOG_FLAG: 
        caller = inspect.stack()[1][3]  # name of caller function
        str = indent_spaces(indent) + f"{caller:>16}: {mess}"
        logger.debug(str)

def dict_str(name, dict_or_list, indent=0):
    # convert list/dict to string. Used list.join() as only way I could find
    # to get embedded newlines to work with logging
    nitems = len(dict_or_list)
    prefix = f"\n{indent_spaces(indent)}{name}[{nitems}] = "
    str_list = []
    str = ""
    if isinstance(dict_or_list, dict):
        if nitems > 0:
            str_list = [f"{k} : {v}" for (k,v) in dict_or_list.items()]
        str_list.insert(0, prefix + "{")
        str_list[-1] += "}"
        str = ("\n" + indent_spaces(indent+1)).join(str_list)
    else:
        str = prefix + "["
        if nitems > 0:
            str_list = [f"{v}" for v in dict_or_list]
            str += ", ".join(str_list)
        str += "]"
    return str

class Pieces():
    # All the current turn pieces
    def __init__(self, game, nest_level=1):
        self.game = game
        self.nest_level = nest_level
        self.pieces = {} # dict of all pieces; key=(row, col), value=GameObject()
        self.moves = {} # pos (row,col) that can move; value=list of destinations 
        self.takes = {} # pos that can take; value=list of black pieces
        self.take_moves = {} # dict of moves (pos, dest) :: take_value 
        self.destinations = set()   # set of destinations to test if black can take
        not_pawn_destinations = set() # same but excluding pawns as they can take diagonally
        pawn_take_destinations = set() # possible pawn takes
        self.kill_zone = set()  # non-pawn moves plus hypothetical pawn takes
        self.move_vals = [] # moves list sorted on white piece value
        self.take_vals = [] # take list sorted on black take value
        self.king = None # king (row, col) location
        self.total_value = 0 # value of all pieces
        self.check_mate = False
        self.check = False

        for row_number in range(0, 8):
            for column_number in range(0, 8):
                # visit all squares to find pieces
                row_col = (row_number, column_number) # from position
                piece = game.get_piece_notation(row_col)
                if piece != None and game.test_turn(piece.colour):
                    game.select_piece_to_move(row_col) # update possible moves
                    pos = game.pos_notation(row_col)
                    self.pieces[pos] = piece
                    (abbrv, value) = (piece.abbrv, piece.value)
                    self.total_value += value
                    if abbrv.lower() == 'k':
                        self.king = pos

                    if len(piece.possible_moves) > 0:
                        self.moves[pos] = [game.pos_notation(_row_col) for _row_col in piece.possible_moves]
                        self.destinations.update(self.moves[pos])
                        if abbrv.lower() == 'p':
                            # hmm .. tricky as pawn move changes to diagonal if a take
                            dest_row = [row_number + piece.direction]
                            dest_col = []
                            if column_number < 7:
                                dest_col.append(column_number+1)
                            if column_number > 0:
                                dest_col.append(column_number-1)
                            pawn_take_destinations.update(
                                [game.pos_notation((_r, _c)) 
                                        for _r in dest_row for _c in dest_col])
                        else:
                            not_pawn_destinations.update(self.moves[pos])
                        self.kill_zone = pawn_take_destinations | \
                                            not_pawn_destinations

                        moves = [(pos, dest, abbrv, value) for dest in self.moves[pos]]
                        self.move_vals.extend(moves)

                        takes = [op for op in 
                            [game.get_piece_notation(dest) for dest in self.moves[pos]] 
                                                    if op != None]
                        if len(takes) > 0:
                            self.takes[pos] = takes

        self.move_vals.sort(key=lambda x: x[3], reverse=True) # sort on piece value, shuffle king to top
        self.check_mate = True if self.king == None else False # king taken so checkmate
        for pos in self.takes:
            # list of take moves (pos, dest) in take value order
            _p = self.pieces[pos]
            for _t in self.takes[pos]:
                self.take_moves[(pos, game.pos_notation(_t.pos()))] = \
                                    (_p.abbrv, _p.value, _t.abbrv, _t.value)
                self.take_vals.append(((pos, _p.abbrv, _p.value), \
                    (game.pos_notation(_t.pos()), _t.abbrv, _t.value)))
        self.take_vals.sort(key=lambda x: x[1][2], reverse=True) # sort on _t.value
    
    def __repr__(self):
        indent = self.nest_level + 1
        str = ""
        str += f"Pieces() : {self.game.get_turn_colour()} total_value={self.total_value} king={self.king}"
        str += f"{dict_str('pieces', self.pieces, indent)} "
        str += f"{dict_str('moves', self.moves, indent)} "
        str += f"{dict_str('takes', self.takes, indent)} "
        str += f"{dict_str('take_moves', self.take_moves, indent)} "
        str += f"{dict_str('move_vals', self.move_vals, indent)} "
        str += f"{dict_str('take_vals', self.take_vals, indent)} "
        str += f"{dict_str('destinations', self.destinations, indent)} "
        str += f"{dict_str('kill_zone', self.kill_zone, indent)} "
        return str

class RandomMove():
    PERM_SEMI_RANDOM_BIT = 0  # semi-random, avoid king moves and moving into kill zone
    PERM_TAKE_BIT = 1 # take()
    PERM_DODGE_BIT = 2 # dodge()
    PERM_LOOKAHEAD_BIT = 3 # lookahead()
    perm_all = -1
    perm_lookahead = (1 << PERM_LOOKAHEAD_BIT)
    perm_notlook = perm_all & ~perm_lookahead # all but lookahead, to slow at the moment

    def __init__(self, game, perm=-1, nest_level=1):
        self.game = game
        self.permutations = perm # bit msk of functions to run before random_move()
        self.nest_level = nest_level # debug nesting level, useful when try_move()
        self.totals = []    # multithread lookahead 

        self.white = Pieces(game, nest_level+1) # this colours pieces
        game.toggle_turn() # swap turn
        self.black = Pieces(game, nest_level+1) # other colour pieces
        game.toggle_turn() # swap turn back

        self.white.check = True if not self.white.check_mate and \
                (self.white.king in self.black.destinations) else False
        self.black.check = True if not self.black.check_mate and \
                (self.black.king in self.white.destinations) else False

        # white move that can be followed by black take
        # intersect (in both sets)
        shared_dest = self.white.destinations & self.black.kill_zone
        self.white_moves_black_take = {(pos, dest): game.get_piece_notation(pos)
                    for pos in self.white.moves
                        for dest in self.white.moves[pos] if dest in shared_dest}
        
        (LOG_FLAG >= LOG_HIGH) and log(self.__repr__())

    def __repr__(self):
        indent = self.nest_level
        str = ""
        str += f"RandomMove(): {self.game.get_turn_colour()} perm={hex(self.permutations)}"
        str += "\n" + indent_spaces(indent) + f"'white': check={self.white.check} pieces={self.white}"
        str += "\n" + indent_spaces(indent) + f"'black': check={self.black.check} pieces={self.black}"
        str += f"{dict_str('white_moves_black_take', self.white_moves_black_take, indent)} "
        return str

    def dest_then_black_take(self, dest):
        res = dest in self.black.kill_zone
        (LOG_FLAG >= LOG_HIGH) and log(f"{res} dest={dest}", indent=self.nest_level+1)
        return res

    def take(self, val=-1):
        # PERM_TAKE, best value take greater than val
        move = None
        taken = '.'
        val = -1
        for _take in self.white.take_vals:
            # first in list has (joint) highest value
            ((pos, p_abbrv, p_value), (t_pos, t_abbrv, t_value)) = _take
            LOG_FLAG and log(f"piece={(pos, p_abbrv, p_value)}, take={(t_pos, t_abbrv, t_value)}", indent=self.nest_level+1)
            if t_value < val:
                break   
            if self.dest_then_black_take(t_pos):
                continue    # avoid as can be taken by black
            else:
                move = (pos, t_pos, p_abbrv)
                taken = t_abbrv
                val = t_value
                break
        LOG_FLAG and log(f"move={move}, taken={taken}, val={val}", indent=self.nest_level)
        return move, taken, val
    
    def dodge_list(self, val):
        # Check if I can be taken, have a value greater than val and 
        # there is a move that can be made
        froms = []
        for take_val in self.black.take_vals:
            # take_val[0] is black, take_val[1] is white
            (_tpos, _tabbrv, _tvalue) = take_val[1]
            if _tvalue < val: 
                # stop looking as attack better than defence
                break
            if _tpos in self.white.moves:
                # possible escape
                froms.append(take_val[1])
        froms.sort(key=lambda x: x[2], reverse=True) # sort on value
        (LOG_FLAG >= LOG_HIGH) and log(f"froms={froms}", indent=self.nest_level+1)
        return froms
    
    def dodge(self, val):
        # PERM_DODGE, move piece value greater than val that can be taken 
        froms = self.dodge_list(val) # sorted pieces greater than val in jeopardy
        move, taken, val = None, '.', -1
        if len(froms) == 0:
            return move, taken, val

        dodges = [] # escape moves that could be made
        takers = [] # escape moves that can take

        for (pos, p_abbrv, p_value) in froms:
            for dest in self.white.moves[pos]:
                # loop through all possible (pos, dest) moves
                if self.dest_then_black_take(dest):
                    # takeable so keep looking
                    continue
                _move = (pos, dest, p_abbrv)
                move_val = (_move, p_value)
                if (pos, dest) in self.white.take_moves:
                    # this move is a taker
                    (pabbrv, pvalue_, taken, tvalue)= self.white.take_moves[(pos, dest)] # e.g. ('r', 4, 'P', 1)
                    takers.append((move_val, taken, tvalue))  # TODO: if tvalue > p_value:  # value of black piece taken gt white piece
                dodges.append(move_val) # value of piece moving

        # sort takers on dest value, dodges already sorted on from value
        takers.sort(key=lambda x: x[2], reverse=True) 
        (LOG_FLAG >= LOG_HIGH) and log(f"dodge takers [{len(takers)}]={takers}", indent=self.nest_level)
        (LOG_FLAG >= LOG_HIGH) and log(f"dodges[{len(dodges)}]={dodges}", indent=self.nest_level)

        pval = 0
        if len(takers):
            # best value take move
            ((move, pval), taken, val) = takers[0] 
            (LOG_FLAG >= LOG_HIGH) and log(f"takers move={move}, piece_value={pval}, taken={taken}, taken_val={val}, takers[{len(takers)}]={takers}", indent=self.nest_level)
        
        # list of more valuable piece than taker
        _move = None
        better_dodges = [(_move, _pval) for (_move, _pval) in dodges if _pval > pval]
        if len(better_dodges):
            move, taken, val = _move, '.', 0
            LOG_FLAG and log(f"dodges move={move}, taken={taken}, val={val}", indent=self.nest_level+1)

        return move, taken, val

    def random_move(self):
        # avoid moving king to reduce check jeopardy
        move = None
        moves = self.white.move_vals # fmt: (pos, dest, abbrv, value)

        if len(moves) > 0:
            if self.permutations & (1 << RandomMove.PERM_SEMI_RANDOM_BIT):
                avoid_take = [_m for _m in moves if not self.dest_then_black_take(_m[1])]
                if len(avoid_take):
                    moves = avoid_take  # avoid a move that is then taken
                non_king = [_m for _m in moves if _m[2].lower() != 'k']
                if len(non_king):
                    moves = non_king   # avoid king going on a suicide run
            move = random.choice(moves)[:3]
        LOG_FLAG and log(f"move={move}", indent=self.nest_level)
        return move
    
    def get_move(self, perm=-1):
        # return: (pos, dest, abbrv), taken
        colour = self.game.get_turn_colour()
        move, taken, val = None, '.', -1
        if perm == -1:
            perm = self.permutations
        
        LOG_FLAG and log(16*"+" + f" start {self.game.nturn} {colour} perm={perm}")
        start_time = time.perf_counter()

        if self.white.check:
            # In check so look for move to get out of check
            return self.escape_check()
        
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
        
        if perm & (1 << RandomMove.PERM_LOOKAHEAD_BIT):
            res = self.lookahead()
            if res[0] != None:
                if res[0] != move:
                    # After all this, is lookahead better ?
                    LOG_FLAG and log(f"{res} differs from previous move={move}")
                (move, taken) = res        
        
        LOG_FLAG and log(16*"-" + f" move={move}, taken={taken}; " + 
            f"{colour} : duration={time.perf_counter()-start_time:0.4f} " +
            f"nwhite={len(self.white.pieces)}, nblack={len(self.black.pieces)}", 
                indent=self.nest_level)
        return move, taken

    def escape_check(self):
        # Try all moves and return one that changes check state
        # TODO: rework to find move to put other into check
        # return: (pos, dest, abbrv), taken
        global LOG_FLAG
        log_flag = LOG_FLAG  # disable log in try_move
        abbrv, pos, dest, taken = "", None, None, "." 
        move = None
        not_check = []
        indent = self.nest_level + 1

        if not self.white.check:
            return (pos, dest, abbrv), taken
        
        LOG_FLAG and log(f"started", indent=indent)

        for pos in self.white.moves:
            for dest in self.white.moves[pos]:
                _move = (pos, dest)
                (LOG_FLAG >= LOG_HIGH) and log(f"try {_move}", indent=indent)
                LOG_FLAG = False # suppress log to avoid info overload
                rm = self.try_move(_move, self.permutations, self.nest_level+1)
                if rm == None:
                    LOG_FLAG = log_flag
                    LOG_FLAG and log(f"dodgy {_move}", indent=indent)
                    continue
            
                if rm.white.check != self.white.check:
                    # Found a move to get out of check
                    not_check.append((_move, rm.white.total_value))
                LOG_FLAG = log_flag
        not_check.sort(key=lambda x: x[1], reverse=True) # sort on total_value

        if len(not_check):
            LOG_FLAG and log(dict_str("not_check", not_check, indent))
            move = not_check[0][0] # best total_value
            # test if move can be taken
            avoid_take = [_m for (_m, _val) in not_check if not self.dest_then_black_take(_m[1])]
            if len(avoid_take):
                move = avoid_take[0]
        
        if move == None:
            self.white.check_mate = True
        else:
            (pos, dest) = move
            if move in self.white.take_moves:
                (abbrv, value, taken, t_value) = self.white.take_moves[move]
            else:
                abbrv = self.game.get_piece_notation(pos).abbrv
            move = (pos, dest, abbrv)

        LOG_FLAG and log(f"{(move), taken}", indent=indent)
        return move, taken

    def try_move(self, move, perm, nest_level):
        # copy the game and make the move. Return summary of 'white' board positions
        rm = None
        (pos, dest) = move
        _perm = perm & ~(1 << RandomMove.PERM_LOOKAHEAD_BIT) # dont lookahead
        turn = self.game.turn
        (LOG_FLAG >= LOG_MED) and log(f"'white' {self.game.get_turn_colour()} {_perm} {move}", nest_level)

        dupl_game = copy.deepcopy(self.game)
        dupl_game.nturn = self.game.nturn*1000 # makes it easier to follow in trace
        try:
            dupl_game.move_pos(pos, dest)
            dupl_game.turn = turn # move has toggled turn so reset to original
            rm = RandomMove(dupl_game, _perm, nest_level=nest_level)
        except ChessExc as exc:
            assert False, f"internal error: try_move {move} raises exception: {exc} {exc.err}"

        return rm

    def try_white(self, move, nest_level):
        # 'white' move followed by 'black' auto reply
        # return (white.total, black.total) after auto.
        colour = self.game.get_turn_colour()
        turn = self.game.turn # turn colour index
        perm = self.permutations & ~(1 << RandomMove.PERM_LOOKAHEAD_BIT) # dont lookahead
        dupl_rm = None
        am = None # aut_move result
        white_total = black_total = -1
        
        (LOG_FLAG >= LOG_MED) and log(f"'white' {colour} {move}", nest_level)
        dupl_rm = self.try_move(move, perm, nest_level) # 'white'
        if dupl_rm != None:
            dupl_rm.game.toggle_turn() # 'black'
            am = random_auto_move(dupl_rm.game, perm) # black

        if am != None:
            # 'white' before move is 'black' after auto
            (totals, pieces) = dupl_rm.game.game_values()
            white_total = totals[turn]
            black_total = totals[int(not(turn))]
        else:
            (LOG_FLAG >= LOG_MED) and log(f"'black' no move so loses")
            white_total = 999
            black_total = -1

        return  (white_total, black_total)

    def lookahead(self):
        # return: (pos, dest, abbrv), taken
        global LOG_FLAG
        log_flag = LOG_FLAG  # disable log in try_move
        abbrv, pos, dest, taken = "", None, None, "." 
        move = None
        indent = self.nest_level + 1
        colour = self.game.get_turn_colour()
        self.totals = []

        threads = []
        thread_flag = False

        LOG_FLAG and log(f"started", indent=indent)
        LOG_FLAG = False # suppress log to avoid info overload

        for pos in self.white.moves:
            for dest in self.white.moves[pos]:
                _move = (pos, dest)
                if not thread_flag:
                    (white_total, black_total) = self.try_white(_move, self.nest_level+5)
                    self.totals.append((_move,
                        white_total - black_total,
                        white_total, black_total))
                else:
                    th = myThread(self, _move, self.nest_level+1, 
                                self.permutations, log_flag)
                    threads.append(th)
        if thread_flag:
            for th in threads:
                th.start()
            for th in threads:
                th.join()
            for th in threads:
                self.totals.append((th.move,
                        th.white_total - th.black_total,
                        th.white_total, th.black_total))

        LOG_FLAG = log_flag

        totals = self.totals
        totals.sort(key=lambda x: x[1], reverse=True) # sort on total_value
        pos_dest = None
        if len(totals):
            # (('a2', 'a3'), 0, 51, 51)
            best_total = totals[0][1]  # first elem in ordered list
            best_totals = [] # group of best totals
            for total in totals:
                if total[1] != best_total:
                    break # stop looking
                else:
                    best_totals.append(total)
            (LOG_FLAG >= LOG_HIGH) and log(dict_str("totals", totals, indent))
            (LOG_FLAG >= LOG_MED) and log(dict_str("best_totals", best_totals, indent))

            pos_dest = best_totals[0][0] # best total_value delta
            for total in best_totals:
                # avoid moving king
                (pos, dest) = _move = total[0]
                if pos != self.white.king:
                    pos_dest = _move
                    break

        if pos_dest:
            (pos, dest) = pos_dest
            if pos_dest in self.white.take_moves:
                (abbrv, value, taken, t_value) = self.white.take_moves[pos_dest]
            else:
                abbrv = self.game.get_piece_notation(pos).abbrv
            move = (pos, dest, abbrv)

        LOG_FLAG and log(f"{(move), taken}", indent=indent)
        return move, taken


class myThread (threading.Thread):
    def __init__(self, rm, move, nest_level, perm, log_flag):
        threading.Thread.__init__(self)
        self.rm = rm
        self.move = move
        self.nest_level = nest_level
        self.white_total = 0
        self.black_total = 0

    def run(self):
        (self.white_total, self.black_total) = \
            self.rm.try_white(self.move, self.nest_level)

def random_auto_move(game, perm=RandomMove.perm_notlook):
    # Return move to make
    # in: Headless_ChessGame(), perm=bit mask of move permutations e.g. take()
    # out: abbrv, from, to, taken or '.'
    abbrv, from_pos, to_pos, taken = '.', None, None, '.'
    colour = game.get_turn_colour()
    rm = RandomMove(game, perm) # can throw ChessExc exception
    if rm.white.check_mate or rm.black.check_mate:
        return None

    move, taken = rm.get_move(perm)
    if move:
        (from_pos, to_pos, abbrv) = move
        moved = f"{abbrv}{from_pos}:{to_pos}"

        (ncommands, errs) = game.commands(moved)    # will toggle_turn
        LOG_FLAG and log(f"{game.nturn} command={moved}, from_pos={from_pos}, to_pos={to_pos}, taken={taken}, ncommands={ncommands}, errs={errs}, {game.dump(True)}")
        if len(errs) > 0:
            abbrv, from_pos, to_pos, taken = '.', None, None, '.'
        elif taken.lower() == 'k':
            LOG_FLAG and log(f"Checkmate {colour} takes king: {move}, {taken}")
        move = (abbrv, from_pos, to_pos, taken)   # moves and taken piece

    return move
