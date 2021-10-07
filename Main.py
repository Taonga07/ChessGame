from tkinter import filedialog, messagebox, Menu, Tk, PhotoImage, colorchooser
from os.path import split
from Chess import ChessGame
from os import remove

class Game():
    def __init__(self, image) -> None:
        self.root_window = Tk()
        self.root_window.title('ChessGame')
        self.root_window.iconphoto(True, PhotoImage(image))
        self.root_game = ChessGame(self.root_window)
        self.create_menu_bar(self)

    def create_menu_bar(self, board):
        self.menubar = Menu(self.root_window)

        filemenu = Menu(self.menubar, tearoff=0)
        editmenu = Menu(self.menubar, tearoff=0)

        filemenu.add_command(label="New", command=lambda: self.onNew())
        filemenu.add_command(label="Open", command=lambda: self.onOpen())
        filemenu.add_command(label="Save", command=lambda: self.onSave())
        filemenu.add_separator() # adds line between objects in filemenu dropdown
        filemenu.add_command(label="Exit", command=lambda: self.root_window.destroy())
        editmenu.add_command(label="custormise board", command=lambda: self.onBoardCustormise())

        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        self.root_window.config(menu=self.menubar)

    def onNew(self):
        board, turn = self.root_game.read_game_data('New_Game.txt')
        self.root_game.board, self.root_game.turn = board, turn
        self.root_game.layout_board()

    def onOpen(self):
        filename = filedialog.askopenfilename(initialdir='Games', title='Open file',
                            filetypes=(("main files","*txt*"),("All files","*.*")))
        board, turn = self.root_game.read_game_data(split(filename)[1])
        self.root_game.board, self.root_game.turn = board, turn
        self.root_game.layout_board()

    def onSave(self):
        filename = filedialog.asksaveasfilename(initialdir='Games', title='Save as',
                            filetypes=(("main files","*txt*"),("All files","*.*")))
        self.save_file(filename)

    def save_file(self, filename):
        with open(filename, 'w') as filehandle:
            filehandle.write(f'{str(self.root_game.turn)}\n')
            for row_number in range(0, 8):
                for column_number in range(0,8):
                    if self.root_game.board[row_number][column_number] != None:
                        _piece = self.root_game.board[row_number][column_number].piece
                        _colour = self.root_game.board[row_number][column_number].colour
                        _line = f"{_piece} {_colour} {row_number} {column_number}\n"
                        filehandle.write(_line)

    def onBoardCustormise(self):
        self.save_file('Games/temp.txt')
        light_square_colour = colorchooser.askcolor(title ="Choose 1st color")
        dark_square_colour = colorchooser.askcolor(title ="Choose 2nd color")
        self.root_game = ChessGame(self.root_window, file='temp.txt', square_colours=(light_square_colour[1], dark_square_colour[1]))
        remove('Games/temp.txt')

if __name__== "__main__":
    current_game = Game('/Chess_Resorces/Icon.png')
    current_game.root_window.mainloop()