import tkinter, os

class GameObject():
    def __init__(self, piece, icon, colour, column, row):
        self.icon = icon
        self.colour = colour
        self.piece = piece
        self.row = row
        self.column = column
        self.score = score
        
class Pawn(GameObject):
    def __init__(self, piece, icon, colour, column, row):
        super().__init__(piece, icon, colour, column, row)
        self.piece = 'Pawn'

    def check_move(self, new_row_number,new_column_number):
        return True

def on_click(event):
    global turn
    global window
    global onclick
    global old_colour
    global piece_to_move
    onclick = onclick+1
    square = event.widget
    row_number = int(square.grid_info()["row"])
    column_number  = int(square.grid_info()["column"])
    try:
        if ((onclick == 1 
            and (
                (turn == 0 and board[row_number][column_number].colour == 'white') 
                or (turn == 1 and board[row_number][column_number].colour == 'black')
            )) 
            or onclick == 2
            ):
            currentText = square.cget("text")

            if onclick == 1:
                print('Where would you like to move your', board[row_number][column_number].piece, 'to?')
                old_colour = board[row_number][column_number].colour
                piece_to_move = row_number,column_number
                return
            else:
                if board[row_number][column_number] == 0: #nothing at the square we're moving to
                    if board[piece_to_move[0]][piece_to_move[1]].check_move(row_number,column_number):
                        board[row_number][column_number] = board[piece_to_move[0]][piece_to_move[1]]
                        board[piece_to_move[0]][piece_to_move[1]] = 0
                        layout_window(window)
                        if turn == 0:
                            turn = 1
                        else:
                            turn = 0

                elif (isinstance(board[row_number][column_number], GameObject) and
                    old_colour != board[row_number][column_number].colour):
                    if board[piece_to_move[0]][piece_to_move[1]].check_move(row_number,column_number):
                        board[row_number][column_number] = board[piece_to_move[0]][piece_to_move[1]]
                        board[piece_to_move[0]][piece_to_move[1]] = 0
                        layout_window(window)
                        if turn == 0:
                            turn = 1
                        else:
                            turn = 0
                else:
                    print('you can not take your own piece')
    except:
        if onclick == 1:
            print('No piece there, try again')
        else:
            print('an error has ocurred')
            raise
    onclick = 0
    
def layout_window(window):
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

def create_board(board):
    for row in range(0,8):
        rowlist = []
        for column in range(0,8):
            if row == 0:
                rowlist.append(GameObject(black_pieces[column], path+icons[column+8], 'black', column, row))
            elif row == 7:
                rowlist.append(GameObject(white_pieces[column], path+icons[column], 'white', column, row))
            elif row == 6:
                rowlist.append(Pawn('Pawn', path+'White_Pawn.gif', 'white', column, row))
            elif row == 1:
                rowlist.append(Pawn('Pawn', path+'Black_Pawn.gif', 'black', column, row))
            else:
                rowlist.append(0)
        board.append(rowlist)

def play_chess():
    create_board(board)
    window = tkinter.Tk()
    window.title('chess')
    layout_window(window)
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file= path +'Black_King.gif'))
    #statusbar = tkinter.Label(window, text=turn, bd=1, relief=tkinter.SUNKEN, anchor=tkinter.W)
    #statusbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
    window.mainloop()
    return window

def updateFile():
    Game = 0
    try:
        file = open(path + Game +'.txt','r')
        board_state = json.load(file)
        file.close()
    except:
        board_state = []
    if board_state == ' ':
        file = json.load(board)
    else:
        file = json.load(board)
    file.close()
    return board_state

#set up our path and icon images
cwd = os.getcwd()
resources = '/Chess_Resources/'
path = cwd + resources
icons = ['White_Rook.gif', 'White_Bishop.gif', 'White_Knight.gif', 'White_Queen.gif', 'White_King.gif', 'White_Knight.gif', 'White_Bishop.gif', 'White_Rook.gif', 'Black_Rook.gif', 'Black_Bishop.gif', 'Black_Knight.gif', 'Black_King.gif', 'Black_Queen.gif', 'Black_Knight.gif', 'Black_Bishop.gif', 'Black_Rook.gif'] #/media/barton_hill/THOMAS/ Digi@Local/MyCode/Python/4 - Green/Code/Chess_Resources/ gameOver = False
white_pieces = ['Rook', 'Bishop', 'Knight', 'Queen', 'King', 'Knight', 'Bishop', 'Rook']
black_pieces = ['Rook', 'Bishop', 'Knight', 'King', 'Queen', 'Knight', 'Bishop', 'Rook'] 

board = [] 
score = 0
piece_to_move = (0) 
targetpiece = 0 
piecemove = 0 
piece_capture = 0 
onclick = 0 
window = None 
turn = 0
old_colour = 'white'

if __name__ =="__main__":
    window = play_chess()