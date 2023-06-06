from tkinter import filedialog
import tkinter, Chess, os

def onOpen(window, board):
    Open = filedialog.askopenfilename(initialdir = "/",title = "Open file",filetypes = (("main files","*txt*"),("All files","*.*")))
    f = open(Open,"r")
    Chess.board = f.read()
    Chess.create_board(window, board)

def onSave(board):
    Save = filedialog.asksaveasfilename(initialdir = "/",title = "Save as",filetypes = (("main files","*txt*"),("All files","*.*")))
    file = open(Save,"w+")
    file.write(board)
    file.close() 

def openGuide():
    try:
        os.system("gedit Guide.txt")
    except:
        try:
            os.system("notepad Guide.txt")
        except:
            print("Neither gedit nor notepad could be used to open the file.")