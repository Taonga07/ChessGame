import tkinter, File, CD, CP, os
from tkinter import messagebox

def set_up_window():
    window = tkinter.Tk()
    img = tkinter.PhotoImage(file=CD.path+'Icon-0.png')
    window.iconphoto(True, img)
    window.title('chess')
    return window

def play_chess(file):
    CD.reset_game_vars(CD.game_vars)
    window = set_up_window()
    board = File.open_board(file)
    File.menu(window, board)
    layout_board(window, board)
    window.mainloop()

def layout_board(window, board):
    grid_slaves = window.grid_slaves()
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number] == None:
                square = tkinter.Label(window, text = "                 \n\n\n", bg = CD.bttnclrs[CD.game_vars['bttnclr_turn']])
            else:
                img = tkinter.PhotoImage(file = board[row_number][column_number].icon)
                square = tkinter.Label(window, bg = CD.bttnclrs[CD.game_vars['bttnclr_turn']], image = img)
                square.image = img

            # Connor added - remove any existing grid item at this location - stops UI memory leak
            File.remove_grid_item(window, row_number, column_number)

            square.grid(row = row_number, column = column_number, sticky = tkinter.N+tkinter.S+tkinter.W+tkinter.E)
            square.bind("<Button-1>", lambda event, data=window, data1 = board, data2 = CD.game_vars: on_click(event, data, data1, data2))
            CD.game_vars['bttnclr_turn'] = 1 - CD.game_vars['bttnclr_turn']
        CD.game_vars['bttnclr_turn'] = 1 - CD.game_vars['bttnclr_turn']

def CheckForCheck(board, colour):
    check_pieces = []
    #go througheach sqaue in board chech is the piece can take the king at the sqaure with find moves
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number] != None:
                test_piece = board[row_number][column_number]
                if test_piece.colour != colour: # we are not taking our own piece
                    test_piece.find_moves(board) # reset possible moves for current piece
                    for move in test_piece.possible_moves: # go through the list
                        row, column = move #set item to the row and column it is made of for fute use
                        if (board[row][column] != None) and (board[row][column].piece == 'King') and (board[row][column].colour == colour):
                            #print('test for check')
                            #print(test_piece, test_piece.possible_moves)
                            check_pieces.append(test_piece)
    # this test if we can take the piece that has our king in check
    # but we only need to run the counter_check if our king is in check
    if check_pieces != []: #if pieces are threatening king
        #print('check')
        #print(board)
        #print(check_pieces)
        counter_check = []
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if board[row_number][column_number] != None:
                    counter_piece = board[row_number][column_number]
                    if counter_piece.colour == colour: # we are not setting restrictions for the otherside
                        counter_piece.find_moves(board) # reset possible moves for current piece
                        #print(counter_piece)
                        #print(counter_piece.possible_moves)
                        for move in counter_piece.possible_moves: # go through the list
                            row, column = move #set item to the row and column it is made of for fute use
                            if board[row][column] in check_pieces: # I think you want to test if the piece threatening the king *is* one of the ones you can reach?
                                #print(f'1: {board[row_number][column_number].possible_moves}')
                                #board[row_number][column_number].possible_moves.remove(move)
                                #print(f'2: {board[row_number][column_number].possible_moves}')
                                counter_check.append(counter_piece)
        if counter_check == []: # that is, we are in check, but have no pieces that can take the attacking piece
            messagebox.showinfo('Checkmate')
            print(check_pieces, counter_check)
        else:
            print(check_pieces, 'can be countered by', counter_check)
            messagebox.showinfo('Check')

def on_click(event, window, board, game_vars):
    game_vars['onclick'] = 1 - game_vars['onclick']
    square = event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    #print(f"on_click, row: {row_number}, column:{column_number}")
    game_vars['square_clicked'] = (row_number, column_number)
    piece_clicked = board[row_number][column_number]
    if game_vars['onclick'] == 0: # this is our fist click we are selecting the piece we want to move
        if (piece_clicked != None)and(((game_vars['turn'] == 0)and(piece_clicked.colour == 'White'))or((game_vars['turn'] == 1)and(piece_clicked.colour == 'Black'))):
            CheckForCheck(board, piece_clicked.colour) # check for check/checkmate
            # redundant game_vars['square_clicked'] = game_vars['square_clicked'] #row_number,column_number
            square.config(bg='blue')# highlight square
            piece_clicked.possible_moves = [] # reset posible moves
            piece_clicked.find_moves(board)
            game_vars['old_click'] = game_vars['square_clicked']
            piece_clicked.highlight_moves(window, board)
        else: # if there is no piece or wrong colour piece where we clicked
            messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")
            game_vars['onclick'] = 1 - game_vars['onclick']
    else: # this is our second click, we are selecting the square to move to
        row, column = game_vars['old_click']
        old_piece = board[row][column]
        if game_vars['square_clicked'] not in old_piece.possible_moves: # check possible move for piece
            messagebox.showinfo("Move Not Allowed", "Your piece can not move there!")
            layout_board(window, board) #reset board
            return
        old_click = game_vars['old_click']
        board[row_number][column_number] = board[old_click[0]][old_click[1]]
        board[row_number][column_number].row = row_number
        board[row_number][column_number].column = column_number
        board[old_click[0]][old_click[1]] = None
        layout_board(window, board) #reset board
        game_vars['turn'] = 1 - game_vars['turn']

if __name__ =="__main__":
    play_chess('Test.txt')
