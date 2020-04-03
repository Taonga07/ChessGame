import tkinter, Rules, os

def set_up_window():
    window = tkinter.Tk()
    window.title('chess')
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file = Rules.path +'icon.gif'))
    play_chess(window)
    
def play_chess(window):
    board = reset_board()
    create_board(window, board)
    window.mainloop()

def reset_board():
    board = []
    for row in range(0,8):
        rowlist = []
        for column in range(0,8):
            if row == 6:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'White_Pawn.gif', 'white', column, row))
            elif row == 1:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'Black_Pawn.gif', 'black', column, row))
            else:
                rowlist.append(0)
        board.append(rowlist)

    return board

def create_board(window, board):
    bttnclr="white"
    for column_number in board:
        for row_number in column_number:
            img = tkinter.PhotoImage(file = board[row_number][column_number].icon)
            square = tkinter.Label(window, bg = bttnclr, image = img)
            square.image = img

    if bttnclr == "white":
                bttnclr = "grey"
    else:
        bttnclr = "white"


if __name__ =="__main__":
    set_up_window()