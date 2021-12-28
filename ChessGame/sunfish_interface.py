from os.path import exists
import time

from ChessGame.calculate_move import log # share logging


path_to_sunfish='sunfish.py'
url = "https://raw.githubusercontent.com/thomasahle/sunfish/master/sunfish.py"

def url_download(path_to_file, url):
    import requests

    # curl  https://raw.githubusercontent.com/thomasahle/sunfish/master/sunfish.py -o sunfish.py 
    log(f"{path_to_file} does not exist, downloading from {url}")
    r = requests.get(url)
    with open(path_to_file, 'w') as f:
        f.write(r.text)

if not exists(path_to_sunfish):
    url_download(path_to_sunfish, url)
import sunfish


def board_to_sunfish(board):
    assert len(board) == 8*8 + 8
    sun_board = []

    for row_index in range(12):
        # sunfish board
        sindex = (row_index*10)
        sun_board[sindex+1:sindex+10] = 9*' ' + '\n'

    for row_index in range(8):
        # copy board contents to sunfish board
        bindex = row_index*9
        row = board[bindex+1:bindex+9]

        sindex = ((row_index+2)*10)
        sun_board[sindex+1:sindex+9] = row
    
    return ''.join(sun_board)




class SunFishModel(object):
    MOVE_WON, MOVE_LOST, MOVE_MATE, MOVE_INVALID, MOVE_OK, MOVE_NONE, MOVE_BLACK, MOVE_WHITE = range(8)
    COLOUR = {MOVE_WHITE: 'White', MOVE_BLACK: 'Black'}
    initial = sunfish.initial
    def __init__(self, board=initial):
        self.pos_list= [sunfish.Position(board, 0, (True,True), (True,True), 0, 0)]
        self.searcher = sunfish.Searcher()
        self.your_moves = []
        self.moves = []
        self.status = SunFishModel.MOVE_NONE

    def get_move(self, colour=MOVE_BLACK, duration=0.5):
        self.status = SunFishModel.MOVE_NONE

        if colour == SunFishModel.MOVE_BLACK:
            self.pos_list[-1].rotate()

        hist = self.pos_list[-1]
        start = time.time()
        for _depth, move, score in self.searcher.search(hist, self.pos_list):
            if time.time() - start > duration:
                break

        if score == sunfish.MATE_UPPER:
            print(f"{SunFishModel.COLOUR[colour]} Checkmate!")
            self.status = SunFishModel.MOVE_MATE
        
        piece = str(hist.board[move[0]])
        taken = str(hist.board[move[1]])
        my_move = move
        if colour == SunFishModel.MOVE_BLACK:
            # board rotated
            piece = piece.lower() 
            taken = taken.lower()
            my_move = (119-move[0], 119-move[1])
        my_move = f"{piece}{sunfish.render(my_move[0])}:{sunfish.render(my_move[1])}"

        log(f"sunfish_move {SunFishModel.COLOUR[colour]} {len(self.pos_list)}: {my_move, taken, _depth, move, score}")
        return (my_move, taken)
 
    def move(self, move_pos):
        pos=self.pos_list[-1]
        self.pos_list.append(pos.move((move_pos[0], move_pos[1])))
        return self.pos_list[-1]
    
    def your_move(self, your_move):
        # white your_move eg. ("a2", "a4")
        self.status = SunFishModel.MOVE_NONE

        move = sunfish.parse(your_move[0]), sunfish.parse(your_move[1])
        log(f"your_move {your_move} : {move}")

        if move not in self.pos_list[-1].gen_moves():
            log(f"invalid move {your_move}")
            self.status = SunFishModel.MOVE_INVALID
        else:
            self.your_moves.append((sunfish.render(move[0]) + sunfish.render(move[1])))
            print("Your move:", self.your_moves[-1] )
            self.move(move)
            self.status = SunFishModel.MOVE_OK

            # After our move we rotate the board and print it again.
            # This allows us to see the effect of our move.
            sunfish.print_pos(self.pos_list[-1].rotate())

            if self.pos_list[-1].score <= -sunfish.MATE_LOWER:
                print("You won")
                self.status = SunFishModel.MOVE_WON
    
                    
    def sunfish_move(self, colour=MOVE_BLACK, duration=1.0):
        self.status = SunFishModel.MOVE_NONE
        # Fire up the engine to look for a move.
        start = time.time()
        for _depth, move, score in self.searcher.search(self.pos_list[-1], self.pos_list):
            if time.time() - start > duration:
                break

        if score == sunfish.MATE_UPPER:
            print(f"{SunFishModel.COLOUR[colour]} Checkmate!")
            self.status = SunFishModel.MOVE_MATE
        
        piece = str(self.pos_list[-1].board[move[0]])
        my_move = move
        if colour == SunFishModel.MOVE_BLACK:
            # board rotated
            piece = piece.lower() # black move
            my_move = (119-move[0], 119-move[1])
        my_move = f"{piece}{sunfish.render(my_move[0])}:{sunfish.render(my_move[1])}"

        log(f"sunfish_move {SunFishModel.COLOUR[colour]} {len(self.pos_list)}: {my_move, _depth, move, score}")

        self.moves.append(my_move)
        self.move(move)

        if self.pos_list[-1].score <= -sunfish.MATE_LOWER:
            print(f"{SunFishModel.COLOUR[colour]} You lost")
            self.status = SunFishModel.MOVE_LOST
    
    def moved_piece(self, colour=MOVE_BLACK):
        # return piece abbrv just moved
        return self.moves[-1]

    def print_pos(self, colour=MOVE_WHITE):
        # assumed invoked after colour move
        hist = self.pos_list[-1]
        sunfish.print_pos(hist if colour==SunFishModel.MOVE_BLACK else hist.rotate())

def sunfish_auto_move(game):
    # Return move to make, in: Headless_ChessGame(), out: from, to, taken or '.'
    game_dump = game.dump()
    sunfish_layout = board_to_sunfish(game_dump)
    m = SunFishModel(sunfish_layout)
    colour = SunFishModel.MOVE_WHITE if game.test_turn('white') else SunFishModel.MOVE_BLACK
    (moved, taken) = m.get_move(colour)
    moves = moved.split(':') if moved else None
    from_pos, to_pos = (None, None), (None, None)
    if len(moves) == 2:
        from_pos=moves[0][1:] # first char piece, last two chars board coords
        to_pos = moves[1]

    if m.status == SunFishModel.MOVE_NONE:
        (ncommands, errs) = game.commands(moved)    # will toggle_turn
        log(f"{SunFishModel.COLOUR[colour]} command={moved}, from_pos={from_pos}, to_pos={to_pos}, taken={taken}, ncommands={ncommands}, errs={errs}, {game.dump(True)}")

    return moved, from_pos, to_pos, taken   # moves and taken piece

def test1():
    # sanity check layout
    board = (
    'PPPPPPPP\n'
    'RNBQKBNR\n'
    'rnbqkbnr\n' 
    'pppppppp\n'
    '........\n'
    '........\n'
    '........\n'
    '........\n'
    )
    sunfish_board = board_to_sunfish(board)
    m = SunFishModel(sunfish_board)
    m.print_pos()

def main():
    m = SunFishModel()

    for move_index, your_move in enumerate([("a2", "a4"), ("d2", "d3"), ()]):
        log(f"index={move_index} {your_move}: {m.print_pos()}")

        if your_move == ():
            break
    
        m.your_move(your_move)
        if m.status != SunFishModel.MOVE_OK:
            break

        m.sunfish_move()

        log(f"\tlast sunfish_move {m.moves[-1]}")
        
if __name__=="__main__":
    test1()
    main()
