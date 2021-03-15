from tkinter import filedialog, messagebox
import tkinter, json, Chess, os, CP, CD

def menu(window, board):
    menubar = tkinter.Menu(window)

    filemenu = tkinter.Menu(menubar, tearoff=0)
    editmenu = tkinter.Menu(menubar, tearoff=0)
    viewmenu = tkinter.Menu(menubar, tearoff=0)
    toolmenu = tkinter.Menu(menubar, tearoff=0)
    helpmenu = tkinter.Menu(menubar, tearoff=0)

    filemenu.add_command(label="New", command=lambda: onNew(window, board, 'Test.txt'))
    filemenu.add_command(label="Open", command=lambda: onOpen(window, board))
    filemenu.add_command(label="Save", command=lambda: onSave(window, board))
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

def onNew(window, board, filename):
    board = Chess.open_board(filename)
    Chess.layout_board(window, board)

def onOpen(window, board):
    filename = filedialog.askopenfilename(initialdir=CD.save_path, title='Open file',
                        filetypes=(("main files","*txt*"),("All files","*.*")))
    CD.save_path = os.path.split(filename)[0]   # update save location
    onNew(window, board, filename)

def onSave(window, board):
    filename = filedialog.asksaveasfilename(initialdir=CD.save_path, title='Save as',
                        filetypes=(("main files","*txt*"),("All files","*.*")))
    CD.save_path = os.path.split(filename)[0]   # update save location
    Chess.save_board(filename, board)

def openGuide():
    try:
        os.system("gedit Guide.txt")
    except:
        try:
            os.system("notepad Guide.txt")
        except:
            messagebox.showerror("Error","This is not possible!")