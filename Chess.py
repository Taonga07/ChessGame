import tkinter, Rules, os

def set_up_window():
    window = tkinter.Tk()
    window.title('chess')
    window.tk.call('wm', 'iconphoto', window._w, tkinter.PhotoImage(file = Rules.path +'Black_King.gif'))
    play_chess(window)
    
def play_chess(window):
    board = reset_board()
    create_board(window, board)
    window.mainloop()

def reset_board():
    board = []
    return board

def create_board(window, board):
    pass

if __name__ =="__main__":
    set_up_window()