import tkinter, Rules, Files

def set_up_window():
    window = tkinter.Tk()
    window.title('chess')
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file = Rules.path +'icon.gif'))
    #play_chess(window)
    start(window)
    return window


def start(window):
    board = reset_board()

    # Can explicitly set window size here if you like
    #window.geometry('400x400')

    photo = tkinter.PhotoImage(file = Rules.path + "Intro.gif")
    w = tkinter.Label(window, image = photo)
    # This tip keeps the image around, otherwise it doesnt display properly
    # Found it by a Google: http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    w.image = photo

    # Thomas: If you want to use "pack" here and then also use a grid later when you create the board
    #         then we need to remove all widgets from the window before we draw the board - see destroy_all_widgets
    #         or you can use "w.grid(column=0, row=0)" instead of the pack
    w.pack()

    ent = tkinter.Entry(window)
    ent.pack()
    ent.focus_set() 

    menubar = tkinter.Menu(window)

    filemenu = tkinter.Menu(menubar, tearoff = 0)
    editmenu = tkinter.Menu(menubar, tearoff = 0)
    viewmenu = tkinter.Menu(menubar, tearoff= 0 )
    toolmenu = tkinter.Menu(menubar, tearoff = 0)
    helpmenu = tkinter.Menu(menubar, tearoff = 0)

    # Thomas: You need to use "lambda:" here so it only runs the command when the menu option is clicked, rather than running it immediately
    filemenu.add_command(label="New", command = lambda: play_chess(window))
    filemenu.add_command(label="Open", command = lambda: Files.onOpen(window, board))
    filemenu.add_command(label="Save", command = lambda: Files.onSave(board))
    filemenu.add_command(label="Exit", command = lambda: window.destroy())

    helpmenu.add_command(label="Open Guide", command = lambda: Files.openGuide())

    menubar.add_cascade(label="File", menu = filemenu)
    menubar.add_cascade(label="Edit", menu = editmenu)
    menubar.add_cascade(label="View", menu = viewmenu)
    menubar.add_cascade(label="Tools", menu = toolmenu)
    menubar.add_cascade(label="Help", menu = helpmenu)

    window.config(menu = menubar)

# https://stackoverflow.com/questions/15781802/python-tkinter-clearing-a-frame
def destroy_all_widgets(window):
    for widget in window.winfo_children():
        widget.destroy()

def play_chess(window):
    destroy_all_widgets(window)
    board = reset_board()
    create_board(window, board)

def reset_board():
    board = []
    for row in range(0,8):
        rowlist = []
        for column in range(0,8):
#            if row == 7:
#                for i in range(Rules.white_pieces):
#                    rowlist.append(Rules.(i)(i, white_pieces[column], path+icons[column], 'white', column, row))
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
    window = set_up_window()
    window.mainloop()