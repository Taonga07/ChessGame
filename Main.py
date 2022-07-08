from requests import get
from io import BytesIO
import pygame

class ChessGame():
    def __init__(self) -> None:
        self.board_colours = [(0,0,0), (255,255,255)]
        self.board = eval(get("https://tinyurl.com/yck73c8x").content)
        self.window = pygame.display.set_mode((160,160), pygame.RESIZABLE)
        self.piece_images = pygame.image.load(BytesIO(get("https://tinyurl.com/4prmu6ws").content)).convert_alpha()
    def __call__(self) -> None:
        pygame.display.set_icon(pygame.image.load('resources/icon.png'))
        self.main_loop()
    def main_loop(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:exit()
            pygame.display.flip()
    def update_board(self) -> None:
        square_size, image_size = min(self.window.get_size())/8, (self.piece_images.get_width()/6, self.piece_images.get_height()/2)
        squares = {(8*x)+y:{"coords": (x,y), "rect": pygame.draw.rect(self.window, self.board_colours[(x+y)%2], [square_size*y,square_size*x]+[square_size]*2)} for x in range(8) for y in range(8)}
        pieces = {(8*x)+y: {"piece": str(self.board[x][y]), "coords": (x,y), "rect": self.window.blit(pygame.transform.scale(self.piece_images.subsurface([image_size[0]*self.board[x][y][1], image_size[1]*self.board[x][y][0]], image_size), [square_size]*2), [square_size*y,square_size*x])} for x in range(8) for y in range(8) if self.board[x][y] != None}	

if __name__== "__main__":
    ChessGame()()