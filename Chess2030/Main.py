from tkinter import filedialog, Menu, Tk, PhotoImage, colorchooser
from Chess import ChessGame
from os.path import split

class Game():
    def __init__(self, image) -> None:
        self.savedir = 'Games'
        self.root_window = Tk()
        self.root_window.title('ChessGame')
        self.root_window.iconphoto(True, PhotoImage(image))
        self.root_game = ChessGame(self.root_window, savedir=self.savedir)
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
        board, turn = self.root_game.read_game_data()
        self.root_game.board, self.root_game.turn = board, turn
        self.root_game.layout_board()

    def onOpen(self):
        filename = filedialog.askopenfilename(initialdir=self.savedir, title='Open file',
                            filetypes=(("main files","*txt*"),("All files","*.*")))
        board, turn = self.root_game.read_game_data(filename)
        self.root_game.board, self.root_game.turn = board, turn
        self.root_game.layout_board()

    def onSave(self):
        filename = filedialog.asksaveasfilename(initialdir=self.savedir, title='Save as',
                            filetypes=(("main files","*txt*"),("All files","*.*")))
        self.save_file(filename)

    def onBoardCustormise(self):
        light_square_colour = colorchooser.askcolor(title ="Choose 1st color")
        dark_square_colour = colorchooser.askcolor(title ="Choose 2nd color")
        self.root_game.square_colours = (light_square_colour[1], dark_square_colour[1])
        self.root_game.layout_board()

if __name__== "__main__":
    current_game = Game('/Chess_Resorces/Icon.png')
    current_game.root_window.mainloop()