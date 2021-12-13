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
    IntVar,
)
import time
from os.path import split, join, expanduser, dirname
from sunfish_interface import sunfish_auto_move
from calculate_move import random_auto_move
from API import ChessExc

class Gui_ChessGame:
    def __init__(self, Headless_ChessGame, square_colours=("White", "Grey")) -> None:
        self.click, self.first_click = 1, (0, 0)
        self.square_colours = square_colours
        self.Game = Headless_ChessGame
        self.create_root_window()
        self.layout_board()
        self.auto = None

    def create_root_window(self):
        self.root_window = Tk()
        self.root_window.title("ChessGame")
        image = join(dirname(__file__), "Chess_Resources", "Icon.png")
        self.root_window.iconphoto(True, PhotoImage(file=image))
        self.create_menu_bar()

    def create_menu_bar(self):
        self.menubar = Menu(self.root_window)

        filemenu = Menu(self.menubar, tearoff=0)
        editmenu = Menu(self.menubar, tearoff=0)
        automenu = Menu(self.menubar, tearoff=0)


        filemenu.add_command(label="New", command=self.onNew)
        filemenu.add_command(label="Open", command=self.onOpen)
        filemenu.add_command(label="Save", command=self.onSave)
        filemenu.add_separator()  # adds line between objects in filemenu dropdown
        filemenu.add_command(label="Exit", command=self.root_window.destroy)

        editmenu.add_command(label="customise board", command=self.onBoardCustormise)

        sunfish_opt = IntVar()
        random_opt = IntVar()
        automenu.add_checkbutton(label="Sunfish", variable=sunfish_opt, command=self.onAutoSunfish)
        automenu.add_checkbutton(label="Random", variable=random_opt, command=self.onAutoRandom)

        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        self.menubar.add_cascade(label="Auto", menu=automenu)

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
    
    def auto_change(self, fn):
        # toggle auto
        # Todo: get access to add_checkbutton() variable
        if self.auto == None:
            self.auto = fn
        else:
            self.auto = None

        print(f"Auto toggled, new value = {self.auto}")
    
    def onAutoSunfish(self):
        self.auto_change(sunfish_auto_move)

    def onAutoRandom(self):
        self.auto_change(random_auto_move)

    def onBoardCustormise(self):
        light_square_colour = colorchooser.askcolor(title="Choose 1st color")
        dark_square_colour = colorchooser.askcolor(title="Choose 2nd color")
        self.square_colours = (light_square_colour[1], dark_square_colour[1])
        self.layout_board()

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
    
    def highlight_square(self, row_number, column_number, delay=0, colour='blue'):
        # highlight a square for duration 
        square = self.root_window.grid_slaves(row=row_number, column=column_number)[0]
        square.config(bg=colour)  # highlight position
        if delay > 0:
            self.root_window.update()
            time.sleep(delay) # TODO dodgy sleep in mainloop

    def on_click(self, event):
        self.click = 1 - self.click
        square_info = event.widget.grid_info()
        square_clicked = (int(square_info["row"]), int(square_info["column"]))
        if self.click == 0:  # on fist click we are select a piece
            # first bit of return states true or false second bit the error
            Allowed_to_select = self.Game.select_piece_to_move(square_clicked)
            if Allowed_to_select[0]:
                messagebox.showinfo(Allowed_to_select[1][0], Allowed_to_select[1][1])
                self.click = 1 - self.click
                self.layout_board()
                return
            event.widget.config(bg="blue")  # highlight clicked square
            piece_clicked = self.Game.board[square_clicked[0]][square_clicked[1]]
            piece_clicked.highlight_moves(self.root_window, self.Game.board)
        else:  # this is our second click, we are selecting the square to move to
            alowed_to_move = self.Game.move_selected_piece(square_clicked)
            if alowed_to_move[0]:
                messagebox.showinfo(alowed_to_move[1][0], alowed_to_move[1][1])
            self.layout_board()  # reset board
            if self.auto:
                try:
                    from_pos, to_pos, taken = self.auto(self.Game)
                except ChessExc as exc:
                    messagebox.showinfo(f"Chess exception {exc}, {exc.err} ")

                if taken.lower() == 'k':
                    messagebox.showinfo(f"Checkmate {'Black' if taken.islower() else 'White'} takes {taken}")
                elif from_pos == None:
                    messagebox.showinfo(f"Error in {self.Game.get_turn_colour()} auto")
                if from_pos:
                    self.highlight_square(*self.Game.notation_pos(from_pos), delay=0, colour='blue')
                    self.highlight_square(*self.Game.notation_pos(to_pos), delay=3, colour='green' if taken == '.' else 'red')
                    self.layout_board()  # reset board



