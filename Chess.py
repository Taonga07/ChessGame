import tkinter, os

class Game_Object():
    def __init__(self, piece, icon, colour, column, row):
        self.icon = icon
        self.colour = colour
        self.piece = piece
        self.row = row
        self.column = column
        self.score = score

class Pawn(Game_Object):
    def __init__(self, icon):
        super().__int__(icon, colour) 
        self.piece = 'Pawn'

    def checkMove(new_row_number,new_column_number):
        pass

def on_click(event):
    global window
    global onclick
    global piecetomove
    global turn
    global old_colour
    onclick = onclick+1 
    square = event.widget
    row_number = int(square.grid_info()['row'])
    column_number = int(square.grid_info() ['column'])
    try:
        if (onclick == 1 and 
                (
                    (turn == 0 and board[row_number][column_number].colour == 'white') 
                    or 
                    (turn == 1 and board[row_number][column_number].colour == 'black')
                ) 
                or onclick == 2):
            currentText = square.cget('text')
            if onclick == 1:
                print('Where would you like to move your', board[row_number][column_number].piece, 'to?')
                old_colour = board[row_number][column_number].colour
            #print(board[row_number] [column_number].colour, oldclour)
                piecetomove = (row_number,column_number)
                return
            else:
                #changed to here - not debugged
                old_row_number, old_column_number = piecetomove
                if oldcolour != board[old_row_number][old_column_number].colour:
                    if board[old_row_number][old_column_number].checkMove(row_number,column_number):
                        board[row_number][column_number] = board[old_row_number][old_column_number]
                        board[piecetomove[0]][piecetomove[1]] = 0
        layout_window(window) 
        if turn == 0:
            turn = 1
        else:
            turn = 0
    except:
        if onclick == 1:
            print('No piece there, try again')
        else:
            print('an error has ocurred') 
    onclick = 0

def layout_window(window): 
    bttnclr='white'
    for row_number, row_list in enumerate(board):
        for column_number, column_entry in enumerate(row_list):
            try: 
                img = tkinter.PhotoImage(file = board[row_number] [column_number].icon)
                square = tkinter.Label(window, bg = bttnclr, image = img) 
                square.image = img
            except:
                square = tkinter.Label(window, text = '                 \n\n\n', bg = bttnclr)
            if bttnclr == 'white': 
                bttnclr = 'grey'
            else:
                bttnclr = 'white'
            square.grid(row = row_number, column = column_number)
            square.bind('<Button-1>', on_click)
        if bttnclr == 'white': 
            bttnclr = 'grey'
        else:
            bttnclr = 'white'

def create_board(board):
    for row in range(0,8):
        row_list = []
        for column in range(0,8):
            if row == 0:
                row_list.append(Game_Object(black_pieces[column], path+icons[column+8], 'black', column, row))
            elif row == 7:
                row_list.append(Game_Object(white_pieces[column], path+icons[column], 'white', column, row))
            elif row == 6:
                row_list.append(Game_Object('Pawn', path+'White_Pawn.gif', 'white', column, row))
            elif row == 1:
                row_list.append(Game_Object('Pawn', path+'Black_Pawn.gif', 'black', column, row))
            else: 
                row_list.append(0)
        board.append(row_list)

def play_chess(): 
    create_board(board)
    window = tkinter.Tk() 
    window.title('chess') 
    layout_window(window)
    #not sure what this line was doing?
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file= path +'Black_King.gif'))
    window.mainloop()
    #don't need to return window - everything is happening within the mainloop() from here on
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
piecetomove = (0) 
targetpiece = 0 
piecemove = 0 
piece_capture = 0 
onclick = 0 
window = None 
turn = 0
old_colour = 'white'

if __name__ =='__main__': 
    window = play_chess()