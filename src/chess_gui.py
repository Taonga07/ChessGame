from pygame import QUIT, RESIZABLE, VIDEORESIZE, MOUSEBUTTONDOWN, KEYDOWN, K_ESCAPE, init
from pygame.display import flip, set_caption, set_mode, set_icon
# from ChessGame.sunfish_interface import sunfish_auto_move
# from ChessGame.calculate_move import random_auto_move
from pygame.mouse import get_pos as get_mouse_pos
from pygame.image import load as load_image
from pygame.event import get as get_events
from pygame.draw import rect as draw_rect
from chess_headless import HeadlessChess
# from pygame._sdl2 import messagebox
from pygame.transform import scale
# from ChessGame.API import ChessExc
from sys import exit as sys_exit
from requests import get
from io import BytesIO
from time import sleep
from math import ceil

class ChessGUI():
    def __init__(self, colours=[[50.2]*3, [255]*3]) -> None:
        self.piece_images = load_image(BytesIO(get(URL+"pieces.svg").content))
        self.window_icon = load_image(BytesIO(get(URL+"icon.png").content))
        self.board_colours = colours#, self.chessgame.board = colours, board
        self.window = set_mode((400,400), RESIZABLE)
        self.pieces = self.squares = {}
        self.game = HeadlessChess()

    def __call__(self) -> None:
        "main game loop for the GUI"
        set_icon(self.window_icon), set_caption("ChessGame"), self.window.fill([178]*3)
        self.window.blit(scale(self.window_icon, self.window.get_size()), [0,0])
        flip(), sleep(0.75), self.window.fill([255]*3), flip()
        # awnser = messagebox("Roar!", "Double roar!", info=True, buttons=("Yes", "No", "Don't know"), return_button=0, escape_button=1)
        
        self.update_board(self.game.get_pieces())  
        while True:
            for event in get_events():
                if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT): sys_exit()
                # if event.type == MOUSEBUTTONDOWN:
                #     for piece_key in self.pieces:
                #         if self.pieces[piece_key]["rect"].collidepoint(get_mouse_pos()):
                #             highlighted_squares = {piece_key: (0,0,125)} # get possible move from headless.py instead of hardcoding
                #             self.update_board(highlighted_squares)
                #             print(pieces[piece_key]["coords"])
                if event.type == VIDEORESIZE:
                    self.update_board(self.game.get_pieces())
            flip()

    def update_board(self, pieces, highlighted_squares={}) -> None:
        "Draws the board and pieces while updating the their dictionaries to match the new board"
        square_size, image_size = ceil(min(self.window.get_size()))/8, (self.piece_images.get_width()/6, self.piece_images.get_height()/2)
        self.squares = [draw_rect(self.window, (self.board_colours[(x+y)%2] if ((8*x)+y) not in highlighted_squares.keys() else highlighted_squares[(8*x)+y]), [square_size*y,square_size*x]+[square_size]*2) for x in range(8) for y in range(8)]
        self.pieces = {x: self.window.blit(scale(self.piece_images.subsurface([image_size[0]*pieces[x]["piece"], image_size[1]*pieces[x]["colour"]], image_size), [square_size]*2), [square_size*x for x in pieces[x]["pos"]]) for x in pieces}
        

URL = "https://raw.githubusercontent.com/Taonga07/ChessGame/master/resources/"

if __name__== "__main__":
    init()
    ChessGUI()()