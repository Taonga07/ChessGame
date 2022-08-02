from pygame import QUIT, RESIZABLE, VIDEORESIZE, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, init
from pygame.display import flip, set_caption, set_mode, set_icon
# from ChessGame.sunfish_interface import sunfish_auto_move
# from ChessGame.calculate_move import random_auto_move
from pygame.mouse import get_pos as get_mouse_pos
from pygame.image import load as load_image
from pygame.event import get as get_events
from pygame.draw import rect as draw_rect
from Headless import HeadlessChess
# from pygame._sdl2 import messagebox
from pygame.transform import scale
# from ChessGame.API import ChessExc
from sys import exit as sys_exit
from requests import get
from io import BytesIO
from time import sleep
from math import ceil

class ChessGUI():
    def __init__(self, board, colours=[[50.2]*3, [255]*3]) -> None:
        self.piece_images = load_image(BytesIO(get(URL+"pieces.svg").content))
        self.window_icon = load_image(BytesIO(get(URL+"icon.png").content))
        self.board_colours, self.board = colours, board
        self.window = set_mode((400,400), RESIZABLE)

    def __call__(self) -> None:
        set_icon(self.window_icon), set_caption("ChessGame"), self.window.fill([178]*3)
        self.window.blit(scale(self.window_icon, self.window.get_size()), [0,0])
        flip(), sleep(0.75), self.window.fill([255]*3), flip()
        # awnser = messagebox("Roar!", "Double roar!", info=True, buttons=("Yes", "No", "Don't know"), return_button=0, escape_button=1)
        
        squares, pieces = self.update_board()
        highlighted_squares = {}  
        while True:
            for event in get_events():
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT): sys_exit()
                if event.type == MOUSEBUTTONDOWN:
                    for piece_key in pieces:
                        if pieces[piece_key]["rect"].collidepoint(get_mouse_pos()):
                            highlighted_squares = {piece_key: (0,0,125)} # get possible move from headless.py instead of hardcoding
                            squares, pieces = self.update_board(highlighted_squares)
                            print(pieces[piece_key]["coords"])
                if event.type == VIDEORESIZE:
                    squares, pieces = self.update_board(highlighted_squares)
            flip()

    def update_board(self, highlighted_squares={}) -> None:
        square_size, image_size = ceil(min(self.window.get_size()))/8, (self.piece_images.get_width()/6, self.piece_images.get_height()/2)
        squares = {(8*x)+y:{"coords": (x,y), "rect": draw_rect(self.window, (self.board_colours[(x+y)%2] if ((8*x)+y) not in highlighted_squares.keys() else highlighted_squares[(8*x)+y]), [square_size*y,square_size*x]+[square_size]*2)} for x in range(8) for y in range(8)}
        pieces = {(8*x)+y: {"piece": str(self.board[x][y].img_pos), "coords": (x,y), "rect": self.window.blit(scale(self.piece_images.subsurface([image_size[0]*self.board[x][y].img_pos[1], image_size[1]*self.board[x][y].img_pos[0]], image_size), [square_size]*2), [square_size*y,square_size*x])} for x in range(8) for y in range(8) if self.board[x][y] is not None}
        return squares, pieces

URL = "https://raw.githubusercontent.com/Taonga07/ChessGame/fixes/resources/"

if __name__== "__main__":
    init()
    chessgame = HeadlessChess()
    ChessGUI(chessgame.board)()

#Plan

## Headless.py
#1. read board icons from text file (board.txt)
#2. create class from icon
#3  pass over board with pice positions in svg file (pieces.svg)

## Gui.py
#1. draw board recived form Headless.py
#2. get first user input
#3. lock user inputs
#4. send input to Headless.py

##Headless.py
#1. recive input and return squares to highlight or error msg

##Gui.py
#1. highlight squares or display error msg
#2. get second user input
#3. lock user inputs
#4. send input to Headless.py

##Headless.py
#1. recieve input
#2. detect if move is valid
#3. return error msg or confirmation to move

##Gui.py
#1. display error msg or confirmation to move
#2. update board
#3. repeat process until game is over