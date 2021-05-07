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

def CheckForCheck(board, colour, game_vars):
    attacking_pieces = []
    paths_to_king = []
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            test_piece = board[row_number][column_number]
            if (test_piece != None) and (test_piece.colour != colour):
                test_piece.find_moves(board)
                for move in test_piece.possible_moves:
                    row, column = move # set item to the row and column it is made of for future use
                    square = board[row][column] # set the position of the current square for future use
                    if (square != None) and (square.piece == 'King') and (square.colour == colour):
                        attacking_pieces.append(test_piece)
                    if test_piece.piece != 'Knight':
                        if square.column - test_piece.column != 0:
                            column_dir = int((square.column - test_piece.column) / (abs(square.column - test_piece.column)))
                            column_path = list(range(test_piece.column, square.column, column_dir))
                        if square.row - test_piece.row != 0:
                            row_dir = int((square.row - test_piece.row) / (abs(square.row - test_piece.row)) )
                            row_path = list(range(test_piece.row, square.row, row_dir))
                        if square.column - test_piece.column == 0:
                            column_path = [square.column] * len(row_path)
                        elif square.row - test_piece.row == 0:
                            row_path = [square.row] * len(column_path)
                        print(f'row_path: {row_path}, column_path: {column_path}')
                        attacker_to_king = tuple(zip(row_path, column_path)) 
                        paths_to_king.append(attacker_to_king)
                    
    if attacking_pieces != []: #if pieces are threatening king
        counter_check = []
        messagebox.showinfo('Check', 'Your in Check')
        for row_number in range(0, 8):
            for column_number in range(0, 8):
                if board[row_number][column_number] != None:
                    counter_piece = board[row_number][column_number]
                    if counter_piece.colour == colour: # we are not setting restrictions for the otherside
                        counter_piece.find_moves(board) # reset possible moves for current piece
                        for move in counter_piece.possible_moves: # go through the list
                            if board[move[0]][move[1]] in attacking_pieces: 
                                counter_check.append(counter_piece)
                            elif board[move[0]][move[1]] in paths_to_king:
                                counter_check.append(counter_piece) 
                            else:
                                counter_piece.possible_moves.remove(move)
        if counter_check == []: # that is, we are in check, but have no pieces that can take the attacking piece
            messagebox.showinfo('Checkmate' 'End of Game')

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
            # redundant game_vars['square_clicked'] = game_vars['square_clicked'] #row_number,column_number
            square.config(bg='blue')# highlight square
            piece_clicked.possible_moves = [] # reset posible moves
            piece_clicked.find_moves(board)
            CheckForCheck(board, piece_clicked.colour, game_vars)
            game_vars['old_click'] = game_vars['square_clicked']
            piece_clicked.highlight_moves(window, board)
        else: # if there is no piece or wrong colour piece where we clicked
            messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")
            game_vars['onclick'] = 1 - game_vars['onclick']
    else: # this is our second click, we are selecting the square to move to
        row, column = game_vars['old_click']
        old_piece = board[row][column]
        print('old_piece', old_piece)
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
