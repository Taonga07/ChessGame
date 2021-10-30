from tkinter import (
    messagebox,
    Tk,
    Menu,
    PhotoImage,
    filedialog,
    colorchooser,
    Label,
    N,
    S,
    W,
    E,
)
from os.path import split, join, expanduser


class Gui_ChessGame:
    def __init__(self, Headless_ChessGame, square_colours=("White", "Grey")) -> None:
        self.click, self.first_click = 1, (0, 0)
        self.square_colours = square_colours
        self.Game = Headless_ChessGame
        self.create_root_window()
        self.layout_board()

    def create_root_window(self):
        self.root_window = Tk()
        self.root_window.title("ChessGame")
        image = "ChessGame/Chess_Resources/Icon.png"
        self.root_window.iconphoto(True, PhotoImage(image))
        self.create_menu_bar()

    def create_menu_bar(self):
        self.menubar = Menu(self.root_window)

        filemenu = Menu(self.menubar, tearoff=0)
        editmenu = Menu(self.menubar, tearoff=0)

        filemenu.add_command(label="New", command=self.onNew)
        filemenu.add_command(label="Open", command=self.onOpen)
        filemenu.add_command(label="Save", command=self.onSave)
        filemenu.add_separator()  # adds line between objects in filemenu dropdown
        filemenu.add_command(label="Exit", command=self.root_window.destroy)
        editmenu.add_command(label="custormise board", command=self.onBoardCustormise)

        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

        self.root_window.config(menu=self.menubar)

    def onNew(self):
        board, turn = self.Game.read_game_data("New_Game.txt")
        self.Game.board, self.Game.turn = board, turn
        self.layout_board()

    def onOpen(self):
        filename = filedialog.askopenfilename(
            initialdir=join(expanduser("~"), ".Chess_Games"),
            title="Open file",
            filetypes=(("main files", "*txt*"), ("All files", "*.*")),
        )
        board, turn = self.Game.read_game_data(split(filename)[1])
        self.Game.board, self.Game.turn = board, turn
        self.Game.layout_board()

    def onSave(self):
        filename = filedialog.asksaveasfilename(
            initialdir=join(expanduser("~"), ".Chess_Games"),
            title="Save as",
            filetypes=(("main files", "*txt*"), ("All files", "*.*")),
        )
        self.Game.save_game_data(filename)

    def onBoardCustormise(self):
        light_square_colour = colorchooser.askcolor(title="Choose 1st color")
        dark_square_colour = colorchooser.askcolor(title="Choose 2nd color")
        self.Game.square_colours = (light_square_colour[1], dark_square_colour[1])
        self.Game.layout_board()

    def layout_board(self):
        bttnclr_turn = 0
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                square_colour = self.square_colours[bttnclr_turn]
                if self.Game.board[row_number][column_number] is None:
                    text, img = "                 \n\n\n", None
                else:
                    img, text = (
                        PhotoImage(
                            file=self.Game.board[row_number][column_number].icon
                        ),
                        None,
                    )
                square = Label(self.root_window, text=text, bg=square_colour, image=img)
                grid_slaves = self.root_window.grid_slaves(row_number, column_number)
                if len(grid_slaves) > 0:
                    for g in grid_slaves:
                        g.destroy()
                square.image = img
                square.grid(row=row_number, column=column_number, sticky=N + S + W + E)
                square.bind("<Button-1>", self.on_click)
                bttnclr_turn = 1 - bttnclr_turn
            bttnclr_turn = 1 - bttnclr_turn

    def on_click(self, event):
        self.click = 1 - self.click
        square_info = event.widget.grid_info()
        square_clicked = (int(square_info["row"]), int(square_info["column"]))
        if self.click == 0:  # on fist click we are select a piece
            # first bit of return states true or false second bit the error
            Allowed_to_select = self.Game.select_piece_to_move(square_clicked)
            if not Allowed_to_select[0]:
                messagebox.showinfo(Allowed_to_select[1][0], Allowed_to_select[1][1])
                self.click = 1 - self.click
                self.layout_board()
                return
            event.widget.config(bg="blue")  # highlight clicked square
            piece_clicked = self.Game.board[square_clicked[0]][square_clicked[1]]
            piece_clicked.highlight_moves(self.root_window, self.Game.board)
        else:  # this is our second click, we are selecting the square to move to
            alowed_to_move = self.Game.move_selected_piece(square_clicked)
            if not alowed_to_move[0]:
                messagebox.showinfo(alowed_to_move[1][0], alowed_to_move[1][1])
            self.layout_board()  # reset board
