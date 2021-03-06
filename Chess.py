import tkinter, File, CC, CP, os
from tkinter import messagebox

def set_up_window():
    window = tkinter.Tk()
    #window.iconbitmap('Icon.ico')
    window.title('chess')
    return window

def play_chess(file):
    window = set_up_window()
    board = reset_board(file)
    File.menu(window, board)
    layout_board(window, board)
    window.mainloop()

def reset_board(file):
    board = []
    for column_number in range(0, 8):
        ColumnList = []
        for row_number in range(0, 8):
            ColumnList.append(None)
        board.append(ColumnList)
    input_file = open(file, 'r')
    input_data = input_file.readlines()
    input_file.closed
    for i in input_data:
        Piece, Colour, Row, Column = i.rstrip().split(' ')
        piece = eval(Piece+'(str(Colour)'+', '+'int(Column)'+', '+'int(Row))')
        board[int(piece.row)][int(piece.column)] = piece 
    return board
def save_board(file, board):
    filehandle = open(file, 'w')
    for column_number in range(0, 8):
        for row_number in range(0,8):
            if board[column_number][row_number] != None:
                write = 'CP.' + board[column_number][row_number].piece + ' ' + board[column_number][row_number].colour + ' ' + str(row_number) + ' ' + str(column_number) + ' ' + '\n'
                filehandle.write(write)
    filehandle.close()

# completely remove all grid slaves - causes some flicker
def clear_board_ui(window):
    grid_slaves = window.grid_slaves()
    if len(grid_slaves) > 0:
        for g in grid_slaves:
            g.destroy()

# remove only the grid slaves for the specified row/column
def remove_grid_item(window, row_number, column_number):
    grid_slaves = window.grid_slaves(row_number, column_number)
    if len(grid_slaves) > 0:
        for g in grid_slaves:
            g.destroy()

def layout_board(window, board):
    # causes flicker so don't use this
    #clear_board_ui(window)

    grid_slaves = window.grid_slaves()
    print(f"layout_board, grid slaves count: {len(grid_slaves)}")
    for column_number in range(0, 8):
        for row_number in range(0, 8):
            if board[column_number][row_number] == None:
                square = tkinter.Label(window, text = "                 \n\n\n", bg = CC.bttnclrs[CC.bttnclr_turn])
            else:
                img = tkinter.PhotoImage(file = board[column_number][row_number].icon)
                square = tkinter.Label(window, bg = CC.bttnclrs[CC.bttnclr_turn], image = img)
                square.image = img

            # Connor added - remove any existing grid item at this location - stops UI memory leak
            remove_grid_item(window, row_number, column_number)

            square.grid(row = row_number, column = column_number, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E)
            square.bind("<Button-1>", lambda event, data=window, data1 = board: on_click(event, data, data1))
            CC.bttnclr_turn = 1-CC.bttnclr_turn
        CC.bttnclr_turn = 1-CC.bttnclr_turn

def CheckForCheck(board, colour):
    check_pieces = []
    #go througheach sqaue in board chech is the piece can take the king at the sqaure with find moves
    for column_number in range(0, 8):
        for row_number in range(0, 8):
            if board[column_number][row_number] != None:
                if board[column_number][row_number].colour != colour: # we are not taking our own piece
                    board[column_number][row_number].find_moves(board) # reset possible moves for current piece
                    for move in (board[column_number][row_number].possible_moves): # go through the list
                        row, column = move #set item to the row and column it is made of for fute use
                        if (board[row][column] != None) and (board[row][column].piece == 'King') and (board[row][column].colour == colour):
                            check_pieces.append(board[column_number][row_number])
#this test if we can take the piece that has our king in check
    for column_number in range(0, 8):
        for row_number in range(0, 8):
            if board[column_number][row_number] != None:
                if board[column_number][row_number].colour == colour: # we are not setting restrictions for the otherside
                    board[column_number][row_number].find_moves(board) # reset possible moves for current piece
                    for move in (board[column_number][row_number].possible_moves): # go through the list
                        row, column = move #set item to the row and column it is made of for fute use
                        if board[row][column] not in check_pieces:
                            board[column_number][row_number].possible_moves.remove(move)
    if check_pieces == []: #if there is no moves out of check
        tkinter.messagebox.showinfo('Checkmate', f'{colour} wins! Well Done!')

def on_click(event, window, board):
    CC.onclick = 1 - CC.onclick
    square = event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    print(f"on_click {row_number}, {column_number}")
    square_clicked = (row_number, column_number)
    piece_clicked = board[column_number][row_number]
    if CC.onclick == 0: # this is our fist click we are selecting the piece we want to move
        if (piece_clicked != None)and(((CC.turn == 0)and(piece_clicked.colour == 'White'))or((CC.turn == 1)and(piece_clicked.colour == 'Black'))):
            ##CheckForCheck(board, piece_clicked.colour) # check for check/checkmate
            CC.square_clicked = square_clicked #row_number,column_number
            piece_clicked.possible_moves = [] # reset posible moves
            piece_clicked.find_moves(board)
            CC.old_click = square_clicked
            piece_clicked.highlight_moves(window, board)
        else: # if there is no piece or wrong colour piece where we clicked
            tkinter.messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")
            CC.onclick = 1 - CC.onclick
    else: # this is our second click, we are selecting the square to move to
        row, column = CC.old_click
        old_piece = board[row][column]
        if square_clicked not in old_piece.possible_moves: # check possible move for piece
            tkinter.messagebox.showinfo("Move Not Allowed", "Your piece can not move there!")
            layout_board(window, board) #reset board
            return
        board[column_number][row_number] = board[CC.old_click[0]][CC.old_click[1]]
        board[column_number][row_number].row = row_number
        board[column_number][row_number].column = column_number
        board[CC.old_click[0]][CC.old_click[1]] = None
        layout_board(window, board) #reset board
        CC.turn = 1 - CC.turn

if __name__ =="__main__":
    play_chess('Test.txt')