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
    for row_number, rowlist in enumerate(board):
        for column_number, columnEntry in enumerate(rowlist):
            try:
                img = tkinter.PhotoImage(file = board[row_number][column_number].icon)
                square = tkinter.Label(window, bg = bttnclr, image = img)
                square.image = img
            except:
                square = tkinter.Label(window, text = "                 \n\n\n", bg = bttnclr)

            if bttnclr == "white":
                bttnclr = "grey"
            else:
                bttnclr = "white"
            square.grid(row = row_number, column = column_number)
            square.bind("<Button-1>", on_click)
        if bttnclr == "white":
            bttnclr = "grey"
        else:
            bttnclr = "white"


def on_click(event):
    movepiece(window)

def movepiece(window):
    global click
    global old_colour
    global piece_to_move
    Rules.click += 1
    square = on_click.event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    try:
        if ((click == 1 
            and (
                (Rules.turn == 0 and board[row_number][column_number].colour == 'white') 
                or (Rules.turn == 1 and board[row_number][column_number].colour == 'black')
            )) 
            or click == 2
            ):
            currentText = square.cget("text")

            if click == 1:
                print('Where would you like to move your', board[row_number][column_number].piece, 'to?')
                old_colour = board[row_number][column_number].colour
                piece_to_move = row_number,column_number
                reRules.turn
            else:
                if board[row_number][column_number] == 0: #nothing at the square we're moving to
                    if board[piece_to_move[0]][piece_to_move[1]].check_move(row_number,column_number):
                        board[row_number][column_number] = board[piece_to_move[0]][piece_to_move[1]]
                        board[piece_to_move[0]][piece_to_move[1]] = 0
                        layout_window(window)
                        if Rules.turn == 0:
                            Rules.turn = 1
                        else:
                            Rules.turn = 0

                elif (isinstance(board[row_number][column_number], GameObject) and
                    old_colour != board[row_number][column_number].colour):
                    if board[piece_to_move[0]][piece_to_move[1]].check_move(row_number,column_number):
                        board[row_number][column_number] = board[piece_to_move[0]][piece_to_move[1]]
                        board[piece_to_move[0]][piece_to_move[1]] = 0
                        layout_window(window)
                        if Rules.turn == 0:
                            Rules.turn = 1
                        else:
                            Rules.turn = 0
                else:
                    print('you can not take your own piece')
    except:
        if click == 1:
            print('No piece there, try again')
        else:
            print('an error has ocurred')
            raise
    click = 0


if __name__ =="__main__":
    set_up_window()