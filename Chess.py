import tkinter, Rules, Files

def set_up_window():
    window = tkinter.Tk()
    window.title('chess')
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file = Rules.path +'icon.gif'))
    start(window)

def start(window):
    w = tkinter.Label(window, image = Rules.photo)
    w.pack()
    ent = Entry(window)
    ent.pack()
    ent.focus_set() 
    menubar = tkinter.Menu(window)

    filemenu = tkinter.Menu(menubar, tearoff = 0)
    editmenu = tkinter.Menu(menubar, tearoff = 0)
    viewmenu = tkinter.Menu(menubar, tearoff= 0 )
    toolmenu = tkinter.Menu(menubar, tearoff = 0)
    helpmenu = tkinter.Menu(menubar, tearoff = 0)

    filemenu.add_command(label="New", command = play_chess(window))
    filemenu.add_command(label="Open", command = Files.onOpen(window, board))
    filemenu.add_command(label="Save", command = Files.onSave(board)
    filemenu.add_command(label="Exit", command = window.destroy())

    helpmenu.add_command(label="Open Guide", command = Files.openGuide())

    menubar.add_cascade(label="File", menu = filemenu)
    menubar.add_cascade(label="Edit", menu = editmenu)
    menubar.add_cascade(label="View", menu = viewmenu)
    menubar.add_cascade(label="Tools", menu = toolmenu)
    menubar.add_cascade(label="Help", menu = helpmenu)

    window.config(menu = menubar)
      
def play_chess(window):
    board = reset_board()
    create_board(window, board)
    window.mainloop()

def reset_board():
    board = []
    for row in range(0,8):
        rowlist = []
        for column in range(0,8):
            if row == 6:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'White_Pawn.gif', 'white', column, row))
            elif row == 1:
                rowlist.append(Rules.Pawn('Pawn', Rules.path+'Black_Pawn.gif', 'black', column, row))
            else:
                rowlist.append(0)
        board.append(rowlist)

    return board

def create_board(window, board):
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
#            square.bind("<Button-1>", on_click)
        if bttnclr == "white":
            bttnclr = "grey"
        else:
            bttnclr = "white"


if __name__ =="__main__":
    set_up_window()