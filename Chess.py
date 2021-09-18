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

def check_agianst_check(board, clicked_piece):
    # if you are in check get out of it
    paths_to_king, atackers_pos = [], []
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number]!= None and board[row_number][column_number]!= clicked_piece.colour:
                board[row_number][column_number].find_moves(board, [],)
                for move in board[row_number][column_number].possible_moves:
                    square = board[move[0]][move[1]] # row, column
                    if (square != None) and (square.piece == 'King') and (square.colour == clicked_piece.colour): #our king is in check
                        atackers_pos.append((row_number, column_number))
                        paths_to_king = paths_to_king + board[row_number][column_number].find_path_to_king(move[0], move[1])
                        # code above should add to the paths_to_king it values not the whole list
    if len(paths_to_king) == 0: # paths to king contains squares to prevent check
        #there will alway be 1 move at the moent to end check wich is the piece itself
        return False # so we are not in check
    elif len(paths_to_king) > 0: # you are in check
        ## if len(atackers_pos) > 1: # more than one piece is attacking
        clicked_piece.find_moves(board, paths_to_king, 'z')
        if len(clicked_piece.possible_moves) == 0:
            return True # we can't move
        return False # we can move


def check_for_check(board, clicked_piece): # this function is not used
    # not moving into check
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            if board[row_number][column_number]!= None and board[row_number][column_number]!= clicked_piece.colour:
                board[row_number][column_number].find_moves(board, [])
                for move in board[row_number][column_number].possible_moves:
                    square = board[move[0][move[1]]]
                    if (square != None) and (square.piece == 'King') and (square.colour != clicked_piece.colour): #other king is in check
                        messagebox.showinfo('Check', f'Your {board[row_number][column_number].piece} put the othe player in check')


def on_click(event, window, board, game_vars):
    game_vars['onclick'] = 1 - game_vars['onclick']
    square = event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    game_vars['square_clicked'] = (row_number, column_number)
    piece_clicked = board[row_number][column_number]
    if game_vars['onclick'] == 0: # this is our fist click we are selecting the piece we want to move
        if (piece_clicked != None)and(((game_vars['turn'] == 0)and(piece_clicked.colour == 'White'))or((game_vars['turn'] == 1)and(piece_clicked.colour == 'Black'))):
            #check if we can still move selected piece if we are in check 
            #if we can still move the fuction should limit our moves anyway
            if check_agianst_check(board, piece_clicked):
                # if check_against_check returns True, you selected piec can't move
                messagebox.showinfo('Check', 'you\'re in check')
                game_vars['onclick'] = 1 - game_vars['onclick']
            else: #you can move but moves will be limited if you are in check
                square.config(bg='blue')# highlight square
                piece_clicked.highlight_moves(window, board)
                game_vars['old_click'] = game_vars['square_clicked']
        else: # if there is no piece or wrong colour piece where we clicked
            messagebox.showinfo("Move Not Allowed","No/Your piece there, try again")
            game_vars['onclick'] = 1 - game_vars['onclick']
    else: # this is our second click, we are selecting the square to move to
        row, column = game_vars['old_click']
        old_piece = board[row][column]
        if game_vars['square_clicked'] not in old_piece.possible_moves: # check possible move for piece
            messagebox.showinfo("Move Not Allowed", "Your piece cannot move there!")
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
