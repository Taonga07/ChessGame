import tkinter
class Game_Object():
def __init__(self, piece, icon,
colour, column, row): self.icon = icon
self.colour = colour self.piece = piece self.row = row self.column = column self.score = score
class Pawn(Game_Object): def __init__(self, icon):
super().__int__(icon, colour) self.piece = 'Pawn'
def checkMove(newrowNumber,new columnNumber):
pass
def on_click(event):
global window global onclick global piecetomove global turn
onclick = onclick+1 square = event.widget

bttnclr="white"
rowNumber = int(square.grid_info()["row"])
columnNumber = int(square.grid_info() ["column"])
try:
if onclick == 1 and ((turn ==
0 and board[rowNumber] [columnNumber].colour == 'white') or (turn == 1 and board[rowNumber] [columnNumber].colour == 'black')) or onclick == 2:
currentText = square.cget("text")
if onclick == 1: print('Where would you
like to move your', board[rowNumber] [columnNumber].piece, 'to?')
oldclour = board[rowNumber]
[columnNumber].colour
#print(board[rowNumber] [columnNumber].colour,

oldclour)
piecetomove =
rowNumber,columnNumber return
else:
# if oldcolour !=
board[oldrowNumber] [oldcolumnNumber].colour:
# if board[oldrowNumber] [oldcolumnNumber].checkMove (rowNumber,columnNumber)
oldrownumber,oldcolumnNumbe r = piecetomove
board[rowNumber] [columnNumber] =
board[oldrownumber] [oldcolumnNumber]
board[piecetomove[0]] [piecetomove[1]] = 0
# print(board[rowNumber]
[columnNumber].colour, oldclour)
layout_window(window) if turn == 0:
turn = 1

else:
turn = 0
except:
if onclick == 1:
print('No piece there, try again')
else:
print('an error has
ocurred') onclick = 0
def layout_window(window): bttnclr="white"
for rowNumber, rowlist in
enumerate(board):
for columnNumber,
columnEntry in enumerate(rowlist):
try: img =
tkinter.PhotoImage(file = board[rowNumber] [columnNumber].icon)
square = tkinter.Label(window, bg =
bttnclr, image = img) square.image = img
except:

square = tkinter.Label(window, text = "
\n\n\n", bg = bttnclr)
if bttnclr == "white": bttnclr = "grey"
else:
bttnclr = "white"
square.grid(row = rowNumber, column =
columnNumber)
square.bind("<Button-1>", on_click)
if bttnclr == "white": bttnclr = "grey"
else:
bttnclr = "white"
def create_board(board): global squaresToClear for row in range(0,8):
rowlist = []
for column in range(0,8):
if row == 0:
rowlist.append(Game_Object(bla ck_pieces[column],

path+icons[column+8], 'black', column, row))
elif row == 7:
rowlist.append(Game_Object(wh ite_pieces[column], path+icons[column], 'white', column, row))
elif row == 6:
rowlist.append(Game_Object('Pa wn', path+'White_Pawn.gif', 'white', column, row))
elif row == 1:
rowlist.append(Game_Object('Pa wn', path+'Black_Pawn.gif', 'black', column, row))
else: rowlist.append(0)
board.append(rowlist)
def play_Chess(): create_board(board) window = tkinter.Tk() window.title('chess') layout_window(window) window.tk.call('wm',

'iconphoto', window._w, tkinter.PhotoImage(file= path +'Black_King.gif'))
window.mainloop() return window
def updateFile(): Game = 0
try:
file = open(path + Game +'.txt','r')
board_state = json.load(file)
file.close() except:
board_state = [] if board_state == ' ':
file = json.load(board) else:
file = json.load(board) file.close()
return board_state
path = 'D:/Digi@Local/MyCode/

Python/4 - Green/Code/ Chess_Resources/'
icons = ['White_Rook.gif', 'White_Bishop.gif', 'White_Knight.gif', 'White_Queen.gif', 'White_King.gif', 'White_Knight.gif', 'White_Bishop.gif', 'White_Rook.gif', 'Black_Rook.gif', 'Black_Bishop.gif', 'Black_Knight.gif', 'Black_King.gif', 'Black_Queen.gif', 'Black_Knight.gif', 'Black_Bishop.gif', 'Black_Rook.gif'] #/media/barton_hill/THOMAS/ Digi@Local/MyCode/Python/4 - Green/Code/Chess_Resources/ gameOver = False
score = 0
white_pieces = ['Rook', 'Bishop', 'Knight', 'Queen', 'King', 'Knight', 'Bishop', 'Rook']
black_pieces = ['Rook', 'Bishop', 'Knight', 'King', 'Queen', 'Knight',

'Bishop', 'Rook'] board = [] piecetomove = 0 targetpiece = 0 piecemove = 0 piece_capture = 0 onclick = 0 window = None turn = 0
if __name__ =="__main__": window = play_Chess()
