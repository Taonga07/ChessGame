from requests import get
from io import BytesIO
import pygame

class ChessGame():
    def __init__(self) -> None:
        self.board_colours = [[50.2]*3, [255]*3]
        self.board = eval(get(URL+"board.txt").content)
        self.piece_images = pygame.image.load(BytesIO(get(URL+"pieces.svg").content))
        self.window = pygame.display.set_mode((160,160), pygame.RESIZABLE)
    def __call__(self) -> None:
        pygame.display.set_icon(pygame.image.load(BytesIO(get(URL+"icon.png").content)))
        pygame.display.set_caption("ChessGame")
        squares, pieces = self.update_board()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for piece in pieces.values():
                        if piece["rect"].collidepoint(pygame.mouse.get_pos()):
                            print(piece["coords"]) 
                if event.type==pygame.VIDEORESIZE:
                    squares, pieces = self.update_board()
            pygame.display.flip()

    def update_board(self) -> None:
        square_size, image_size = min(self.window.get_size())/8, (self.piece_images.get_width()/6, self.piece_images.get_height()/2)
        squares = {(8*x)+y:{"coords": (x,y), "rect": pygame.draw.rect(self.window, self.board_colours[(x+y)%2], [square_size*y,square_size*x]+[square_size]*2)} for x in range(8) for y in range(8)}
        pieces = {(8*x)+y: {"piece": str(self.board[x][y]), "coords": (x,y), "rect": self.window.blit(pygame.transform.scale(self.piece_images.subsurface([image_size[0]*self.board[x][y][1], image_size[1]*self.board[x][y][0]], image_size), [square_size]*2), [square_size*y,square_size*x])} for x in range(8) for y in range(8) if self.board[x][y] is not None}	
        return squares, pieces

URL = "https://raw.githubusercontent.com/Taonga07/ChessGame/fixes/resources/"

if __name__== "__main__":
    pygame.init()
    ChessGame()()