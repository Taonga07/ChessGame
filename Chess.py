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


    # Scratch
    #               class      instances
    #   New sprite: Rook       MASTER COPY
    #       Clone Rook         SECOND COPY
    #       Clone Rook         THIRD COPY
    #
    # Python
    #   Define class: Rook     no automatic instance
    #    instruction book
    #
    #   board[0][0] = Rook(black)
    #   board[7][0] = Rook(black)
    #   rookBlackLeft = Rook(white)
    #   rookBlackRight = Rook(white)



    ### board[0][0] = Rook(black)
    ### board[1][0] = Knight(black)
    ### board[2][0] = Bishop(black)
    ### ...

    # End result:
    # Rook Knight  Bishop  Queen  King   Bishop  Knight  Rook           BLACK
    # Pawn Pawn    Pawn    Pawn   Pawn   Pawn    Pawn    Pawn           BLACK
    # 
    #
    #
    #
    # 
    # Pawn Pawn    Pawn    Pawn   Pawn   Pawn    Pawn    Pawn           WHITE
    # Rook Knight  Bishop  King   Queen  Bishop  Knight  Rook           WHITE



    for row in range(0,8):
        rowlist = []
        for column in range(0,8):
            if row == 0:
                rowlist.append(Rules.GameObject(Rules.pieces[column], Rules.path+Rules.icons[column+8], 'black', column, row, 6))
            elif row == 7:
                rowlist.append(Rules.GameObject(Rules.pieces[column], Rules.path+Rules.icons[column], 'white', column, row, 6))
            elif row == 6:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'White_Pawn.gif', 'white', column, row))
            elif row == 1:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'Black_Pawn.gif', 'black', column, row))
            else:
                rowlist.append(0)
        board.append(rowlist)

    # End result for the above code:
    # GameObject GameObject  GameObject  GameObject  GameObject   GameObject  GameObject  GameObject         BLACK
    # Pawn       Pawn        Pawn        Pawn        Pawn         Pawn        Pawn        Pawn               BLACK
    # 
    #
    #
    #
    # 
    # Pawn Pawn    Pawn    Pawn   Pawn   Pawn    Pawn    Pawn           WHITE
    # Rook Knight  Bishop  King   Queen  Bishop  Knight  Rook           WHITE


    return board

def create_board(window, board):

    #print(board)
    print("--------------------------------------------------------------------------------")
    print("Board:")
    print("")
    for boardRow in board:
        boardRowString = ""
        for boardRowItem in boardRow:
            # TODO: I would recommend using "None" to represent a blank board space
            if boardRowItem == 0:
                boardItemString = "_____"
            else:
                boardItemString = boardRowItem.getShortDescription()
            boardRowString += boardItemString + " "
        
        print("row: " + str(boardRowString))
    
    print("")
    print("--------------------------------------------------------------------------------")

if __name__ =="__main__":
    set_up_window()