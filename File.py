from tkinter import filedialog, messagebox
import tkinter, json, Chess, os

def menu(window, board):
    menubar = tkinter.Menu(window)

    filemenu = tkinter.Menu(menubar, tearoff=0)
    editmenu = tkinter.Menu(menubar, tearoff=0)
    viewmenu = tkinter.Menu(menubar, tearoff=0)
    toolmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu = tkinter.Menu(menubar, tearoff=0)

    filemenu.add_command(label="New", command=lambda: Chess.play_chess())
    filemenu.add_command(label="Open", command=lambda: onOpen(window, board))
    filemenu.add_command(label="Save", command=lambda: onSave(board))
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=lambda: window.destroy())

    editmenu.add_command(label="custormise pieces", command=lambda: openGuide())
    editmenu.add_command(label="custormise board", command=lambda: openGuide())
    editmenu.add_checkbutton(label='Blindfold Chess', command=lambda: openGuide())

    viewmenu.add_checkbutton(label='points', command=lambda: openGuide())
    viewmenu.add_checkbutton(label='pieces taken', command=lambda: openGuide())
    viewmenu.add_checkbutton(label='computer evaluation', command=lambda: openGuide())
    viewmenu.add_command(label="game history", command=lambda: openGuide())

    toolmenu.add_command(label="takeback", command=lambda: openGuide())
    toolmenu.add_command(label="flip board", command=lambda: openGuide())
    toolmenu.add_command(label="Request stalemate", command=lambda: openGuide())
    toolmenu.add_command(label="Resighn", command=lambda: openGuide())
    toolmenu.add_command(label="hint", command=lambda: openGuide())

    helpmenu.add_command(label="Open Guide", command=lambda: openGuide())

    menubar.add_cascade(label="File", menu=filemenu)
    menubar.add_cascade(label="Edit", menu=editmenu)
    menubar.add_cascade(label="View", menu=viewmenu)
    menubar.add_cascade(label="Tools", menu=toolmenu)
    menubar.add_cascade(label="Help", menu=helpmenu)

    window.config(menu=menubar)

def onOpen():
    File = filedialog.askopenfilename(initialdir = "/home",title = "Open file",filetypes = (("main files","*txt*"),("All files","*.*")))
    board = []
    with open(File, 'r') as filehandle:
        for row in range(0, 8):
            rowlist = []
            for column in range(0,8):
                board.append(currentPlace)
    window = Chess.set_up_window()
    Chess.layout_board(window, board)
    window.mainloop()


def onSave(board):
    Save = filedialog.asksaveasfilename(initialdir = "/home",title = "Save as",filetypes = (("main files","*txt*"),("All files","*.*")))
    filehandle = open(Save, 'w')
    for column_number in range(0, 8):
        for row_number in range(0,8):
            if board[row_number][column_number] != None:
                write = board[row_number][column_number].piece + ' ' + board[row_number][column_number].colour + ' ' + str(row_number) + ' ' + str(column_number) + ' ' + '\n'
                filehandle.write(write)
    filehandle.close()
def openGuide():
    try:
        os.system("gedit Guide.txt")
    except:
        try:
            os.system("notepad Guide.txt")
        except:
            tkinter.messagebox.showerror("Error","This is not possible!")