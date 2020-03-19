import Chess
from tkinter import *
from tkinter import filedialog def onOpen():
Open = filedialog.askopenfilename(initia ldir =
"/",title = "Open file",filetypes = (("main
files","*txt*"),("All files","*.*")))
f = open(Open,"r") Chess.board = f.read()
Chess.layout_window(Chess.win dow, board)
def onSave(): Save =
filedialog.asksaveasfilename(init ialdir =
"/",title = "Save as",filetypes = (("main
files","*txt*"),("All files","*.*"))) file = open(Save,"w+") file.write(Chess.board) file.close()
def main():
window = Tk() window.geometry('700x550')

window.title("Main")
photo = PhotoImage(file = Chess.path+"Intro.gif")
window.tk.call('wm', 'iconphoto',
window._w, PhotoImage(file= Chess.path +'Black_King.gif'))
w = Label(window, image=photo)
w.pack()
ent = Entry(window) ent.pack()
ent.focus_set()
menubar = Menu(window) filemenu = Menu(menubar,
tearoff=0)
editmenu = Menu(menubar,
tearoff=0)
veiwmenu = Menu(menubar,
tearoff=0)
toolmenu = Menu(menubar,
tearoff=0)
helpmenu = Menu(menubar,
tearoff=0)
filemenu.add_command(label=" New",

command=Chess.play_Chess)
filemenu.add_command(label=" Open",
command=onOpen)
filemenu.add_command(label=" Save",
command=onSave)
filemenu.add_command(label=" Exit",
command=window.quit)
menubar.add_cascade(label="Fil e",
menu=filemenu)
menubar.add_cascade(label="E dit",
menu=editmenu)
menubar.add_cascade(label="Vi ew",
menu=veiwmenu)
menubar.add_cascade(label="To ols",

menu=toolmenu)
menubar.add_cascade(label="H elp",
menu=helpmenu)
window.config(menu=menubar) windzow.mainloop()
if __name__ =="__main__": window = main()
