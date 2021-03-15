import tkinter, File, CD, CP, os
from tkinter import messagebox

def set_up_window():
    window = tkinter.Tk()
    img = tkinter.PhotoImage(file=CD.path+'Icon-0.png')
    window.iconphoto(True, img)
    window.title('chess')
    return window

def play_chess(file):
    CD.set_vars()
    window = set_up_window()
    board = open_board(file)
    File.menu(window, board)
    layout_board(window, board)
    window.mainloop()

def dump_board(board):
    ''' string list all pieces on the board '''
    lines = []
    for row in board:
        for elem in row:
            if elem != None:
                lines.append(str(elem)) # string repr for class
    return lines

OUT_VERSION='1.0'   # increment version if output format changes, this allows for backward compatibility

def open_board(filename):
    board = []
    for row_number in range(0, 8):
        ColumnList = []
        for column_number in range(0, 8):
            ColumnList.append(None)
        board.append(ColumnList)
    with open(filename, 'r') as input_file:
        input_data = input_file.readlines()
    for input_line in input_data:
        input_line = input_line.strip()
        comment_index = input_line.find('#')
        if comment_index >= 0:
            # remove chars to right of comment
            comment_line = input_line[comment_index+1:].strip()
            input_line = input_line[:comment_index]
            split_arr = comment_line.split('=', 1)
            if len(split_arr) > 1:
                var_name = split_arr[0].strip()
                var_value = split_arr[1].strip()
                print(f"DBG input comment variable: {var_name} = {var_value}")
                if var_name == 'version' and (var_value != OUT_VERSION):
                    ''' Handle old formats, e.g. file is '1.0' but app moved on to '1.2' '''
                    print(f"TODO: input file variable {var_name} = {var_value} differs to supported {OUT_VERSION}")
        #print(f"DBG input_line: {input_line}")
        split_arr = input_line.split(' ')
        if len(split_arr) == 4:
            # ignore lines not 4 tokens
            # Piece, Colour, Row, Column to match save_board()
            (Piece, Colour, Row, Column) = split_arr
            piece = eval(f"CP.{Piece}('{Colour}', {Column}, {Row})")
            board[int(piece.row)][int(piece.column)] = piece 
    if True:
        board_dump = dump_board(board)
        board_dump = '\n\t'.join(board_dump)
        print(f"DBG: dump board {filename}:\n\t{board_dump}")
        
    return board

def save_board(filename, board):
    with open(filename, 'w') as filehandle:
        filehandle.write(f'# version={OUT_VERSION}\n')  # file comment
        filehandle.write(f'# Piece, Colour, Row, Column\n')  # file comment
        for row_number in range(0, 8):
            for column_number in range(0,8):
                if board[row_number][column_number] != None:
                    _piece = board[row_number][column_number].piece
                    _colour = board[row_number][column_number].colour
                    # Piece, Colour, Row, Column to match split() in open_board()
                    _line = f"{_piece} {_colour} {row_number} {column_number}\n"
                    filehandle.write(_line)

def remove_grid_item(window, row_number, column_number):
    grid_slaves = window.grid_slaves(row_number, column_number)
    if len(grid_slaves) > 0:
        for g in grid_slaves:
            g.destroy()

def layout_board(window, board):
    grid_slaves = window.grid_slaves()
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number] == None:
                square = tkinter.Label(window, text = "                 \n\n\n", bg = CD.bttnclrs[CD.bttnclr_turn])
            else:
                img = tkinter.PhotoImage(file = board[row_number][column_number].icon)
                square = tkinter.Label(window, bg = CD.bttnclrs[CD.bttnclr_turn], image = img)
                square.image = img

            # Connor added - remove any existing grid item at this location - stops UI memory leak
            remove_grid_item(window, row_number, column_number)

            square.grid(row = row_number, column = column_number, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E)
            square.bind("<Button-1>", lambda event, data=window, data1 = board: on_click(event, data, data1))
            CD.bttnclr_turn = 1-CD.bttnclr_turn
        CD.bttnclr_turn = 1-CD.bttnclr_turn

def CheckForCheck(board, colour):
    check_pieces = []
    #go througheach sqaue in board chech is the piece can take the king at the sqaure with find moves
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number] != None:
                if board[row_number][column_number].colour != colour: # we are not taking our own piece
                    board[row_number][column_number].find_moves(board) # reset possible moves for current piece
                    for move in (board[row_number][column_number].possible_moves): # go through the list
                        row, column = move #set item to the row and column it is made of for fute use
                        if (board[row][column] != None) and (board[row][column].piece == 'King') and (board[row][column].colour == colour):
                            check_pieces.append(board[row_number][column_number])
#this test if we can take the piece that has our king in check
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number] != None:
                if board[row_number][column_number].colour == colour: # we are not setting restrictions for the otherside
                    board[row_number][column_number].find_moves(board) # reset possible moves for current piece
                    for move in (board[row_number][column_number].possible_moves): # go through the list
                        row, column = move #set item to the row and column it is made of for fute use
                        if board[row][column] not in check_pieces:
                            board[row_number][column_number].possible_moves.remove(move)
    if check_pieces == []: #if there is no moves out of check
        messagebox.showinfo('Checkmate', f'{colour} wins! Well Done!')

def on_click(event, window, board):
    CD.onclick = 1 - CD.onclick
    square = event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    print(f"on_click, row: {row_number}, column:{column_number}")
    square_clicked = (row_number, column_number)
    piece_clicked = board[row_number][column_number]
    if CD.onclick == 0: # this is our fist click we are selecting the piece we want to move
        if (piece_clicked != None)and(((CD.turn == 0)and(piece_clicked.colour == 'White'))or((CD.turn == 1)and(piece_clicked.colour == 'Black'))):
            ##CheckForCheck(board, piece_clicked.colour) # check for check/checkmate
            CD.square_clicked = square_clicked #row_number,column_number
            piece_clicked.possible_moves = [] # reset posible moves
            piece_clicked.find_moves(board)
            CD.old_click = square_clicked
            piece_clicked.highlight_moves(window, board)
        else: # if there is no piece or wrong colour piece where we clicked
            messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")
            CD.onclick = 1 - CD.onclick
    else: # this is our second click, we are selecting the square to move to
        row, column = CD.old_click
        old_piece = board[row][column]
        if square_clicked not in old_piece.possible_moves: # check possible move for piece
            messagebox.showinfo("Move Not Allowed", "Your piece can not move there!")
            layout_board(window, board) #reset board
            return
        board[row_number][column_number] = board[CD.old_click[0]][CD.old_click[1]]
        board[row_number][column_number].row = row_number
        board[row_number][column_number].column = column_number
        board[CD.old_click[0]][CD.old_click[1]] = None
        layout_board(window, board) #reset board
        CD.turn = 1 - CD.turn

if __name__ =="__main__":
    play_chess('Test.txt')