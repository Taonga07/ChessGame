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
    check_pieces = []
    paths_to_king = [] # this is your blank list of lists
    for row_number in range(0, 8):
        for column_number in range(0, 8):
            test_piece = board[row_number][column_number]
            if (test_piece != None) and (test_piece.colour != colour):
                test_piece.find_moves(board)
                for move in test_piece.possible_moves:
                    row, column = move # set item to the row and column it is made of for future use
                    square = board[row][column] # set the position of the current square for future use
                    if (square != None) and (square.piece == 'King') and (square.colour == colour):
                        # why elif on line 60
                        # at least one of column / row has to have a path (otherwise you're on top of the king already)
                        # but it could be both, or just one - so you need both to be if just in case
                        if square.column - test_piece.column != 0:
                            column_dir = int((square.column - test_piece.column) / (abs(square.column - test_piece.column)))
                            column_path = list(range(test_piece.column, square.column, dir))
                        if square.row - test_piece.row != 0:
                            row_dir = int((square.row - test_piece.row) / (abs(square.row - test_piece.row)) )
                            row_path = list(range(test_piece.row, square.row, dir))
                        # then we test for the condition if either column/row are zeros
                        # you can have one or other, or neither, but not both
                        if square.column - test_piece.column == 0:
                            column_path = list(range(0, len(row_path)): 0 
                        elif square_row - test_piece.row == 0:
                            row_path = list(range(0, len(column_path)): 0) 
                        # I think you need to work out the row / column path and dir (assuming their not zero) first, then you can work out the case if one or other is zero

                            ''' #can i have two else's like if else
                            are on the same column
                            #dosn't this need to be a list of 0's for each move - yes, they're on the same column ?? how would i do this then 
                            # hang on - I'm thinking it through okay 
                            ??list(range(square.row, test_piece.column): '0') ???
                            # we do its from the other list
                            # can i put them togerther in on_clicke thing 
                            # don't think so - trying to think through the logic ... 

                            

                            '''''
                        
                        if test_piece.piece != 'Knight':
                            check_pieces.append(    )
    if check_pieces != []: #if pieces are threatening king
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
            # first lets check if the piece we've selected to defend is one that can defend
            row, column = game_vars['old_click']
            defending_piece = board[row][column]
            #print('old_piece', defending_piece)
            #print('defending pieces', counter_check)
            if defending_piece in counter_check:
                #print('defender in counter_check')
                # now we can check if our defending piece is being moved into the proper position
                for attacking_piece in check_pieces:
                    # so here
                    # instead of attacking_piece.possible_moves we need path_to_king
                    # so we need something like...
                    # need to 'find' the king and pick up their row / column
                    #i did this up at line 48
                    path_to_king = ((king.row, king.column), (attacking_piece.row, attacking_piece.column))
                    if (game_vars['square_clicked'] in attacking_piece.possible_moves or
                            game_vars['square_clicked'] == (attacking_piece.row, attacking_piece.column)):
                        # we have moved our piece to defendcan actually move into a suitable position
                        return False                   
            print(check_pieces, 'can be countered by', counter_check)
            messagebox.showinfo('Check')
        return True
    return False

    def path_to_king(self, king_pos, attacker_pos)

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
        if CheckForCheck(board, old_piece.colour, game_vars): # check for check/checkmate
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
