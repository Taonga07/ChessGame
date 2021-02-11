import tkinter, CC, CP, os
from tkinter import messagebox

def set_up_window():
    global window
    window = tkinter.Tk()
    window.title('chess')
    return window

def play_chess():
    global board
    window = set_up_window()
    board = reset_board()
    layout_board(window, board)
    window.mainloop()

def reset_board():
    board = []
    for row in range(0, 8):
        rowlist = []
        for column in range(0,8):
            if row == 0:
                for piece in CP.pieces:
                    rowlist.append(piece('Black', column, row))
            elif row == 1:
                rowlist.append(CP.Pawn('Black', column, row))
            elif row == 6:
                rowlist.append(CP.Pawn('White', column, row))
            elif row == 7:
                for piece in CP.pieces:
                    rowlist.append(piece('White', column, row))
            else:
                rowlist.append(None)
        board.append(rowlist)
    return board

def layout_board(window, board):
    for column_number in range(0, 8):
        for row_number in range(0, 8):
            if board[row_number][column_number] == None:
                square = tkinter.Label(window, text = "                 \n\n\n", bg = CC.bttnclrs[CC.bttnclr_turn])
            else:
                img = tkinter.PhotoImage(file = board[row_number][column_number].icon)
                square = tkinter.Label(window, bg = CC.bttnclrs[CC.bttnclr_turn], image = img)
                square.image = img
            square.grid(row = row_number, column = column_number, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E)
            square.bind("<Button-1>", on_click)
            CC.bttnclr_turn = 1-CC.bttnclr_turn
        CC.bttnclr_turn = 1-CC.bttnclr_turn

def on_click(event):
    CC.onclick = 1 - CC.onclick
    square = event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    square_clicked = (row_number, column_number)
    piece_clicked = board[row_number][column_number]
    print(CC.onclick)
    if CC.onclick == 0: # this is our fist click we are selecting the piece we want to move
        if (piece_clicked != None)and(((CC.turn == 0)and(piece_clicked.colour == 'White'))or((CC.turn == 1)and(piece_clicked.colour == 'Black'))):
            square.config(bg='blue') # set clicked square background to blue
            CC.square_clicked = square_clicked #row_number,column_number
            piece_clicked.find_moves(board)
            CC.old_click = square_clicked
            piece_clicked.highlight_moves(window, board)
        else: # if there is no piece or wrong colour piece where we clicked
            tkinter.messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")
            CC.onclick = 1 - CC.onclick
    else: # this is our second click, we are selecting the square to move to
        row, column = CC.old_click
        old_piece = board[row][column]
        valid_move = old_piece.check_move(square_clicked, board) # see if current sqare in possible moves
        if not valid_move:
            tkinter.messagebox.showinfo("Your piece can not move there!", "Move Not Allowed")
            layout_board(window, board) #reset board
            return
        board[row_number][column_number] = board[CC.old_click[0]][CC.old_click[1]]
        board[row_number][column_number].row = row_number
        board[row_number][column_number].column = column_number
        board[CC.old_click[0]][CC.old_click[1]] = None
        layout_board(window, board) #reset board
        CC.turn = 1 - CC.turn

if __name__ =="__main__":
    play_chess()