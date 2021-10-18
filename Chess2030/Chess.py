from tkinter import messagebox, PhotoImage, Tk, Label, N, S, W, E

from ChessHeadless import ChessHeadless

class ChessGame(ChessHeadless):
    def __init__(self, window, square_colours=('White', 'Grey'), file='New_Game.txt'):
        super(ChessGame, self).__init__(file)
        self.square_colours = square_colours
        self.window = window
        self.layout_board()

    def layout_board(self):
        bttnclr_turn = 0
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                square_colour = self.square_colours[bttnclr_turn]
                if self.board[row_number][column_number] == None:
                    text, img = "                 \n\n\n", None
                else:
                    img, text = PhotoImage(file = self.board[row_number][column_number].icon), None
                square = Label(self.window, text = text, bg = square_colour, image = img)
                grid_slaves = self.window.grid_slaves(row_number, column_number)
                if len(grid_slaves) > 0:
                    for g in grid_slaves:
                        g.destroy()
                square.image = img
                square.grid(row = row_number, column = column_number, sticky = N+S+W+E)
                square.bind("<Button-1>", self.on_click)
                bttnclr_turn = 1 - bttnclr_turn
            bttnclr_turn = 1 - bttnclr_turn

    def on_click(self, event):
        self.click = 1 - self.click
        square_info = event.widget.grid_info()
        current_square = (int(square_info['row']), int(square_info['column']))

        if self.click == 0: # on first click we are select a piece
            square_clicked = self.board[current_square[0]][current_square[1]]

            try:
                self.movefrom(current_square[0], current_square[1])
            
            except ChessHeadless.CheckMateExc:
                messagebox.showinfo('Checkmate', 'Checkmate end of game')
                while True:
                    pass
            
            except ChessHeadless.CheckExc:
                messagebox.showinfo('Check', 'you\'re in check')

            except ChessHeadless.InvMoveExc:
                messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")

            else:
                # valid from
                event.widget.config(bg='blue')# highlight clicked square
                square_clicked.highlight_moves(self.window, self.board)

        else: # this is our second click, we are selecting the square to move to
            try:
                self.moveto(current_square[0], current_square[1])

            except ChessHeadless.InvMoveExc:
                messagebox.showinfo("Move Not Allowed", "Your piece cannot move there!")
            finally:
                # always do this
                self.layout_board() #reset board
